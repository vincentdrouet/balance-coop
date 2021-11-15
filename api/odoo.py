import json
import logging
import os
import re
import xmlrpc.client
from datetime import datetime
from typing import Dict, List

from api import config

unp = [re.compile(p, re.IGNORECASE) for p in config.odoo.unp]

DATA_PATH = os.getenv("DATA_PATH", "./data/odoo.json")


class OdooAPI:
    def __init__(self):
        try:
            common_proxy_url = "{}/xmlrpc/2/common".format(config.odoo.url)
            object_proxy_url = "{}/xmlrpc/2/object".format(config.odoo.url)
            self.common = xmlrpc.client.ServerProxy(common_proxy_url)
            self.uid = self.common.authenticate(
                config.odoo.db, config.odoo.user, config.odoo.passwd, {}
            )
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
            config.odoo.db,
            self.uid,
            config.odoo.passwd,
            entity,
            "search_read",
            [cond if cond else []],
            fields_and_context,
        )

    def authenticate(self, login, password):
        return self.common.authenticate(config.odoo.db, login, password, {})


def _load_from_file() -> Dict:
    if not os.path.exists(DATA_PATH):
        return {
            "date": "",
            "products": [],
        }
    with open(DATA_PATH) as json_file:
        return json.load(json_file)


def _save_in_file(products):
    if os.path.exists(DATA_PATH):
        os.remove(DATA_PATH)
    with open(DATA_PATH, "w") as json_file:
        json.dump(products, json_file)


def _consolidate(products: List[Dict]) -> Dict:
    cid_to_c = {}
    for c, cids in config.odoo.categories.items():
        for cid in cids:
            cid_to_c[cid] = c
    for product in products:
        product["bio"] = product["name"].find(" Bio") >= 0
        if product["barcode"] and product["barcode"][0:3] == "260":
            product["id"] = int(product["barcode"][3:7])
        else:
            product["id"] = None
        categ_id = product["categ_id"][0]
        product["category"] = cid_to_c[categ_id]
        name = product["name"]
        for p in unp:
            name = p.sub("", name)
        product["name"] = name.strip()
    return {
        "date": datetime.now().strftime("%d/%m/%y %H:%M"),
        "products": products,
    }


def variable_weight_products():
    try:
        odoo_api = OdooAPI()
        cids = [cid for cids in config.odoo.categories.values() for cid in cids]
        products = odoo_api.search_read(
            "product.product",
            cond=[
                ["sale_ok", "=", True],
                ["categ_id", "in", cids],
            ],
            fields=[
                "barcode",
                "categ_id",
                "image_medium",
                "name",
                "theoritical_price",
            ],
            order="name ASC",
        )
        logging.info(f"{len(products)} products found")
        data = _consolidate(products)
        _save_in_file(data)
        data["synced"] = True
        return data
    except Exception as e:
        logging.error(e)
        data = _load_from_file()
        data["synced"] = False
        return data
