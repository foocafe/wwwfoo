# -*- coding: utf-8 -*-

from django.contrib import admin
from app.foo.models import PartnerAddress, PartnerSocial, PartnerContact, \
    Partner, Event, Speaker, Tag, Language

from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

__author__ = 'Hakan Svalin'
__version__ = '1.0'

class PartnerAddressAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }


class SocialAdmin(admin.ModelAdmin):
    pass


class PartnerContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','phone')
    search_fields = ('name', 'email')


class SpeakerAdmin(admin.ModelAdmin):
    filter_horizontal = ('languages','tags')

class TagAdmin(admin.ModelAdmin):
    pass


class PartnerAdmin(admin.ModelAdmin):
    pass


class EventAdmin(admin.ModelAdmin):
    pass

class LanguageAdmin(admin.ModelAdmin):
    pass

admin.site.register(PartnerAddress, PartnerAddressAdmin)
admin.site.register(PartnerSocial, SocialAdmin)
admin.site.register(PartnerContact, PartnerContactAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Language, LanguageAdmin)

admin.site.register(Partner, PartnerAdmin)
admin.site.register(Event, EventAdmin)
