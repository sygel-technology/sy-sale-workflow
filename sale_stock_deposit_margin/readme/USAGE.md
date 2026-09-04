## How to Use This Module

#### 1. Configure the Module
- Go to the README of `sale_stock_deposit` and follow the configuration instructions.

#### 2. Create a New Quotation
- Select a customer who has a deposit.

#### 3. Verify the Warehouse
- Go to the **‘Other Info’** tab → **‘Delivery’** section.
- Ensure that the selected warehouse corresponds to the location where the customer's deposit is stored.

#### 4. Select a Product from the Deposit
- Choose a product that the customer currently has in deposit, which was previously added through a **sale using the ‘Sale to Deposit’ route**.

#### 5. Set the Correct Route
- Select the **Route**: `(<warehouse_name>) / Deposit Delivery`.

#### 6. Review the Margin Calculation
- You will see that the **‘Margin’** and **‘Margin (%)’** fields in the line are automatically computed as **0**.


Note: The negative margins are not displayed by default. If you remove the Deposit Delivery route, the margin will be set again, but you'll also have to set again the unit price of the product, which is automatically set to 0 when you select the Deposit Delivery route.
