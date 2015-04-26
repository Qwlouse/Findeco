#!/usr/bin/env python3
# coding=utf-8
# region License
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
#endregion #####################################################################
"""
This file contains models for the basic Project structure:
  * Add a UserProfile to every User
  * automatize admin creation for every syncdb
"""

from datetime import datetime
import random

from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import signals

from findeco.settings import ACTIVATION_KEY_VALID_FOR, ADMIN_PASS
from findeco.settings import RECOVERY_KEY_VALID_FOR
import microblogging.models as microblogging_models
import node_storage.models as node_storage_models
from node_storage import Node, Text


def generate_key(nr_of_chars=64):
    return "".join(random.choice("0123456789BCDFGHKLMNPQRSTVWXYZ")
                   for _ in range(nr_of_chars))


####################### Add profile to each user ###############################
class UserProfile(models.Model):
    """
    Contains a textual description and a list of Users this User follows.
    """
    # The user this profile belongs to
    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE)

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

    is_verified_until = models.DateTimeField(default=datetime.min)
    last_seen = models.DateTimeField(default=datetime.min)
    verification_key = models.CharField(max_length=64, default=generate_key)
    api_key = models.CharField(max_length=16, default=lambda: generate_key(16))

    wants_mail_notification = models.BooleanField(default=False)
    help_enabled = models.BooleanField(default=True)
    preferred_language = models.CharField(max_length=20, default="")

    # Override the save method to prevent integrity errors
    # These happen because both the post_save signal and the inlined admin
    # interface try to create the UserProfile. See:
    # http://stackoverflow.com/questions/2813189
    def save(self, *args, **kwargs):
        try:
            existing = UserProfile.objects.get(user=self.user)
            self.id = existing.id  # force update instead of insert
        except UserProfile.DoesNotExist:
            pass
        models.Model.save(self, *args, **kwargs)

    def __unicode__(self):
        return '<Profile of %s>' % self.user.username


# Use post_save signal to ensure the profile will be created automatically
# when a user is created (saved for the first time)
# noinspection PyUnusedLocal
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
    else:
        # also save the profile when the user is saved
        instance.profile.save()


signals.post_save.connect(create_user_profile, sender=User)


####################### Activation Models ######################################
class Activation(models.Model):
    key = models.CharField(max_length=100, default=generate_key)
    key_valid_until = models.DateTimeField()
    user = models.ForeignKey(User)

    @classmethod
    def create(cls, user):
        key = generate_key()
        # make sure it is unique :-)
        while cls.objects.filter(key=key).count() > 0:
            key = generate_key()

        valid_until = datetime.now() + ACTIVATION_KEY_VALID_FOR
        entry = cls(key=key, key_valid_until=valid_until, user=user)
        entry.save()
        return entry

    def is_valid(self):
        return datetime.now() < self.key_valid_until

    def resolve(self):
        if self.is_valid():
            self.user.is_active = True
            self.user.save()
            self.delete()
            return True
        else:
            self.delete()
            return False

    def __unicode__(self):
        return "<Activation for %s>" % self.user.username


class EmailActivation(models.Model):
    key = models.CharField(max_length=100, default=generate_key)
    new_email = models.EmailField()
    user = models.ForeignKey(User)

    @classmethod
    def create(cls, user, new_email):
        # if there is already an entry: overwrite it
        try:
            entry = cls.objects.get(user=user)
        except cls.DoesNotExist:
            entry = cls(user=user)

        entry.key = generate_key()
        # make sure it is unique :-)
        while cls.objects.filter(key=entry.key).count() > 0:
            entry.key = generate_key()
        entry.new_email = new_email
        entry.save()

        return entry

    def resolve(self):
        self.user.email = self.new_email
        self.user.save()
        self.delete()
        return True

    def __unicode__(self):
        return "<EmailActivation for %s>" % self.user.username


class PasswordRecovery(models.Model):
    key = models.CharField(max_length=100, default=generate_key)
    key_valid_until = models.DateTimeField()
    user = models.ForeignKey(User)

    @classmethod
    def create(cls, user):
        # if there is already an entry: overwrite it
        try:
            entry = cls.objects.get(user=user)
            if not entry.is_valid():
                entry.delete()
            else:
                # can't request again if request is still open to prevent spam
                return None
        except cls.DoesNotExist:
            pass

        key = generate_key()
        # make sure it is unique :-)
        while cls.objects.filter(key=key).count() > 0:
            key = generate_key()
        key_valid_until = datetime.now() + RECOVERY_KEY_VALID_FOR
        return cls.objects.create(
            user=user, key=key, key_valid_until=key_valid_until)

    def is_valid(self):
        return datetime.now() < self.key_valid_until

    def resolve(self):
        if self.is_valid():
            password = User.objects.make_random_password()
            self.user.set_password(password)
            self.user.save()
            self.delete()
            return password
        else:
            self.delete()
            return False

    def __unicode__(self):
        return "<PasswordRecovery for %s>" % self.user.username

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
    try:
        auth_models.User.objects.get(username='admin')
    except auth_models.User.DoesNotExist:
        print('*' * 80)
        print('Creating admin -- login: admin, password: ' + ADMIN_PASS)
        print('*' * 80)
        auth_models.User.objects.create_superuser('admin', 'a@b.de', ADMIN_PASS)
    else:
        print('Admin user already exists.')


def create_root():
    try:
        Node.objects.get(id=1)
        print('Root node already present. Skipping initialization.')
    except Node.DoesNotExist:
        print('*' * 80)
        print('Creating root node ...')
        node = Node()
        node.node_type = Node.STRUCTURE_NODE
        node.title = "ROOT"
        node.save()
        root_text = Text()
        root_text.text = "This is the root node."
        root_text.node = node
        root_text.save()
        root_text.authors = [auth_models.User.objects.get(username='admin')]
        root_text.save()
        node_storage_models.PathCache.objects.create(path='', node=node)
        print('*' * 80)


def create_system_user():
    try:
        auth_models.User.objects.get(username='system')
    except auth_models.User.DoesNotExist:
        print('*' * 80)
        print('Creating system user without login.')
        print('*' * 80)
        User.objects.create(username='system')
    else:
        print('system user already exists.')


def get_system_user():
    return auth_models.User.objects.get(username='system')


def create_anonymous_user():
    try:
        auth_models.User.objects.get(username='anonymous')
    except auth_models.User.DoesNotExist:
        print('*' * 80)
        print('Creating anonymous user without login.')
        print('*' * 80)
        User.objects.create(username='anonymous')
    else:
        print('anonymous user already exists.')


def get_permission(name):
    a, _, n = name.partition('.')
    return auth_models.Permission.objects.get(content_type__app_label=a, codename=n)


def create_groups():
    if Group.objects.filter(
            name__in=["texters", "voters", "bloggers"]).count() > 0:
        print("groups already present... skipping")
        return
    print('*' * 80)
    print('Creating groups -- texters, voters, bloggers ')
    print('*' * 80)
    #### Create a group of Texters
    g = Group.objects.create(name="texters")
    perms = ['node_storage.add_node', 'node_storage.add_argument',
             'node_storage.add_derivation', 'node_storage.add_nodeorder',
             'node_storage.add_text']
    for p in perms:
        g.permissions.add(get_permission(p))
    g.save()
    #### Create a group of Voters
    g = Group.objects.create(name="voters")
    perms = ['node_storage.add_vote', 'node_storage.add_spamflag',
             'node_storage.change_vote', 'node_storage.change_spamflag',
             'node_storage.delete_vote', 'node_storage.delete_spamflag'
             ]
    for p in perms:
        g.permissions.add(get_permission(p))
    g.save()
    #### Create a group of Bloggers
    g = Group.objects.create(name="bloggers")
    perms = ['microblogging.add_post']
    for p in perms:
        g.permissions.add(get_permission(p))
    g.save()


# noinspection PyUnusedLocal
def initialize_database(*sender, **kwargs):
    create_admin()
    create_system_user()
    create_anonymous_user()
    create_root()


# noinspection PyUnusedLocal
def initialize_groups(sender, **kwargs):
    create_groups()


signals.post_syncdb.connect(initialize_database,
                            sender=node_storage_models,
                            dispatch_uid='findeco.models.initialize_database')

signals.post_syncdb.connect(initialize_groups,
                            sender=microblogging_models,
                            dispatch_uid='findeco.models.initialize_groups')