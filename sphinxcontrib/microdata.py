# -*- coding: utf-8 -*-

# Derived from https://github.com/noirbizarre/pelican-microdata
#   author: Axel Haustant
#   email: noirbizarre+pelican@gmail.com
#   license: GNU LESSER GENERAL PUBLIC LICENSE Version 3

""" Microdata semantic markups support for Sphinx Documentation Generator. """

####################################################################################################

from __future__ import unicode_literals

import re

from docutils import nodes
from sphinx.util.compat import Directive
from docutils.parsers.rst import directives

from sphinx.writers.html import HTMLTranslator
from sphinx.writers.text import TextTranslator
from sphinx import addnodes

####################################################################################################

# match: value <name>
role_regexp = re.compile(r'(?P<value>.+?)\s*\<(?P<name>.+)\>$')

####################################################################################################

class ItemScope(nodes.Element):

    """ This class defines an ItemScope node. """

    ##############################################

    def __init__(self, tagname, itemtype, itemprop=None, compact=False):

        # print 'microdata.ItemScope'

        kwargs = {
            'itemscope': None,
            'itemtype': "http://data-vocabulary.org/%s" % itemtype,
            }
        if itemprop:
            kwargs['itemprop'] = itemprop
        super(ItemScope, self).__init__('', **kwargs)
        self.tagname = tagname
        self.compact = tagname == 'p' or compact

####################################################################################################

class ItemProp(nodes.Inline, nodes.TextElement):
    """ This class defines an ItemProp node. """
    pass

####################################################################################################

class ItemScopeDirective(Directive):

    """ This class defines a ``itemscope`` directive.

    .. code-block:: ReST

        .. itemscope:: <Schema type>
            :tag: element type (default: div)
            :itemprop: optionnal itemprop attribute
            :compact: optionnal

            Nested content

    """

    required_arguments = 1
    has_content = True
    option_spec = {
        'tag': directives.unchanged,
        'itemprop': directives.unchanged,
        'compact': directives.unchanged,
        }

    ##############################################

    def run(self):

        # print 'microdata.ItemScopeDirective.run'

        self.assert_has_content()
        itemtype = self.arguments[0]
        tag = self.options.get('tag', 'div')
        itemprop = self.options.get('itemprop', None)
        compact = 'compact' in self.options
        node = ItemScope(tag, itemtype, itemprop, compact)
        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]

####################################################################################################

def itemprop_role(role, rawtext, text, lineno, inliner, options={}, content=[]):

    """ This class defines a ``itemprop`` role.

    .. code-block:: ReST

        :itemprop:`Displayed text <itemprop name>`
        :itemprop:`Displayed text <itemprop name:http://some.url/>`

    """

    # print 'microdata.itemprop_role'

    match = role_regexp.match(text)
    if not match.group('value') and match.group('name'):
        raise ValueError('%s does not match expected itemprop format: :itemprop:`value <name>`')
    value = match.group('value')
    name = match.group('name')
    if ':' in name:
        # :itemprop:`value <name:href>`
        name, href = name.split(':', 1)
    else:
        href = None

    return [ItemProp(value, value, name=name, href=href)], []

####################################################################################################

def visit_ItemScope_html(self, node):
    # print 'microdata.visit_ItemScope_html'
    self.body.append(node.starttag())

####################################################################################################

def depart_ItemScope_html(self, node):
    # print 'microdata.depart_ItemScope_html'
    self.body.append(node.endtag())

####################################################################################################

def visit_ItemProp_html(self, node):

    # print 'microdata.visit_ItemProp_html'
    if node['href']:
        self.body.append(self.starttag(node, 'a', '', itemprop=node['name'], href=node['href']))
    else:
        self.body.append(self.starttag(node, 'span', '', itemprop=node['name']))

####################################################################################################

def depart_ItemProp_html(self, node):

    # print 'microdata.depart_ItemProp_html'
    if node['href']:
        self.body.append('</a>')
    else:
        self.body.append('</span>')

####################################################################################################

def visit_paragraph_html(self, node):

    # print 'microdata.visit_paragraph_html'

    # docutils code was:
    #   if self.should_be_compact_paragraph(node):
    #       self.context.append('')
    #   else:
    #       self.body.append(self.starttag(node, 'p', ''))
    #       self.context.append('</p>\n')

    if (self.should_be_compact_paragraph(node)
        or (isinstance(node.parent, ItemScope) and node.parent.compact)):
        self.context.append('')
    else:
        self.body.append(self.starttag(node, 'p', ''))
        self.context.append('</p>\n')

####################################################################################################

def visit_ItemScope_text(self, node):
    # print 'microdata.visit_ItemScope_text'
    pass

####################################################################################################

def depart_ItemScope_text(self, node):
    # print 'microdata.depart_ItemScope_text'
    pass

####################################################################################################

def visit_ItemProp_text(self, node):
    # print 'microdata.visit_ItemProp_text'
    pass

####################################################################################################

def depart_ItemProp_text(self, node):
    # print 'microdata.depart_ItemProp_text'
    pass

####################################################################################################

def visit_paragraph_text(self, node):

    if (not isinstance(node.parent, nodes.Admonition)
        or isinstance(node.parent, addnodes.seealso)):
        self.new_state(0)

####################################################################################################

def setup(app):

    # print 'Load microdata'
    
    app.add_node(ItemScope,
                 html=(visit_ItemScope_html, depart_ItemScope_html),
                 text=(visit_ItemScope_text, depart_ItemScope_text),
                 )
    app.add_node(ItemProp,
                 html=(visit_ItemProp_html, depart_ItemProp_html),
                 text=(visit_ItemProp_text, depart_ItemProp_text),
                 )

    app.add_directive('itemscope', ItemScopeDirective)
    app.add_role('itemprop', itemprop_role)

    # handle compact parameter
    # TODO: find a cleaner way to handle this case
    HTMLTranslator.visit_paragraph = visit_paragraph_html
    # TextTranslator.visit_paragraph = visit_paragraph_text

####################################################################################################
# 
# End
# 
####################################################################################################
