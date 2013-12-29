=============================
 Microdata plugin for Sphinx
=============================

`Microdata`_ semantic markups support for `Sphinx`_ Documentation Generator.

This plugin is derived from `pelican-microdata`_.

Installation
------------

See `sphinx-contrib`_ for more details.

To install the plugin, you have to run these commands:

.. code-block:: bash

    python setup.py build
    python setup.py install

Usage
-----

To load the plugin, you have to add it in your ``conf.py`` file.

.. code-block:: python

    extensions = [
      ...
      'sphinxcontrib.microdata',
      ]

Directives
----------

Microdata plugin provides two directives:

- ``itemscope``, a block directive allowing to declare an itemscope block:

    .. code-block:: ReST

        .. itemscope:: <Schema type>
            :tag: element type (default: div)
            :itemprop: optionnal itemprop attribute
            :compact: optionnal

            Nested content

- ``itemprop``, an inline directive/role allowing to annotate some text with an itemprop attribute.

    .. code-block:: ReST

        :itemprop:`Displayed text <itemprop name>`
        :itemprop:`Displayed text <itemprop name:http://some.url/>`

Example
-------

This reStructuredText document:

.. code-block:: ReST

    .. itemscope: Person
        :tag: p

        My name is :itemprop:`Bob Smith <name>`
        but people call me :itemprop:`Smithy <nickanme>`.
        Here is my home page:
        :itemprop:`www.exemple.com <url:http://www.example.com>`
        I live in Albuquerque, NM and work as an :itemprop:`engineer <title>`
        at :itemprop:`ACME Corp <affiliation>`.

will result in:

.. code-block:: html

    <p itemscope itemtype="http://data-vocabulary.org/Person">
        My name is <span itemprop="name">Bob Smith</span>
        but people call me <span itemprop="nickname">Smithy</span>.
        Here is my home page:
        <a href="http://www.example.com" itemprop="url">www.example.com</a>
        I live in Albuquerque, NM and work as an <span itemprop="title">engineer</span>
        at <span itemprop="affiliation">ACME Corp</span>.
    </p>

This reStructuredText document using nested itemscope:

.. code-block:: ReST

    .. itemscope:: Person
    
        My name is :itemprop:`John Doe <name>`
    
        .. itemscope:: Address
            :tag: p
            :itemprop: address
    
            I live in :itemprop:`Albuquerque <name>`

will result in:

.. code-block:: html

    <div itemscope itemtype="http://data-vocabulary.org/Person">
    <p>
    My name is <span itemprop="name">John Doe</span>
    </p>
    <p itemprop="address" itemscope itemtype="http://data-vocabulary.org/Address">
    I live in <span itemprop="name">Albuquerque</span>'
    </p>
    </div>

This reStructuredText document using nested and compact itemscope:

.. code-block:: ReST

    .. itemscope:: Person
        :tag: p
        :compact:
    
        My name is :itemprop:`John Doe <name>`
    
        .. itemscope:: Address
            :tag: span
            :itemprop: address
    
            I live in :itemprop:`Albuquerque <name>`

will result in:

.. code-block:: html

    <p itemscope itemtype="http://data-vocabulary.org/Person">
    My name is <span itemprop="name">John Doe</span>
    <span itemprop="address" itemscope itemtype="http://data-vocabulary.org/Address">
    I live in <span itemprop="name">Albuquerque</span>
    </span>
    </p>

.. .............................................................................

.. _Microdata: http://schema.org
.. _Sphinx: http://sphinx-doc.org
.. _sphinx-contrib:  https://bitbucket.org/birkenfeld/sphinx-contrib
.. _pelican-microdata: https://github.com/noirbizarre/pelican-microdata

.. End
