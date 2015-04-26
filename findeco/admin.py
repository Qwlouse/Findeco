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

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from .models import UserProfile, Activation, PasswordRecovery, EmailActivation


class UserProfileInline(admin.StackedInline):
    """
    Configure UserProfile to be inlined into user administration
    """
    model = UserProfile
    max_num = 1
    can_delete = False


class UserAdmin(AuthUserAdmin):
    # add UserProfile inline as an inline to UserAdmin page
    inlines = [UserProfileInline]

# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)


class ActivationAdmin(admin.ModelAdmin):
    model = Activation
    list_display = ('__unicode__', 'user', 'key_valid_until', 'key')
    list_display_links = ('__unicode__',)

admin.site.register(Activation, ActivationAdmin)


class EmailActivationAdmin(admin.ModelAdmin):
    model = EmailActivation
    list_display = ('__unicode__', 'user', 'new_email', 'key')
    list_display_links = ('__unicode__',)

admin.site.register(EmailActivation, EmailActivationAdmin)


class PasswordRecoveryAdmin(admin.ModelAdmin):
    model = PasswordRecovery
    list_display = ('__unicode__', 'user', 'key_valid_until', 'key')
    list_display_links = ('__unicode__',)

admin.site.register(PasswordRecovery, PasswordRecoveryAdmin)
