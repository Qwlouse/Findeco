#!/usr/bin/python
# coding=utf-8
"""
This file contains models for the basic Project structure:
  * Add a UserProfile to every User
  * automatize admin creation for every syncdb
"""
from __future__ import division, print_function, unicode_literals
from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
try:
    from local_settings import ADMIN_PASS
except ImportError :
    ADMIN_PASS = "1234"

####################### Add profile to each user ###############################
class UserProfile(models.Model):
    """
    Contains a textual description and a list of Users this User follows.
    """
    # The user this profile belongs to
    user = models.OneToOneField(User)

    description = models.TextField(
        blank=True,
        help_text="Self-description")

    following = models.ManyToManyField(
        User,
        related_name='followers',
        symmetrical=False,
        blank=True,
        help_text="List of users this user follows.")

    def __unicode__(self):
        return '<Profile of %s>' % self.user.username

# Use post_save signal to ensure the profile will be created automatically
# when a user is created (saved for the first time)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

signals.post_save.connect(create_user_profile, sender=User)


############################ Automatic superuser creation ######################
# From http://stackoverflow.com/questions/1466827/
#
# Prevent interactive question about wanting a superuser created.
signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_models,
    dispatch_uid='django.contrib.auth.management.create_superuser')

# Create our own admin user automatically.
def create_admin(app, created_models, verbosity, **kwargs):
    if not settings.DEBUG:
        return
    try:
        auth_models.User.objects.get(username='admin')
    except auth_models.User.DoesNotExist:
        print('*' * 80)
        print('Creating admin -- login: admin, password: '+ADMIN_PASS)
        print('*' * 80)
        auth_models.User.objects.create_superuser('admin', 'a@b.de', ADMIN_PASS)
    else:
        print('Admin user already exists.')

signals.post_syncdb.connect(create_admin,
    sender=auth_models, dispatch_uid='common.models.create_admin')
