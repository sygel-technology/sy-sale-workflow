.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl
    :alt: License: AGPL-3

================================
SO Sequence Confirmed Order Type
================================

This module allows you to assign a different prefix to sales orders in 'Done' or 'Sale' status depending on the type of sale.

For example: 'SQ-0001' in 'Draft' status, can be renamed to 'SO-0001' in 'Done' or 'Sale' status.


Installation
============

To install this module, you need to:

#. Only install


Configuration
=============

To configure this module, you need to:

#. Go to Sales -> Configuration -> Sale Order Type.
#. Create or edit a new type of sale.
#. Select an 'Entry Sequence'.
#. Check 'Different Prefix for Confirmed Sale Orders'.
#. Enter the new prefix for confirmed sale orders in the 'Confirmed Sale Order Prefix' field.
#. Save the changes.


Usage
=====

To use this module, you need to:

#. Go to the Sales module
#. Select or create a new quotation
#. Click on confirm

The name of the confirmed sales order will be prefixed with the new prefix.


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

This module is part of the `Sygel/sy-sale-workflow <https://github.com/sygel-technology/sy-sale-workflow>`_.

To contribute to this module, please visit https://github.com/sygel-technology.
