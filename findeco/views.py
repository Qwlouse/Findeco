#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Klaus Greff <klaus.greff@gmx.net>,
# Johannes Merkert <jonny@pinae.net>
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
from __future__ import division, print_function, unicode_literals
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.mail import send_mail
import json
import random

from findeco.view_helpers import create_graph_data_node_for_structure_node
import node_storage as backend
from node_storage.factory import create_user
from .paths import parse_suffix
from .view_helpers import *


@ensure_csrf_cookie
def home(request, path):
    with open("static/index.html", 'r') as index_html_file:
        return HttpResponse(index_html_file.read(), mimetype='text/html')



@ValidPaths("StructureNode")
@ViewErrorHandling
def load_index(request, path):
    node = assert_node_for_path(path)
    slot_list = backend.get_ordered_children_for(node)
    index_nodes = [create_index_node_for_slot(slot) for slot in slot_list]
    return json_response({'loadIndexResponse': index_nodes})


@ValidPaths("StructureNode")
@ViewErrorHandling
def load_argument_index(request, path):
    prefix, path_type = parse_suffix(path)
    node = assert_node_for_path(prefix)
    data = [create_index_node_for_argument(a, node) for a in
            node.arguments.order_by('index')]
    return json_response({'loadIndexResponse': data})


@ValidPaths("StructureNode")
@ViewErrorHandling
def load_graph_data(request, path, graph_data_type):
    if not path.strip('/'):  # root node!
        nodes = [backend.get_root_node()]
        related_nodes = []
    else:
        slot_path = path.rsplit('.', 1)[0]
        slot = assert_node_for_path(slot_path)
        nodes = backend.get_ordered_children_for(slot)
        sources = Q(derivates__in=nodes)
        derivates = Q(sources__in=nodes)
        related_nodes = backend.Node.objects.filter(sources | derivates). \
            exclude(id__in=[n.id for n in nodes]).distinct().all()

    graph_data_children = [create_graph_data_node_for_structure_node(n) for n in
                           nodes]
    graph_data_related = [create_graph_data_node_for_structure_node(n) for n in
                          related_nodes]
    data = {'graphDataChildren': graph_data_children,
            'graphDataRelated': graph_data_related}
    return json_response({'loadGraphDataResponse': data})


@ValidPaths("StructureNode", "Argument")
@ViewErrorHandling
def load_text(request, path):
    try:
        # try to load from cache
        t = backend.TextCache.objects.get(path=path.strip().strip('/'))
        paragraphs = json.loads(t.paragraphs)
    except backend.TextCache.DoesNotExist:
        node = assert_node_for_path(path)
        paragraphs = [{'wikiText': "=" + node.title + "=\n" + node.text.text,
                       'path': path,
                       '_node_id': node.id,
                       'authorGroup': [create_user_info(a) for a in
                                       node.text.authors.all()]}]
        for slot in backend.get_ordered_children_for(node):
            favorite = slot.favorite
            paragraphs.append({'wikiText': build_text(favorite, depth=2),
                               'path': path + "/" + slot.title + "." + str(
                                   favorite.get_index(slot)),
                               '_node_id': favorite.id,
                               'authorGroup': [create_user_info(a) for a in
                                               favorite.text.authors.all()]})
            # write to cache
        t = json.dumps(paragraphs)
        backend.TextCache.objects.create(path=path, paragraphs=t)

    for p in paragraphs:
        node = backend.Node.objects.get(id=p['_node_id'])
        p['isFollowing'] = get_is_following(
            request.user.id, node)
        p['isFlagging'] = node.spam_flags.filter(
            user_id=request.user.id).count()
        del p['_node_id']

    return json_response({
        'loadTextResponse': {
            'paragraphs': paragraphs,
            'isFollowing': paragraphs[0]['isFollowing'],
            'isFlagging': paragraphs[0]['isFlagging']}})


@ViewErrorHandling
def load_user_info(request, name):
    user = assert_active_user(name)
    user_info = create_user_info(user)
    return json_response({
        'loadUserInfoResponse': {
            'userInfo': user_info
        }})


@ViewErrorHandling
def load_user_settings(request):
    assert_authentication(request)
    user = User.objects.get(id=request.user.id)
    return json_response({'loadUserSettingsResponse': {
        'userInfo': create_user_info(user),
        'userSettings': create_user_settings(user)
    }})


@ViewErrorHandling
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            django_login(request, user)
            return json_response({
                'loginResponse': {
                    'userInfo': create_user_info(user),
                    'userSettings': create_user_settings(user)
                }})
        else:
            raise DisabledAccount(username)
    else:
        raise InvalidLogin()


def logout(request):
    django_logout(request)
    messages = [
        "Didel dadel dana, ab geht's ins Nirvana.",
        "Mach's gut und danke für den Fisch.",
        "I'll be back!!"
    ]
    m = random.choice(messages)
    return json_response({'logoutResponse': {
        'farewellMessage': m
    }})


@ValidPaths("StructureNode", "Argument")
@ViewErrorHandling
def flag_node(request, path):
    assert_authentication(request)
    assert_permissions(request, ['node_storage.add_spamflag'])
    user = request.user
    node = assert_node_for_path(path)

    marks = node.spam_flags.filter(user=user.id).all()
    if marks.count() == 0:
        new_mark = backend.SpamFlag()
        new_mark.node = node
        new_mark.user_id = request.user.id
        new_mark.save()
        node.update_favorite_for_all_parents()
    return json_response({'markNodeResponse': {}})


@ValidPaths("StructureNode", "Argument")
@ViewErrorHandling
def unflag_node(request, path):
    assert_authentication(request)
    assert_permissions(request, ['node_storage.delete_spamflag'])
    user = request.user
    node = assert_node_for_path(path)

    marks = node.spam_flags.filter(user=user.id).all()
    if marks.count() == 1:
        marks[0].delete()
        node.update_favorite_for_all_parents()
    return json_response({'markNodeResponse': {}})


@ValidPaths("StructureNode", "Argument")
@ViewErrorHandling
def follow_node(request, path):
    assert_authentication(request)
    assert_permissions(request, ['node_storage.add_vote',
                                 'node_storage.change_vote'])
    user = request.user
    node = assert_node_for_path(path)

    marks = node.votes.filter(user=user.id).all()
    if marks.count() >= 1:
        mark = marks[0]
        if mark.head() != node:
            mark.nodes.remove(node)
            new_mark = backend.Vote()
            new_mark.user_id = request.user.id
            new_mark.save()
            new_mark.nodes.add(node)
            for n in traverse_derivates_subset(node, mark.nodes.all()):
                mark.nodes.remove(n)
                new_mark.nodes.add(n)
            mark.save()
            new_mark.save()
            node.update_favorite_for_all_parents()
            for n in traverse_derivates_subset(node, mark.nodes.all()):
                n.update_favorite_for_all_parents()
    else:
        mark = backend.Vote()
        mark.user_id = request.user.id
        mark.save()
        mark.nodes.add(node)
        for n in traverse_derivates(node):
            mark.nodes.add(n)
        mark.save()
        node.update_favorite_for_all_parents()
        for n in traverse_derivates(node):
            n.update_favorite_for_all_parents()
    return json_response({'markNodeResponse': {}})


@ValidPaths("StructureNode", "Argument")
@ViewErrorHandling
def unfollow_node(request, path):
    assert_authentication(request)
    assert_permissions(request, ['node_storage.delete_vote'])
    user = request.user
    node = assert_node_for_path(path)

    marks = node.votes.filter(user=user.id).all()
    if marks.count() > 0:
        mark = marks[0]
        if mark.nodes.count() == 1:
            mark.delete()
            node.update_favorite_for_all_parents()
        else:
            mark.nodes.remove(node)
            for n in traverse_derivates_subset(node, mark.nodes.all()):
                mark.nodes.remove(n)
                n.update_favorite_for_all_parents()
            if mark.nodes.count() == 0:
                mark.delete()
    return json_response({'markNodeResponse': {}})


@ViewErrorHandling
def store_settings(request):
    assert_authentication(request)
    user = User.objects.get(id=request.user.id)
    assert_post_parameters(request, ['description', 'displayName'])
    display_name = request.POST['displayName']
    if display_name != user.username:
        is_available = User.objects.filter(username=display_name).count() == 0
        if not is_available:
            raise UsernameNotAvailable(display_name)
        else:
            user.username = display_name

    user.profile.description = request.POST['description']
    user.save()
    return json_response({'storeSettingsResponse': {}})


@ValidPaths("StructureNode")
@ViewErrorHandling
def store_text(request, path):
    assert_authentication(request)
    assert_permissions(request,
                       ['node_storage.add_node', 'node_storage.add_argument',
                        'node_storage.add_vote', 'node_storage.add_nodeorder',
                        'node_storage.add_derivation', 'node_storage.add_text',
                        'node_storage.change_vote'])
    user = request.user
    assert_post_parameters(request, ['wikiText'])

    if not 'argumentType' in request.POST:
        if 'wikiTextAlternative' in request.POST:
            raise MissingPOSTParameter('argumentType')
            # store new structure node
        _, new_path = store_structure_node(path, request.POST['wikiText'], user)

    elif 'wikiTextAlternative' not in request.POST:
        # store Argument
        new_path = store_argument(path, request.POST['wikiText'],
                                  request.POST['argumentType'], user)

    else:
        # store Argument and Derivate of structure Node
        arg_text = request.POST['wikiText']
        arg_type = request.POST['argumentType']
        derivate_wiki_text = request.POST['wikiTextAlternative']
        new_path = store_derivate(path, arg_text, arg_type, derivate_wiki_text,
                                  user)

    return json_response({'storeTextResponse': {'path': new_path}})


@ViewErrorHandling
def account_registration(request):
    assert_post_parameters(request, ['displayName', 'password', 'emailAddress'])

    emailAddress = request.POST['emailAddress']
    password = request.POST['password']
    displayName = request.POST['displayName']
    try:
        validate_email(emailAddress)
    except ValidationError:
        raise InvalidEmailAddress(emailAddress)

    #Check for already existing Username
    if User.objects.filter(username=displayName).count():
        raise UsernameNotAvailable(displayName)

    #Check for already existing Mail 
    if User.objects.filter(email=emailAddress).count():
        raise EmailAddressNotAvailiable(emailAddress)
    user = create_user(displayName,
                       description="",
                       mail=emailAddress,
                       password=password,
                       groups=['texters', 'voters', 'bloggers'])
    user.is_active = False
    activationKey = random.getrandbits(256)
    user.profile.activationKey = activationKey
    user.save()
    send_mail(settings.REGISTRATION_TITLE,
              settings.REGISTRATION_BODY + ' ' + settings.FINDECO_BASE_URL +
              '/#activate/' + str(activationKey), settings.EMAIL_HOST_USER,
              [emailAddress])

    return json_response({'accountRegistrationResponse': {}})


@ViewErrorHandling
def account_activation(request):
    assert_post_parameters(request, ['activationKey'])
    activationKey = request.POST['activationKey']

    #Check for already existing Username
    if not ((User.objects.filter(
            profile__activationKey__exact=activationKey).filter(
            is_active=False).count()) == 1):
        raise InvalidActivationKey()
    else:
        user = User.objects.get(profile__activationKey__exact=activationKey)

        user.profile.activationKey = ''
        user.is_active = True
        user.save()
    return json_response({'accountActivationResponse': {}})


@ViewErrorHandling
def account_reset_request_by_name(request):
    assert_post_parameters(request, ['displayName'])
    displayName = request.POST['displayName']

    assert_active_user(displayName)

    user = User.objects.get(username=displayName)
    activationKey = random.getrandbits(256)
    user.profile.activationKey = activationKey
    user.save()
    send_mail(settings.REGISTRATION_RECOVERY_TITLE,
              settings.REGISTRATION_RECOVERY_BODY + ' ' +
              settings.FINDECO_BASE_URL + '/#confirm/' + str(activationKey),
              settings.EMAIL_HOST_USER,
              [user.email])

    return json_response({'accountResetRequestByNameResponse': {}})


@ViewErrorHandling
def account_reset_request_by_mail(request):
    assert_post_parameters(request, ['emailAddress'])
    emailAddress = request.POST['emailAddress']

    #Check for activated User with displayname
    if not ((User.objects.filter(email=emailAddress).filter(
            is_active=True).filter(
            profile__activationKey__exact='').count()) == 1):
        return json_error_response('UnknownUser', emailAddress)

    user = User.objects.get(email=emailAddress)
    activationKey = random.getrandbits(256)
    user.profile.activationKey = activationKey
    user.save()
    send_mail(settings.REGISTRATION_RECOVERY_TITLE,
              settings.REGISTRATION_RECOVERY_BODY + ' ' +
              settings.FINDECO_BASE_URL + '/#confirm/' + str(activationKey),
              settings.EMAIL_HOST_USER,
              [user.email])

    return json_response({'accountResetRequestByMailResponse': {}})


@ViewErrorHandling
def account_reset_confirmation(request):
    assert_post_parameters(request, ['activationKey'])
    activationKey = request.POST['activationKey']

    #Check for already existing Username
    if not ((User.objects.filter(
            profile__activationKey__exact=activationKey).filter(
            is_active=True).count()) == 1):
        raise InvalidActivationKey()
    else:
        user = User.objects.get(profile__activationKey__exact=activationKey)
        user.profile.activationKey = ''
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()
        send_mail(settings.REGISTRATION_RECOVERY_TITLE_SUCCESS,
                  settings.REGISTRATION_RECOVERY_BODY_SUCCESS + ' Password : ' +
                  str(password), settings.EMAIL_HOST_USER,
                  [user.email])
    return json_response({'accountResetConfirmationResponse': {}})


@ViewErrorHandling
def error_404(request):
    raise InvalidURL()