from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django_countries.fields import CountryField

class Brand(models.Model):
    slug = models.SlugField(max_length=40, unique=True)
    name = models.CharField(max_length=250, unique=True)
    color = models.CharField(max_length=20, default='black')
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now = True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wwe2k16:brands')

    def save(self, *args, **kwargs):
        if not self.created_at:
			self.created_at = timezone.now()

        self.slug = slugify(self.name)
        self.updated_at = timezone.now()
        return super(Brand, self).save(*args, **kwargs)

class Wrestler(models.Model):
    slug = models.SlugField(max_length=40, unique=True)
    name = models.CharField(max_length=250, unique=True)
    ovr = models.PositiveIntegerField(default=0)
    country = CountryField(blank_label='USA')
    brand = models.ForeignKey(Brand, blank=True, default='', null=True, on_delete=models.SET_DEFAULT)
    height = models.PositiveIntegerField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)
    original_primary = models.PositiveIntegerField(default=0)
    original_secondary = models.PositiveIntegerField(default=0)
    primary = models.PositiveIntegerField(default=0)
    secondary = models.PositiveIntegerField(default=0)
    tertiary = models.PositiveIntegerField(default=0)
    tag_team = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now = True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wwe2k16:wrestler', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.created_at:
			self.created_at = timezone.now()

        self.slug = slugify(self.name)
        self.updated_at = timezone.now()
        return super(Wrestler, self).save(*args, **kwargs)

class TagTeam(models.Model):
    slug = models.SlugField(max_length=40, unique=True)
    name = models.CharField(max_length=250, unique=True)
    members = models.ManyToManyField(Wrestler)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now = True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'tagteams'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wwe2k16:tagteam', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.created_at:
			self.created_at = timezone.now()
        
        self.slug = slugify(self.name)
        self.updated_at = timezone.now()
        return super(TagTeam, self).save(*args, **kwargs)

class Championship(models.Model):
    PRIMARY = 'PR'
    SECONDARY = 'SE'
    TERTIARY = 'TE'
    TAG_TEAM = 'TT'
    BELT_TYPE_CHOICES = (
        (PRIMARY, 'Primary'),
        (SECONDARY, 'Secondary'),
        (TERTIARY, 'Tertiary'),
        (TAG_TEAM, 'Tag Team'),
    )
    slug = models.SlugField(max_length=40, unique=True)
    name = models.CharField(max_length=250, unique=True)
    belt_type = models.CharField(choices=BELT_TYPE_CHOICES, max_length=2, default=PRIMARY)
    champion = models.ManyToManyField(Wrestler, blank=True, default='')
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now = True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def is_tagteam(self):
        return self.belt_type in (self.TAG_TEAM)

    def get_absolute_url(self):
        return reverse('wwe2k16:championship', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.created_at:
			self.created_at = timezone.now()

        self.slug = slugify(self.name)
        self.updated_at = timezone.now()
        return super(Championship, self).save(*args, **kwargs)

class Event(models.Model):
    slug = models.SlugField(max_length=40, unique=True)
    name = models.CharField(max_length=250)
    year = models.CharField(max_length=4)
    brand = models.ForeignKey(Brand, blank=True, default='')
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now = True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['name', 'year']

    def __str__(self):
        return "%s (%s)" % (self.name, self.year)

    def get_absolute_url(self):
        return reverse('wwe2k16:event', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
		if not self.created_at:
			self.created_at = timezone.now()

		self.slug = slugify(self.name)
		self.updated_at = timezone.now()
		return super(Event, self).save(*args, **kwargs)

class MatchType(models.Model):
    slug = models.SlugField(max_length=40, unique=True)
    name = models.CharField(max_length=250, unique=True)
    no_of_participants = models.PositiveIntegerField(default=2)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now = True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wwe2k16:matchtype', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
		if not self.created_at:
			self.created_at = timezone.now()

		self.slug = slugify(self.name)
		self.updated_at = timezone.now()
		return super(MatchType, self).save(*args, **kwargs)

class Match(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    championship = models.ForeignKey(Championship, null=True, blank=True)
    match_type = models.ForeignKey(MatchType, blank=True, default='')
    participants = models.ManyToManyField(Wrestler, blank=True, related_name='participating_match')
    winner = models.ForeignKey(Wrestler, null=True, blank=True, related_name='winning_match')
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now = True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'matches'

    def save(self, *args, **kwargs):
		if not self.created_at:
			self.created_at = timezone.now()

		self.updated_at = timezone.now()
		return super(Match, self).save(*args, **kwargs)