from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField

class Brand(models.Model):
    name = models.CharField(max_length=250, unique=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now = True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
		if not self.created_at:
			self.created_at = timezone.now()

		self.updated_at = timezone.now()
		return super(Brand, self).save(*args, **kwargs)

class Wrestler(models.Model):
    name = models.CharField(max_length=250, unique=True)
    ovr = models.IntegerField(max_length=2)
    country = CountryField(blank_label='USA')
    brand = models.ForeignKey(Brand, blank=True, default='', null=True, on_delete=models.SET_DEFAULT)
    height = models.IntegerField(max_length=3, null=True, blank=True)
    weight = models.IntegerField(max_length=3, null=True, blank=True)
    original_primary = models.IntegerField(max_length=3, default=0)
    original_secondary = models.IntegerField(max_length=3, default=0)
    primary = models.IntegerField(max_length=3, default=0)
    secondary = models.IntegerField(max_length=3, default=0)
    tertiary = models.IntegerField(max_length=3, default=0)
    tag_team = models.IntegerField(max_length=3, default=0)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now = True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
		if not self.created_at:
			self.created_at = timezone.now()

		self.updated_at = timezone.now()
		return super(Wrestler, self).save(*args, **kwargs)

class TagTeam(models.Model):
    name = models.CharField(max_length=250, unique=True)
    members = models.ManyToManyField(Wrestler)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now = True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'tagteams'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
		if not self.created_at:
			self.created_at = timezone.now()

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
    name = models.CharField(max_length=250, unique=True)
    belt_type = models.CharField(choices=BELT_TYPE_CHOICES, max_length=2, default=PRIMARY)
    champion = models.ForeignKey(Wrestler, blank=True, default='', null=True)
    champion2 = models.ForeignKey(Wrestler, blank=True, default='', null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now = True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def is_tagteam(self):
        return self.belt_type in (self.TAG_TEAM)

    def save(self, *args, **kwargs):
		if not self.created_at:
			self.created_at = timezone.now()

		self.updated_at = timezone.now()
		return super(Championship, self).save(*args, **kwargs)

class Event(models.Model):
    name = models.CharField(max_length=250)
    year = models.CharField(max_length=4)
    brand = models.ForeignKey(Brand, blank=True, default='')
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now = True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['name', 'year']

    def __str__(self):
        return ("%s (%s)"%(self.name, self.year))

    def save(self, *args, **kwargs):
		if not self.created_at:
			self.created_at = timezone.now()

		self.updated_at = timezone.now()
		return super(Event, self).save(*args, **kwargs)

class MatchType(models.Model):
    name = models.CharField(max_length=250, unique=True)
    no_of_participants = models.IntegerField(max_length=2, default=2)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now = True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
		if not self.created_at:
			self.created_at = timezone.now()

		self.updated_at = timezone.now()
		return super(MatchType, self).save(*args, **kwargs)

class Match(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    championship = models.ForeignKey(Championship, null=True, blank=True)
    match_type = models.ForeignKey(MatchType, blank=True, default='')
    participants = models.ManyToManyField(Wrestler, null=True, blank=True)
    winner = models.ForeignKey(Wrestler)
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