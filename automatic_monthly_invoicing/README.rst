.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl
    :alt: License: AGPL-3

===========================
Automatic Monthly Invoicing
===========================
This module allows you to invoice all non invoiced the sales orders of the previous month in a single invoice 
automatically for partners who have configured it this way.



Installation
============

To install this module, you need to:

#. Only install



Configuration
=============

To configure this module, you need to:

#. Go to the partner or Invoice Address for which you want monthly invoices to be generated.
#. Check the option 'Automatic Monthly Invoicing'.

By default, the module generates the invoices in draft status in case you want to generate the 
invoices and validate them automatically, you can do it from developer mode by doing the following steps:

#. Go to 'Settings' -> 'Technical' -> 'Scheduled Actions'.
#. Go to the action 'Automatic Monthly Invoicing Scheduled Action'.
#. Edit the code field in the 'Python Code' tab.
#. Change: 'create_monthly_invoices(validate=False)' to 'create_monthly_invoices(validate=True)'.
#. Save.



Usage
=====

To use this module you need to:

#. Create a new sales order, select a 'Invoice Address' that has the option 
    'Automatic Monthly Invoicing' checked.
#. All sales orders from that selected 'Invoice Address' will be automatically grouped into one 
    invoice on the first day of the following month.



Bug Tracker
===========

Bugs and errors are managed in `issues of GitHub <https://github.com/sygel/sy-sale-workflow/issues>`_.
In case of problems, please check if your problem has already been
reported. If you are the first to discover it, help us solving it by indicating
a detailed description `here <https://github.com/sygel/sy-sale-workflow/issues/new>`_.

Do not contact contributors directly about support or help with technical issues.



Credits
=======

Authors
~~~~~~~

* Sygel, Odoo Community Association (OCA)


Contributors
~~~~~~~~~~~~

* Ángel García de la Chica Herrera <angel.garcia@sygel.es>


Maintainer
~~~~~~~~~~

This module is maintained by Sygel.

.. image:: https://www.sygel.es/logo.png
   :alt: Sygel
   :target: https://www.sygel.es

This module is part of the `Sygel/sy-account-invoice-reporting <https://github.com/sygel-technology/sy-account-invoice-reporting>`_.

To contribute to this module, please visit https://github.com/sygel-technology.
