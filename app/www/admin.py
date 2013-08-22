# -*- coding: utf-8 -*-

from django.contrib import admin
from app.www.models import Image

__author__ = 'Hakan Svalin'
__version__ = '1.0'

class ImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Image, ImageAdmin)