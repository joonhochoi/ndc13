from django.db import models
from django.utils.safestring import mark_safe
from datetime import datetime


class Tag(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=24, blank=True, null=True)
    image = models.ImageField(upload_to='tag', blank=True, null=True)

    def html_get_color_div(self):
        return mark_safe('<div style="background-color:%s; border:1px solid black; text-align:center;">sample</div>' % self.color)

    def __unicode__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class SessionDate(models.Model):
    day = models.DateField()

    def __unicode__(self):
        return str(self.day)


class SessionTime(models.Model):
    begin = models.TimeField()
    end = models.TimeField()

    def _todatetime(self, time):
        return datetime.today().replace(hour=time.hour, minute=time.minute, second=time.second,
                                        microsecond=time.microsecond, tzinfo=time.tzinfo)

    def duration_in_min(self):
        return (self._todatetime(self.end) - self._todatetime(self.begin)).seconds / 60

    def __unicode__(self):
        return '%s - %s' % (self.begin, self.end)


class Company(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __unicode__(self):
        return self.name


class Speaker(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    email = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    company = models.ForeignKey(Company, null=True)

    def __unicode__(self):
        return '%s(%s)' % (self.name, self.company)


class Session(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    desc = models.CharField(max_length=2000, null=True, blank=True, db_index=True)
    slide_url = models.CharField(max_length=255, null=True, blank=True)
    speakers = models.ManyToManyField(Speaker, blank=True)
    tags = models.ManyToManyField(Tag)

    room = models.ForeignKey(Room)
    date = models.ForeignKey(SessionDate)
    times = models.ManyToManyField(SessionTime)

    def duration_in_min(self):
        return sum([_.duration_in_min() for _ in self.times.all()])

    def get_companies(self):
        return set([_.company for _ in self.speakers.all()])

    def html_get_speakers(self):
        return ', '.join([_.name for _ in self.speakers.all()])

    def html_get_companies(self):
        return ', '.join([_.name for _ in self.get_companies()])

    def __unicode__(self):
        return self.name
