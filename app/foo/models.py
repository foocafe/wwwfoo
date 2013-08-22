# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.contrib.sites.models import Site
from taggit.managers import TaggableManager
from django_google_maps import fields as google_map_fields

__author__ = 'Hakan Svalin'
__version__ = '0.0.1'


def today_at(hour, minute=0):
    now = datetime.datetime.now()
    return datetime.datetime(now.year, now.month, now.day, hour, minute)

def today_at_eight():
    return today_at(8)

def today_at_five():
    return today_at(17)

class PartnerAddress(models.Model):
    """ Partner address model, physical or in real life.
    """

    class Meta:
        db_table = "foo_partner_addresses"

    def __unicode__(self):
        return "%s - %s, %s" % (self.address_1, self.city, self.country_code)

    # Partner
    partner = models.ForeignKey('Partner')

    # Address line 1
    address_1 = models.CharField(max_length=80, verbose_name="Address line 1")

    # Address line 2
    address_2 = models.CharField(max_length=80, verbose_name="Address line 2", null=True, blank=True)

    # Postal code
    postal_code = models.CharField(max_length=10, verbose_name="Postal Code")

    # City
    city = models.CharField(max_length=80, verbose_name="City")

    # ISO Country code
    country_code = models.CharField(max_length=2, verbose_name="Country code",
        default="SE",
        help_text="Restrain your self to ISO country codes like, SE, US, BB etc")

    # Google specific GEO location
    geo_location = google_map_fields.GeoLocationField(max_length=100, null=True,
        blank=True,
        help_text="I think this one should be a Google Maps link, I'm not sure..."
        )


class PartnerSocial(models.Model):
    """ Partners social media channels.
    """
    CHANNELS = (('FB', 'Facebook'),
                ('LI', 'LinkedIn'),
                ('TW','Twitter'),
                ('IG', 'Instagram'))
    class Meta:
        db_table = "foo_partner_social"

    def __unicode__(self):
        return "%s - %s" % (self.channel_name(self.channel), self.value)

    def channel_name(self, channel):
        """ Return the name of the specified channel token
        """
        result = "Unknown - %s" % (channel,)
        for ch in PartnerSocial.CHANNELS:
            if ch[0] == channel:
                result = ch[1]
                break

        return result

    # The partner
    partner = models.ForeignKey(to='Partner')

    # Kind of social channel
    channel = models.CharField(max_length=2, choices=CHANNELS,
                               blank=False, null=False,
                               verbose_name="Channel")

    # URL, token or any other value that identifies the channel
    value = models.CharField(max_length=255, blank=False, null=False,
                             verbose_name='Value',
                             help_text="URL, token or other value...")


class PartnerContact(models.Model):
    """ Partner contact, typically a person.
    """

    class Meta:
        db_table = "foo_partner_contact"

    def __unicode__(self):
        return "%s - %s %s" % (self.name, self.email, self.phone)

    # The partner
    partner = models.ForeignKey('Partner')

    title = models.CharField(max_length=20, null=True, blank=True,
                             verbose_name='Title')

    name = models.CharField(max_length=60,
                            verbose_name='Name')

    email = models.EmailField(blank=True, null=True,
                              verbose_name="Email")

    phone = models.CharField(max_length=20, blank=True, null=True,
                             verbose_name="Phone number",
                             help_text=None)

    # Any comments in regards to this partner contact
    comment = models.TextField()


class Language(models.Model):
    """

    """

    def __unicode__(self):
        return "%s - %s" % (self.name, self.code)

    # ISO language code
    code = models.CharField(max_length=2, unique=True, primary_key=True)

    # Name of the language
    name = models.CharField(max_length=80)


class Tag(models.Model):
    """ Tagging... might be something out there I can use instead of implementing
    a tagging model on my own...
    """
    # The tag name
    name = models.CharField(max_length=80, unique=True)

    def __unicode__(self):
        return self.name


class Speaker(models.Model):
    """ A speaker is a prominent (nah!) person who might be, or
    has been a speaker at Foo
    """
    class Meta:
        db_table = 'foo_speaker'


    def __unicode__(self):
        return self.name

    # Speaker name, first and last
    name = models.CharField(max_length=80, verbose_name='Name',
                            help_text='First and last name, please.')

    # Languages this speaker is fluent in
    languages = models.ManyToManyField(Language, verbose_name='Language(s)')

    # Tags
    tags = models.ManyToManyField(Tag, verbose_name="Tagging", blank=True, null=True)

class Partner(models.Model):
    """ Partner model
    A partner has a name, a partnership classification, an URL and
    an image or logo.


    """
    # Partnership categorization
    PARTNERSHIP = (("R", "Regular"), ("P", "Premium"))
    CHAPTERS = (
        ('ALL', 'All'),
        ('MMX', 'Malmö'),
        ('BB',  'Barbados'),
        ('STK', 'Stockholm'),
        ('GBG', 'Göteborg')
    )

    class Meta:
        db_table = 'foo_partners'

    # Partner name
    name = models.CharField(verbose_name='Partner name', max_length=60, unique=True)

    # Partnership
    partnership = models.CharField(verbose_name='Partnership', max_length=2,
                                   choices=PARTNERSHIP)


    # Foo Chapter this partner is connected to
    chapter = models.CharField(max_length=10, choices=CHAPTERS,
                                   default=CHAPTERS[1][0])

    # Active or not
    active = models.BooleanField(verbose_name='Partnership active or not', default=True)

    # URL
    url = models.URLField(
        null=True, blank=True,
        verbose_name='Partner URL',
        help_text='Complete URL to partners site, e.g. http://www.foocafe.org'
    )

    # Image or Logo
    logo = models.ImageField(
        null=True, blank=True,
        verbose_name="Logo image",
        upload_to='partner-logos'
    )

    # Comments
    comment = models.TextField(blank=True, null=True, verbose_name='Comments')

    # Address of this partner
    address = models.ManyToManyField(to=PartnerAddress,
        related_name='partner_address',
        null=True, blank=True,
        verbose_name='Address(es)'
    )

    # Contacts
    contacts = models.ManyToManyField(to=PartnerContact,
        related_name='partner_contact',
        null=True, blank=True,
        verbose_name="Contact(s)"
    )

    # Social
    social = models.ManyToManyField(to=PartnerSocial,
                                    null=True, blank=True,
                                    related_name='partner_social',
                                    verbose_name='Social Channels'
                                    )

    def __unicode__(self):
        return self.name

    @property
    def is_premium_partner(self):
        return self.partnership == 'PP'

    @property
    def is_partner(self):
        return self.partnership == 'PA'

    @property
    def is_supporter(self):
        return self.partnership == 'SU'

    @property
    def image_url(self):
        """
        Shortcut to the image fields url
        """
        return self.image.url


class Event(models.Model):
    """ Event model, what we do at foo, events, conferences, seminars etc.
    """

    CATEGORIES = ((0,'None'), (1, 'Code'), (2, 'People'),
                  (3, 'Business'), (4, 'Innovation'), (5, 'Cutting Edge'))

    class Meta:
        db_table = "foo_events"

    # Title
    title = models.CharField(max_length=60)

    # Slug/ID
    slug = models.SlugField(max_length=60, unique=True, blank=True, null=True)

    # Event description
    description = models.TextField(max_length=1024)

    # Event categorization
    category = models.PositiveSmallIntegerField(default=0, choices=CATEGORIES)

    # Event start
    start = models.DateTimeField(verbose_name="Start", default=today_at_eight)

    # Event end
    end = models.DateTimeField(verbose_name="Ends", default=today_at_five)

    capacity = models.PositiveSmallIntegerField(default=20,
        verbose_name="Capacity",
        help_text="How many can come..."
    )

    registration_count = models.PositiveSmallIntegerField(default=0,
        verbose_name="Registrations",
        help_text="Number of registrations (so far)"
    )

    attender_count = models.PositiveSmallIntegerField(default=0,
        verbose_name="Attenders",
        help_text="How many was attending"
    )


