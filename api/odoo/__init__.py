import httpx
import logging
import os
import re

from aio_odoorpc_base.sync.common import login as odoo_login
from aio_odoorpc_base.sync.object import execute_kw
from aio_odoorpc_base.helpers import execute_kwargs
from tinydb import TinyDB
from typing import List, Dict

ODOO_URL = os.getenv("ODOO_URL", "https://test.sas.lachouettecoop.fr/jsonrpc")
ODOO_DB = os.getenv("ODOO_DB", "dbsas")
ODOO_LOGIN = os.getenv("ODOO_LOGIN")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

TINYDB_PATH = os.getenv("TINYDB_PATH", "./data/odoo.json")
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
]
UNWANTED_NAME_CHUNKS_PATTERNS = [
    re.compile(u, re.IGNORECASE) for u in UNWANTED_NAME_CHUNKS
]


def _load_from_db():
    db = TinyDB(TINYDB_PATH)
    products_table = db.table(PRODUCTS_TABLE)
    return products_table.all()


def _save_in_db(products):
    db = TinyDB(TINYDB_PATH)
    products_table = db.table(PRODUCTS_TABLE)
    products_table.truncate()
    for product in products:
        products_table.insert(product)


def _consolidate(products: List[Dict]):
    for product in products:
        name = product["name_template"]
        for p in UNWANTED_NAME_CHUNKS_PATTERNS:
            name = p.sub("", name)
        product["name"] = name.strip()
        product["bio"] = product["name_template"].find(" Bio") >= 0
        product["id"] = int(product["barcode"][3:6])
        categ_id = product["categ_id"][0]
        if categ_id in VRAC:
            product["categ"] = "vrac"
        elif categ_id in FRUITS:
            product["categ"] = "fruit"
        elif categ_id in LEGUMES:
            product["categ"] = "legume"
        elif categ_id in VIANDE:
            product["categ"] = "viande"
        elif categ_id in POISSON:
            product["categ"] = "poisson"
        elif categ_id in FRUITS_SECS:
            product["categ"] = "fruit_sec"
        else:
            product["categ"] = "autre"


def variable_weight_products():
    try:
        with httpx.Client(timeout=120) as client:
            uid = odoo_login(
                http_client=client,
                url=ODOO_URL,
                db=ODOO_DB,
                login=ODOO_LOGIN,
                password=ODOO_PASSWORD,
            )
            kwargs = execute_kwargs(
                fields=[
                    "barcode",
                    "categ_id",
                    "image_medium",
                    "name_template",
                    "theoritical_price",
                ]
            )
            products = execute_kw(
                http_client=client,
                url=ODOO_URL,
                db=ODOO_DB,
                uid=uid,
                password=ODOO_PASSWORD,
                obj="product.product",
                method="search_read",
                args=[
                    ["active", "=", True],
                    ["sale_ok", "=", True],
                    # In 'La Chouette Coop', all variable weight products have a barcode starting with 2600
                    ["barcode", "like", "2600_________"],
                ],
                kw=kwargs,
            )
            logging.info(f"{len(products)} products found")
            _consolidate(products)
            _save_in_db(products)
            return products
    except Exception as e:
        logging.error(e)
        return _load_from_db()
