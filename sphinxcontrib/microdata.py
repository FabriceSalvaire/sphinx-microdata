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

####################################################################################################

# match: value <name>
role_regexp = re.compile(r'(?P<value>.+?)\s*\<(?P<name>.+)\>$')

####################################################################################################

class ItemScope(nodes.Element):

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
    pass

####################################################################################################

class ItemScopeDirective(Directive):

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

def visit_ItemScope(self, node):
    # print 'microdata.visit_ItemScope'
    self.body.append(node.starttag())

####################################################################################################

def depart_ItemScope(self, node):
    # print 'microdata.depart_ItemScope'
    self.body.append(node.endtag())

####################################################################################################

def visit_ItemProp(self, node):

    # print 'microdata.visit_ItemProp'

    if node['href']:
        self.body.append(self.starttag(node, 'a', '', itemprop=node['name'], href=node['href']))
    else:
        self.body.append(self.starttag(node, 'span', '', itemprop=node['name']))

####################################################################################################

def depart_ItemProp(self, node):

    # print 'microdata.depart_ItemProp'

    if node['href']:
        self.body.append('</a>')
    else:
        self.body.append('</span>')

####################################################################################################

def visit_paragraph(self, node):

    # print 'microdata.visit_paragraph'

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

def setup(app):

    # print 'Load microdata'
    
    app.add_node(ItemScope,
                 html=(visit_ItemScope, depart_ItemScope),
                 )
    app.add_node(ItemProp,
                 html=(visit_ItemProp, depart_ItemProp),
                 )

    app.add_directive('itemscope', ItemScopeDirective)
    app.add_role('itemprop', itemprop_role)

    # handle compact parameter
    # TODO: find a cleaner way to handle this case
    HTMLTranslator.visit_paragraph = visit_paragraph

####################################################################################################
# 
# End
# 
####################################################################################################
