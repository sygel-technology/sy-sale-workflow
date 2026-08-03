- In future versions, we will consider modifying the sale order line widget to show the available quantity of the product in the customer's deposit.

- Note: If you make a 'Deposit Sale' of a product with lot numbers. You will need to use the same lot number in the 'Deposit Delivery', or another existing lot in the deposit. Odoo is not able to automatically select by default a lot that is in the deposit, because deposit delivery operations do not have the deposit as origin (the location odoo uses to get the lots). You can also make an inventory adjustment to fix this.

- The code inside the _search_rule() has been encapsulated in another function and also called from _get_rule(). Now, _get_rule() does not call _search_rule() inside sales confirmations, so the code to get the deposit rule has been moved to _get_rule(). Other functions could have been inherited, but, as they were too complex, this is the best way.
- The res_partner fields should be reviewed to determine if they should be commercial fields.
- Potential issue with multi-company configuration.
- Potential issue with contact merging.
- Review inherited functions.
