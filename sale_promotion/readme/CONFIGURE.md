To configure this module, you need to go to Sales > Products > Promotions and create a
new promotion. Create as many price rules as needed, considering the following fields:

1.  **Computation:** Select "Fixed Price" as the computation method and set a value
	in the "Fixed Price" field so that value will be set as the unit price in sale
	orders if that rule is applied. Select "Discount" as the computacion method	and
	set a value in the "Discount" field so that value will be set as the discount 
	in sale orders if that rule is applied.
2.  **Apply On:**  Select "All Products" if the price or the discount can be applied to 
	all products. Select "Product Category" and choose a category if the price or the 
	discount can applied to products of a given category. Select "Product" and choose 
	a product template if the price or the discount can be applied to a given product 
	template. Select "Product Variant" and choose a product variant if the price or 
	the discount can applied to a given product variant.
3.  **Min. Quantity:** The rule can only be applied if the quantity is equal or greater
	than the set value.
4.  **Validity:** The rule can only be applied if the date order is inbetween the selected
	dates.

Once a promotion is created, it is necessary to create a Campaign (Sales > Products > 
Campaigns).

1.  **Start Date:** Select a date if the promotion can only be applied from that date.
2.  **End Date:** Select a date if the promotion can only be applied before that date.
3.  **Pricelists:** Select the list of pricelists for which the campaign is available. The
	campaign will only be applied to a sale order if the order's pricelist is selected
	in this field.
4.  **Promotions:** Select the list of promotions that are part of the campaign.
