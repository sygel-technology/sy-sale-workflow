This module integrates sale_stock_deposit and sale_margin 
to automatically set the sale margin of Delivery Stock Deposit Sale Order Lines to 0.

This is done because the Delivery Stock Deposit Sale Order Lines are not invoiced, and the margin was already calculated when the original sale was initially processed, using the Sale to Deposit route.
