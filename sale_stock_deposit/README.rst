.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
	:target: http://www.gnu.org/licenses/agpl
	:alt: License: AGPL-3

==================
Sale Stock Deposit
==================

This module allows you to create and control deposits for customers. 
With the deposits you will be able to create sales and pickings to customer deposits and subsequently, create sales and pickings from the deposits to the customer.


Installation
============

To install this module, you need to:

#. Only install

Note: Once installed the module will create the warehouses, types of operations, routes and rules for each warehouse available.


Configuration
=============

To configure this module, you need to:

#. Go to the Inventory module
#. Click on Configuration and then Settings
#. In the Traceability section activate 'Lots & Serial Numbers'.
#. In the Warehouse section activate 'Storage Locations' and 'Multi-Step Routes'.

To create a customer's deposit:

#. From the contact, go to the 'Stock deposit' tab and click on 'Create New Deposit'.
#. Enter the name. By default 'Deposit + <contact_name>'.
#. Select the Location from the different available deposits and save.


Usage
=====

To use this module, you need to:

To create a new 'Deposit Sale':

#. Create a new quotation.
#. Select a customer who has a deposit.
#. Go to the 'Other Info' tab -> 'Delivery' section 
#. Select the warehouse where the customer's deposit is located. 
#. Add a new product and Select the Route: '(<warehouse_name>) / Deposit Sale'
#. Confirm the Sale
#. Validate the generated picking. Remember to set the done quantities manually.

To create a new 'Delivery Stock Deposit':

#. Create a new quotation.
#. Select a customer who has a deposit.
#. Go to the 'Other Info' tab -> 'Delivery' section 
#. Select the warehouse where the customer's deposit is located.
#. Add the same product that was added to the deposit in the sale to deposit. 
#. Select the Route: '(<warehouse_name>) / Delivery Stock Deposit'
#. Confirm the Sale
#. Validate the generated picking

On the other hand, you will be able to see the state of the customer's deposits.

#. Go to the 'Stock Deposits' tab of the contact and click on 'View Deposit Status', if you only want to see the status of one deposit.
#. From the contact's view header click on 'Deposits' to see the status of all the customer's deposits.


ROADMAP
=======

In future versions, we will consider modifying the sale order line widget to show the available quantity of the product in the 
customer's deposit.

Note: If you make a 'Deposit Sale' of a product with lot numbers. You will need to use the same lot number in the 'Delivery Stock Deposit' or make an inventory adjustment.


Bug Tracker
===========

Bugs and errors are managed in `issues of GitHub <https://github.com/sygel-technology/sy-sale-workflow/issues>`_.
In case of problems, please check if your problem has already been
reported. If you are the first to discover it, help us solving it by indicating
a detailed description `here <https://github.com/sygel-technology/sy-sale-workflow/issues/new>`_.

Do not contact contributors directly about support or help with technical issues.


Credits
=======

Authors
~~~~~~~

* Sygel, Odoo Community Association (OCA)

Contributors
~~~~~~~~~~~~

* Ángel García de la Chica Herrera <angel.garcia@sygel.es>
* Valentin Vinagre <valentin.vinagre@sygel.es>

Maintainer
~~~~~~~~~~

This module is maintained by Sygel.

.. image:: https://www.sygel.es/logo.png
   :alt: Sygel
   :target: https://www.sygel.es

This module is part of the `Sygel/sy-sale-workflow <https://github.com/sygel-technology/sy-sale-workflow>`_.

To contribute to this module, please visit https://github.com/sygel-technology.