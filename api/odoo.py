import json
import logging
import os
import re
import xmlrpc.client
from typing import Dict, List

ODOO_URL = os.getenv("ODOO_URL", "https://test.sas.lachouettecoop.fr")
ODOO_DB = os.getenv("ODOO_DB", "dbsas")
ODOO_LOGIN = os.getenv("ODOO_LOGIN")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

# This is use to filter categories before send them to front
# For a scale used for fruits and vegetable no need to show all the others
CATEGORIES = os.getenv("CATEGORIES", "fruit legume").split()

DATA_PATH = os.getenv("DATA_PATH", "./data/odoo.json")
PRODUCTS_TABLE = "products"

# 139 - EPICERIE / VRAC
# 327 - EPICERIE / VRAC / FARINE, CEREALES, LEGUMINEUSES, FRUITS A COCQUES, ETC EN VRAC
# 328 - EPICERIE / VRAC / FRUITS SECS, GRAINES ETC RECONDITIONNES
VRAC = [139, 327, 328]
# 347 - FRAIS / VIANDE / CHARCUTERIE ET SALAISONS
# 351 - FRAIS / VIANDE / VIANDE DE PORC
# 353 - FRAIS / VIANDE / VOLAILLE ET GIBIERS
VIANDE = [347, 353, 351]
# 152 - FRAIS / POISSONNERIE
POISSON = [152]
# 337 - FRAIS / FRUITS ET LEGUMES / FRUITS
FRUITS = [337]
# 418 - FRAIS / FRUITS ET LEGUMES / LEGUMES
LEGUMES = [418]
# 122 - EPICERIE / FRUITS SECS EN PAQUET
FRUITS_SECS = [122]

UNWANTED_NAME_CHUNKS = [
    " vrac",
    " au kg",
    " 1 kg",
    " 1kg",
    " bio",
    " prix",
    " sous vide",
    " ss vide",
    " à la pièce",
    " maraîcher",
]
UNWANTED_NAME_CHUNKS_PATTERNS = [re.compile(u, re.IGNORECASE) for u in UNWANTED_NAME_CHUNKS]


class OdooAPI:
    def __init__(self):
        try:
            self.url = ODOO_URL
            self.db = ODOO_DB
            self.user = ODOO_LOGIN
            self.passwd = ODOO_PASSWORD
            common_proxy_url = "{}/xmlrpc/2/common".format(self.url)
            object_proxy_url = "{}/xmlrpc/2/object".format(self.url)
            self.common = xmlrpc.client.ServerProxy(common_proxy_url)
            self.uid = self.common.authenticate(self.db, self.user, self.passwd, {})
            self.models = xmlrpc.client.ServerProxy(object_proxy_url)
        except Exception as e:
            logging.error(f"Odoo API connection impossible: {e}")

    def search_read(self, entity, cond=None, fields=None, limit=0, offset=0, order="id ASC"):
        """Main api request, retrieving data according search conditions."""
        fields_and_context = {
            "fields": fields if fields else {},
            "context": {"lang": "fr_FR", "tz": "Europe/Paris"},
            "limit": limit,
            "offset": offset,
            "order": order,
        }

        return self.models.execute_kw(
            self.db,
            self.uid,
            self.passwd,
            entity,
            "search_read",
            [cond if cond else []],
            fields_and_context,
        )

    def authenticate(self, login, password):
        return self.common.authenticate(self.db, login, password, {})


def _load_from_file():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH) as json_file:
        return json.load(json_file)


def _save_in_file(products):
    if os.path.exists(DATA_PATH):
        os.remove(DATA_PATH)
    with open(DATA_PATH, "w") as json_file:
        json.dump(products, json_file)


def _consolidate(products: List[Dict]):
    for product in products:
        name = product["name_template"]
        for p in UNWANTED_NAME_CHUNKS_PATTERNS:
            name = p.sub("", name)
        product["name"] = name.strip()
        product["bio"] = product["name_template"].find(" Bio") >= 0
        product["id"] = int(product["barcode"][3:7])
        categ_id = product["categ_id"][0]
        if categ_id in VRAC and "vrac" in CATEGORIES:
            product["category"] = "vrac"
        elif categ_id in FRUITS and "fruit" in CATEGORIES:
            product["category"] = "fruit"
        elif categ_id in LEGUMES and "legume" in CATEGORIES:
            product["category"] = "legume"
        elif categ_id in VIANDE and "viande" in CATEGORIES:
            product["category"] = "viande"
        elif categ_id in POISSON and "poisson" in CATEGORIES:
            product["category"] = "poisson"
        elif categ_id in FRUITS_SECS and "fruit_sec" in CATEGORIES:
            product["category"] = "fruit_sec"
        else:
            product["category"] = "autre"


def variable_weight_products():
    try:
        odoo_api = OdooAPI()
        products = odoo_api.search_read(
            "product.product",
            cond=[
                ["sale_ok", "=", True],
                # In 'La Chouette Coop', all variable weight products
                # have a barcode starting with 260
                ["barcode", "like", "260__________"],
            ],
            fields=[
                "barcode",
                "categ_id",
                "image_medium",
                "name_template",
                "theoritical_price",
                "qty_available",
            ],
            order="name_template ASC",
        )
        logging.info(f"{len(products)} products found")
        _consolidate(products)
        _save_in_file(products)
        return products
    except Exception as e:
        logging.error(e)
        return _load_from_file()
