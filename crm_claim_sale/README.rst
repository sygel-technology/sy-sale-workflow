.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl
    :alt: License: AGPL-3

==============
CRM Claim Sale
==============

This module allows you to create a sale from a claim in the crm application using all the
fields of the claim by default.In addition, it also allows you to create a 'Sale Order Type'
to be used by default for Sales created from a Claim.


Installation
============

To install this module, you need to:

#. Only install


Configuration
=============

To configure this module, you need to:

#. Go to the Sales application.
#. Click on Configuration and go to "Sales Order Types".
#. Create a "Sales Order Types" and check the box "Default claim".

Note that there can only be one "Sale Order Type" with the "Default claim" field selected.
If there is already another "Sale Order Type" with the "Default claim" field selected you 
must first deactivate it before activating a new one.


Usage
=====

To use this module, you need to:

#. Create or edit a claim
#. Click on Create new quotation. 

You will see a new quotation being created with all the default claim data including the 
"Sale Order Type" you have configured for the claims.


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


Maintainer
~~~~~~~~~~

This module is maintained by Sygel.

.. image:: https://www.sygel.es/logo.png
   :alt: Sygel
   :target: https://www.sygel.es

This module is part of the `Sygel/sy-sale-workflow <https://github.com/sygel-technology/sy-sale-workflow/>`_.

To contribute to this module, please visit https://github.com/sygel-technology.
