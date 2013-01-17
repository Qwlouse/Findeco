#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Klaus Greff <klaus.greff@gmx.net>
# This file is part of Findeco.
#
# Findeco is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# Findeco is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Findeco. If not, see <http://www.gnu.org/licenses/>.
################################################################################
#
################################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
################################################################################
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
from node_storage import Node, Text

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
    user = models.OneToOneField(
        User,
        related_name='profile')

    description = models.TextField(
        blank=True,
        help_text="Self-description")

    followees = models.ManyToManyField(
        'self',
        related_name='followers',
        symmetrical=False,
        blank=True,
        help_text="Profiles of users this user follows.")

    blocked = models.ManyToManyField(
        'self',
        related_name='blocked_by',
        symmetrical=False,
        blank=True,
        help_text="Profiles of users this user blocked."
    )

    # Override the save method to prevent integrity errors
    # These happen because both teh post_save signal and the inlined admin
    # interface try to create the UserProfile. See:
    # http://stackoverflow.com/questions/2813189
    def save(self, *args, **kwargs):
        try:
            existing = UserProfile.objects.get(user=self.user)
            self.id = existing.id #force update instead of insert
        except UserProfile.DoesNotExist:
            pass
        models.Model.save(self, *args, **kwargs)

    def __unicode__(self):
        return '<Profile of %s>' % self.user.username

# Use post_save signal to ensure the profile will be created automatically
# when a user is created (saved for the first time)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
    else:
        # also save the profile when the user is saved
        instance.profile.save()

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
def create_admin():
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

def create_root():
    print('Creating root node ...')
    node = Node()
    node.node_type='structureNode'
    node.title = "ROOT"
    node.save()
    root_text = Text()
    root_text.text = "This is the root node."
    root_text.node = node
    root_text.save()
    root_text.authors = []
    root_text.save()

def initialize_database(sender, **kwargs):
    create_admin()
    if Node.objects.all().count() > 0:
        print('Root node already present. Skipping initialization.')
        return
    print('*'*80)
    print('Creating Initial Data')
    create_root()
    print('*'*80)
    #create_initial_data()

signals.post_syncdb.connect(initialize_database,
    sender=auth_models, dispatch_uid='findeco.models.initialize_database')