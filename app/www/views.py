# -*- coding: utf-8 -*-

import random

from django.shortcuts import render, render_to_response

from app.foo.models import Partner
from app.www.models import Image

__author__ = 'Hakan Svalin'
__version__ = '1.0'

def get_common_context_vars():
    """
    """
    partners_dict = {'premium': [], 'partner': [], 'supporter': []}
    partners = Partner.objects.all()
    for p in partners:
        if p.is_premium_partner:
            partners_dict['premium'].append(p)
        elif p.is_partner:
            partners_dict['partner'].append(p)
        else:
            partners_dict['supporter'].append(p)

    # To keep all partners happy shuffle them around
    for k in partners_dict:
        random.shuffle(partners_dict[k])

    result = {'partners': partners_dict}

    slider_images = Image.objects.filter(category='FPS')
    result['slider'] = slider_images

    return result

def index(request):
    return render_to_response("index.html", get_common_context_vars())
