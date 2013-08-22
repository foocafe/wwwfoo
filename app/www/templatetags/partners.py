# -*- coding: utf-8 -*-
from django import template

__author__ = 'Hakan Svalin'
__version__ = '1.0'

register = template.Library()

class PartnersNode(template.Node):
    pass

def do_partners(parser, token):
    try:
        tag_name, format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return PartnersNode()

