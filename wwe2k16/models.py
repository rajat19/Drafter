from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django_countries.fields import CountryField

INACTIVE = False
ACTIVE = True
STATUS_CHOICES = (
	(ACTIVE, 'Active'),
	(INACTIVE, 'Inactive'),
)
class Brand(models.Model):
	slug = models.SlugField(max_length=40, unique=True)
	name = models.CharField(max_length=250, unique=True)
	color = models.CharField(max_length=20, default='black')
	status = models.BooleanField(choices=STATUS_CHOICES, default=ACTIVE)
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
	country = CountryField(blank_label='( Select country )', blank=True)
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
		return reverse('wwe2k16:wrestler-add')

	def total_titles(self):
		return self.primary + self.secondary + self.tertiary + self.tag_team

	def total_points(self):
		return (3 * self.primary) + (2 * self.secondary) + (1 * self.tertiary) + (1 * self.tag_team) + (0.5 * self.ovr) + (self.original_primary)

	def save(self, *args, **kwargs):
		if not self.country:
			self.country = 'US'
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
	status = models.BooleanField(choices=STATUS_CHOICES, default=ACTIVE)
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
	brand = models.ForeignKey(Brand, blank=True, default='', null=True)
	created_at = models.DateTimeField(null=True, blank=True)
	updated_at = models.DateTimeField(auto_now = True, null=True, blank=True)
	deleted_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		unique_together = ['name', 'year']

	def __str__(self):
		return "%s (%s)" % (self.name, self.year)

	def get_absolute_url(self):
		return reverse('wwe2k16:event-add')

	def save(self, *args, **kwargs):
		if not self.created_at:
			self.created_at = timezone.now()

		self.slug = slugify(self.__str__)
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
		return reverse('wwe2k16:matchtype-add')

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
	participants = models.ManyToManyField(Wrestler, blank=True, related_name='participants')
	winner = models.ForeignKey(Wrestler, blank=True, related_name='winner')
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

class TagTeamMatch(models.Model):
	TEAM1 = 1
	TEAM2 = 2
	WINNER_CHOICES = (
		(TEAM1, 'Team 1'),
		(TEAM2, 'Team 2'),
	)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	championship = models.ForeignKey(Championship, null=True, blank=True)
	team1 = models.ManyToManyField(Wrestler, related_name='team1')
	team2 = models.ManyToManyField(Wrestler, related_name='team2')
	winner = models.PositiveSmallIntegerField(choices=WINNER_CHOICES, default=TEAM1)
	created_at = models.DateTimeField(null=True, blank=True)
	updated_at = models.DateTimeField(auto_now = True, null=True, blank=True)
	deleted_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		verbose_name_plural = 'matches'

	def save(self, *args, **kwargs):
		if not self.created_at:
			self.created_at = timezone.now()

		self.updated_at = timezone.now()
		return super(TagTeamMatch, self).save(*args, **kwargs)

class ChampionshipHistory(models.Model):
	match = models.ForeignKey(Match, null=True, blank=True)
	old_champion = models.ManyToManyField(Wrestler, blank=True, related_name='old_champion')
	new_champion = models.ManyToManyField(Wrestler, blank=True, related_name='new_champion')
	created_at = models.DateTimeField(null=True, blank=True)
	updated_at = models.DateTimeField(auto_now = True, null=True, blank=True)
	deleted_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		verbose_name_plural = 'history'

	def save(self, *args, **kwargs):
		if not self.created_at:
			self.created_at = timezone.now()

		self.updated_at = timezone.now()
		return super(ChampionshipHistory, self).save(*args, **kwargs)

class DraftHistory(models.Model):
	brand = models.ForeignKey(Brand)
	# TODO: change to arrayfield for postgresql
	data = models.CharField(null=True, blank=True)
	created_at = models.DateTimeField(null=True, blank=True)
	updated_at = models.DateTimeField(auto_now = True, null=True, blank=True)
	deleted_at = models.DateTimeField(null=True, blank=True)

	def save(self, *args, **kwargs):
		if not self.created_at:
			self.created_at = timezone.now()

		self.updated_at = timezone.now()
		return super(DraftHistory, self).save(*args, **kwargs)