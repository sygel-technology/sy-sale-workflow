To use this module, you need to:

To create a new 'Deposit Sale':

1. Create a new quotation.
2. Select a customer who has a deposit.
3. Go to the 'Other Info' tab -> 'Delivery' section 
4. Select the warehouse where the customer's deposit is located. 
5. Add a new product and Select the Route: '(<warehouse_name>) / Deposit Sale'
6. Confirm the Sale
7. Validate the generated picking. Remember to set the done quantities manually.
8. This picking will 'reserve' the stock of that product in your warehouse for the customer. This is achieved by moving (in Odoo) the stock from the deposit location to the customer location. Though the product is still in warehouse and it has not been delivered yet, it belongs to the customer, and the negative stock in the deposit location represents this, reserving the product for him.


To create a new 'Deposit Delivery':

1. Create a new quotation.
2. Select a customer who has a deposit.
3. Go to the 'Other Info' tab -> 'Delivery' section 
4. Select the warehouse where the customer's deposit is located.
5. Add the same product that was added to the deposit in the sale to deposit. 
6. Select the Route: '(<warehouse_name>) / Deposit Delivery'
7. Confirm the Sale
8. Validate the generated picking
9. This picking will remove the stock from the deposit, completing the delivery cicle in odoo. This is achieved by moving the stock (in odoo) from the deposit location to the customer location. This operation works correcly because the stock has previously been moved (in odoo) to the customer location, and the deposit location is negative.


On the other hand, you will be able to see the state of the customer's deposits.

1. Go to the 'Stock Deposits' tab of the contact and click on 'View Deposit Status', if you only want to see the status of one deposit.
2. From the contact's view header click on 'Deposits' to see the status of all the customer's deposits.
