from django.contrib.postgres.fields import ArrayField
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.query import QuerySet
from django.utils.text import slugify
from django.utils import timezone
from django_countries.fields import CountryField

INACTIVE = False
ACTIVE = True
STATUS_CHOICES = (
    (ACTIVE, 'Active'),
    (INACTIVE, 'Inactive'),
)


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class TimestampModel(models.Model):
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()

        self.updated_at = timezone.now()
        return super(TimestampModel, self).save(*args, **kwargs)


class SoftDeletionModel(TimestampModel):
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        super(SoftDeletionModel, self).save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()


class Brand(SoftDeletionModel):
    slug = models.SlugField(max_length=40, unique=True)
    name = models.CharField(max_length=250, unique=True)
    color = models.CharField(max_length=20, default='black')
    status = models.BooleanField(choices=STATUS_CHOICES, default=ACTIVE)

    def __str__(self):
        return self.name

    @staticmethod
    def get_absolute_url():
        return reverse('wwe2k16:brands')

    @staticmethod
    def db_fields():
        return ['name', 'color']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Brand, self).save(*args, **kwargs)


class Wrestler(SoftDeletionModel):
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

    def __str__(self):
        return self.name

    @staticmethod
    def get_absolute_url():
        return reverse('wwe2k16:wrestler-add')

    def original_titles(self):
        return self.original_primary + self.original_secondary

    def total_titles(self):
        return self.primary + self.secondary + self.tertiary + self.tag_team

    def total_points(self):
        return (3 * self.primary) + (2 * self.secondary) + (1 * self.tertiary) + (1 * self.tag_team) + (0.5 * self.ovr) + (self.original_primary)

    @staticmethod
    def db_fields():
        return [
            'name', 'ovr', 'country', 'brand', 'height', 'weight', 'original_primary',
            'original_secondary', 'primary', 'secondary', 'tertiary', 'tag_team'
        ]

    def save(self, *args, **kwargs):
        if not self.country:
            self.country = 'US'

        self.slug = slugify(self.name)
        return super(Wrestler, self).save(*args, **kwargs)


class TagTeam(SoftDeletionModel):
    slug = models.SlugField(max_length=40, unique=True)
    name = models.CharField(max_length=250, unique=True)
    members = models.ManyToManyField(Wrestler)

    class Meta:
        verbose_name_plural = 'tagteams'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wwe2k16:tagteam', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(TagTeam, self).save(*args, **kwargs)


class Championship(SoftDeletionModel):
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

    def __str__(self):
        return self.name

    def is_tag_team(self):
        return self.belt_type in self.TAG_TEAM

    def get_absolute_url(self):
        return reverse('wwe2k16:championship', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Championship, self).save(*args, **kwargs)


class Event(SoftDeletionModel):
    slug = models.SlugField(max_length=40, unique=True)
    name = models.CharField(max_length=250)
    year = models.CharField(max_length=4)
    brand = models.ForeignKey(Brand, blank=True, default='', null=True)

    class Meta:
        unique_together = ['name', 'year']

    def __str__(self):
        return "%s (%s)" % (self.name, self.year)

    def get_absolute_url(self):
        return reverse('wwe2k16:event', kwargs={'slug': self.slug})

    @staticmethod
    def db_fields():
        return ['name', 'brand', 'year']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.__str__)
        return super(Event, self).save(*args, **kwargs)


class MatchType(SoftDeletionModel):
    slug = models.SlugField(max_length=40, unique=True)
    name = models.CharField(max_length=250, unique=True)
    no_of_participants = models.PositiveIntegerField(default=2)

    def __str__(self):
        return self.name

    @staticmethod
    def get_absolute_url():
        return reverse('wwe2k16:matchtype-add')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(MatchType, self).save(*args, **kwargs)


class Match(TimestampModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    championship = models.ForeignKey(Championship, null=True, blank=True)
    match_type = models.ForeignKey(MatchType, blank=True, default='')
    participants = models.ManyToManyField(Wrestler, blank=True, related_name='participants')
    winner = models.ForeignKey(Wrestler, blank=True, related_name='winner', null=True)

    def __str__(self):
        return "%s (%s)" % (self.event, self.championship)

    class Meta:
        verbose_name_plural = 'matches'


class TagTeamMatch(TimestampModel):
    TEAM1 = 't1'
    TEAM2 = 't2'
    WINNER_CHOICES = (
        (TEAM1, 'Team 1'),
        (TEAM2, 'Team 2'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    tag_championship = models.ForeignKey(Championship, null=True, blank=True)
    team1 = models.ManyToManyField(Wrestler, related_name='team1', blank=True)
    team2 = models.ManyToManyField(Wrestler, related_name='team2', blank=True)
    tag_winner = models.CharField(choices=WINNER_CHOICES, default=TEAM1, max_length=2)

    def __str__(self):
        return "%s (%s)" % (self.event, self.tag_championship)

    class Meta:
        verbose_name_plural = 'tag_team_matches'


class ChampionshipHistory(TimestampModel):
    match = models.ForeignKey(Match, null=True, blank=True)
    tag_match = models.ForeignKey(TagTeamMatch, null=True, blank=True)
    old_champion = models.ManyToManyField(Wrestler, blank=True, related_name='old_champion')
    new_champion = models.ManyToManyField(Wrestler, blank=True, related_name='new_champion')

    def __str__(self):
        return "%s / %s" % (self.match, self.tag_match)

    class Meta:
        verbose_name_plural = 'championship_history'


class DraftHistory(SoftDeletionModel):
    name = models.CharField(max_length=200, null=True, blank=True)
    brand = models.ForeignKey(Brand)
    data = ArrayField(
        models.CharField(null=True, blank=True, max_length=1000),
        size=50,
        null=True
    )

    class Meta:
        verbose_name_plural = 'draft_history'
        unique_together = ['name', 'brand']


class TemporaryDraft(TimestampModel):
    brand = models.ForeignKey(Brand)
    wrestlers = models.ManyToManyField(Wrestler, blank=True)
