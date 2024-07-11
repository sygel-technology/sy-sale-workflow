# Copyright 2021 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Free Delivery Untaxed",
    "summary": "Decide if delivery is free based on untaxed price",
    "version": "15.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/sygel-technology/sy-sale-workflow",
    "author": "Sygel",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "delivery",
    ],
    "data": [
        "views/delivery_view.xml",
    ],
}
