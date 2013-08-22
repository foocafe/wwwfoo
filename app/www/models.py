# -*- coding: utf-8 -*-

from django.db import models

__author__ = 'Hakan Svalin'
__version__ = '1.0'

class Image(models.Model):
    """ Image model

    """
    IMAGE_CATEGORIES = (
        ('FPS', 'Front page slider'),
    )

    class Meta:
        db_table = 'foo_images'

    title = models.CharField(verbose_name='Image title', max_length=255)

    category = models.CharField(verbose_name="Image category", max_length=60,
                                choices=IMAGE_CATEGORIES)

    tagging = models.CharField(verbose_name='Image tagging', max_length=255)

    image = models.ImageField(upload_to='images')

    def __unicode__(self):
        return self.title

    @property
    def url(self):
        return self.image.url
