#!/usr/bin/env python3
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
# #############################################################################
# Copyright (c) 2015 Klaus Greff <klaus.greff@gmx.net>,
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
# #############################################################################
#
##############################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# endregion ###################################################################

import random

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.core.mail import send_mail
from django.db.models import Count
from django.utils.html import escape
from django.utils.translation import ugettext
from django.views.decorators.csrf import ensure_csrf_cookie
from findeco.project_path import project_path
from findeco.search_tools import get_search_query

from .view_helpers import *
from microblogging import search_for_microblogging
from microblogging.system_messages import (
    post_node_was_flagged_message, post_new_derivate_for_node_message,
    post_new_argument_for_node_message, post_node_was_unflagged_message)
from findeco.models import (UserProfile, Activation, PasswordRecovery,
                            EmailActivation)
import node_storage as backend
from node_storage.factory import create_user


# ################### General stuff ###########################################
@ensure_csrf_cookie
def home(request):
    with open(project_path("static/index.html"), 'r') as index_html_file:
        return HttpResponse(index_html_file.read(), content_type='text/html')


def jasmine(request):
    with open(project_path("static/jasmine.html"), 'r') as index_html_file:
        return HttpResponse(index_html_file.read(), content_type='text/html')


@ViewErrorHandling
def error_404(request):
    raise InvalidURL()


@ViewErrorHandling
def search(request, search_fields, search_string):
    things_to_search_for = set(search_fields.split('_'))

    user_results = []
    if 'user' in things_to_search_for:
        exact_username_matches = User.objects.filter(
            username__iexact=search_string.strip())
        for user in exact_username_matches:
            user_results.append({"url": "user/" + user.username,
                                 "title": user.username,
                                 "snippet": "Profil von " + user.username})
        user_query = get_search_query(search_string, ['first_name',
                                                      'last_name'])
        found_users = User.objects.filter(user_query)
        for user in found_users:
            user_results.append({"url": "user/" + user.username,
                                 "title": user.username,
                                 "snippet": "Profil von " + user.username})
        user_query = get_search_query(search_string, ['description', ])
        found_profiles = UserProfile.objects.filter(user_query)
        for profile in found_profiles:
            user_results.append({
                "url": "user/" + profile.user.username,
                "title": profile.user.username,
                "snippet": profile.description[:min(len(profile.description),
                                                    140)]})
    content_results = []
    if 'content' in things_to_search_for:
        node_query = get_search_query(search_string, ['title', ])
        found_titles = backend.Node.objects.filter(node_query).exclude(
            node_type=backend.Node.SLOT).order_by("-id")
        for node in found_titles:
            content_results.append({
                "url": node.get_a_path(),
                "title": node.title,
                "snippet": node.text.text[:min(len(node.text.text), 140)]})
        text_query = get_search_query(search_string, ['text', ])
        found_texts = backend.Text.objects.filter(text_query).order_by("-id")
        for text_node in found_texts:
            content_results.append({
                "url": text_node.node.get_a_path(),
                "title": text_node.node.title,
                "snippet": text_node.text[:min(len(text_node.text), 140)]})
    microblogging_results = []
    if 'microblogging' in things_to_search_for:
        microblogging_results = search_for_microblogging(search_string)

    return json_response(
        {'searchResponse': {'userResults': user_results,
                            'contentResults': content_results,
                            'microbloggingResults': microblogging_results}})


# ################### Node Infos ##############################################
@ValidPaths("StructureNode")
@ViewErrorHandling
def load_index(request, path):
    return json_response({'loadIndexResponse': get_index_nodes_for_path(path)})


@ValidPaths("StructureNode")
@ViewErrorHandling
def load_argument_index(request, path):
    prefix, path_type = parse_suffix(path)
    node = assert_node_for_path(prefix)
    data = [create_index_node_for_argument(a, request.user.id) for a in
            node.arguments.annotate(num_follows=Count('votes')).
            order_by('-num_follows')]
    return json_response({'loadArgumentIndexResponse': data})


@ValidPaths("StructureNode", "Argument")
@ViewErrorHandling
def load_node(request, path):
    node = assert_node_for_path(path)
    index_nodes = get_index_nodes_for_path(path)

    return json_response({'loadNodeResponse': {
        'fullTitle': node.title,
        'nodeID': node.pk,
        'isFollowing': get_is_following(request.user.id, node),
        'isFlagging': get_is_flagging(request.user.id, node),
        'wikiText': node.text.text,
        'authors': [author.username for author in node.text.authors.all()],
        'indexList': index_nodes
    }})


@ValidPaths("StructureNode")
@ViewErrorHandling
def load_graph_data(request, path, graph_data_type):
    if not path.strip('/'):  # root node!
        nodes = [backend.get_root_node()]
        # related_nodes = []
    else:
        slot_path = path.rsplit('.', 1)[0]
        slot = assert_node_for_path(slot_path)
        if graph_data_type == "withSpam":
            # This means display ALL nodes
            nodes = backend.get_ordered_children_for(slot)
        else:  # if graph_data_type == 'full':
            nodes = backend.Node.objects.filter(parents=slot)\
                .annotate(spam_count=Count('spam_flags', distinct=True))\
                .filter(spam_count__lt=2)\
                .filter(votes__isnull=False)

        current_node = backend.get_node_for_path(path)
        nodes = list(nodes)
        if current_node not in nodes:
            nodes.append(current_node)

    graph_data_children = map(create_graph_data_node_for_structure_node, nodes)
    data = {'graphDataChildren': graph_data_children,
            'graphDataRelated': []}
    return json_response({'loadGraphDataResponse': data})


@ValidPaths("StructureNode", "Argument")
@ViewErrorHandling
def load_text(request, path):
    path = path.strip().strip('/')
    try:
        # try to load from cache
        t = backend.TextCache.objects.get(path=path)
        paragraphs = json.loads(t.paragraphs)
    except backend.TextCache.DoesNotExist:
        node = assert_node_for_path(path)
        paragraphs = create_paragraph_list_for_node(node, path, depth=2)
        # write to cache
        t = json.dumps(paragraphs)
        backend.TextCache.objects.create(path=path, paragraphs=t)

    for p in paragraphs:
        node = backend.Node.objects.get(id=p['_node_id'])
        p['isFollowing'] = get_is_following(request.user.id, node)
        p['isFlagging'] = get_is_flagging(request.user.id, node)
        del p['_node_id']

    return json_response({
        'loadTextResponse': {
            'paragraphs': paragraphs,
            'isFollowing': paragraphs[0]['isFollowing'],
            'isFlagging': paragraphs[0]['isFlagging']}})


@ViewErrorHandling
def load_argument_news(request):
    cards = []
    for argument in Argument.objects.filter(sources__isnull=True)\
                            .order_by("-id")[:20]:
        node = argument.concerns
        cards.append({
            'argument': {
                'text': argument.text.text,
                'fullTitle': argument.title,
                'path': argument.get_a_path(),
                'isFollowing': get_is_following(request.user.id, argument),
                'followingCount': argument.votes.count(),
                'isFlagging': get_is_flagging(request.user.id, argument),
                'flaggingCount': argument.spam_flags.count(),
                'authorGroup': [author.username
                                for author in argument.text.authors.all()],
                'type': argument.arg_type
            },
            'node': {
                'text': node.text.text,
                'fullTitle': node.title,
                'path': node.get_a_path(),
                'isFollowing': get_is_following(request.user.id, node),
                'followingCount': node.votes.count(),
                'isFlagging': get_is_flagging(request.user.id, node),
                'flaggingCount': node.spam_flags.count(),
                'authorGroup': [author.username
                                for author in node.text.authors.all()]
            }
        })

    return json_response({'loadArgumentNewsResponse': cards})


# ##################### Store/Modify Nodes ####################################
@ValidPaths("StructureNode")
@ViewErrorHandling
def store_proposal(request, path):
    assert_authentication(request)
    assert_permissions(request,
                       ['node_storage.add_node', 'node_storage.add_vote',
                        'node_storage.add_nodeorder', 'node_storage.add_text',
                        'node_storage.change_vote'])
    user = request.user
    p = json.loads(request.body)

    slot_path = path.rsplit('.', 1)[0]
    slot = get_node_for_path(slot_path)
    proposal_node = generate_proposal_node_with_subsections(slot,
                                                            p['proposal'],
                                                            user)

    new_path = get_good_path_for_structure_node(proposal_node, slot, slot_path)
    return json_response({'storeProposalResponse': {'path': new_path}})


@ValidPaths("StructureNode")
@ViewErrorHandling
def store_refinement(request, path):
    assert_authentication(request)
    assert_permissions(request,
                       ['node_storage.add_node', 'node_storage.add_argument',
                        'node_storage.add_vote', 'node_storage.add_nodeorder',
                        'node_storage.add_derivation', 'node_storage.add_text',
                        'node_storage.change_vote'])
    user = request.user
    p = json.loads(request.body)

    origin = get_node_for_path(path)
    slot_path = path.rsplit('.', 1)[0]
    slot = get_node_for_path(slot_path)

    derivate = generate_refinement(origin, p['proposal'], p['argument'], slot,
                                   user)

    new_path = get_good_path_for_structure_node(derivate, slot, slot_path)

    # microblog alert
    post_new_derivate_for_node_message(user, path, new_path)

    return json_response({'storeRefinementResponse': {'path': new_path}})


@ValidPaths("StructureNode")
@ViewErrorHandling
def store_argument(request, path):
    assert_authentication(request)
    assert_permissions(request,
                       ['node_storage.add_node', 'node_storage.add_argument',
                        'node_storage.add_vote', 'node_storage.add_nodeorder',
                        'node_storage.add_text', 'node_storage.change_vote'])
    user = request.user
    p = json.loads(request.body)

    node = get_node_for_path(path)
    title = p['argument']['title']
    text = p['argument']['text']
    arg_type = p['argument']['type']
    arg = create_argument(node, arg_type=arg_type, title=title, text=text,
                          authors=[user])
    create_vote(user, [arg])  # auto-follow
    new_path = "{path}.{arg_type}.{index}".format(
        path=path, arg_type=arg_type, index=arg.index)

    # microblog alert
    post_new_argument_for_node_message(user, path, p['argument']['type'],
                                       new_path)
    return json_response({'storeArgumentResponse': {'path': new_path}})


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

    # microblog alert
    post_node_was_flagged_message(path, user)
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

    # microblog alert
    post_node_was_unflagged_message(path, user)
    return json_response({'markNodeResponse': {}})


@ValidPaths("StructureNode", "Argument")
@ViewErrorHandling
def mark_node_follow(request, path):
    assert_authentication(request)
    assert_permissions(request, ['node_storage.add_vote',
                                 'node_storage.change_vote'])
    node = assert_node_for_path(path)

    follow_node(node, request.user.id)
    return json_response({'markNodeResponse': {}})


@ValidPaths("StructureNode", "Argument")
@ViewErrorHandling
def mark_node_unfollow(request, path):
    assert_authentication(request)
    assert_permissions(request, ['node_storage.delete_vote'])
    node = assert_node_for_path(path)

    unfollow_node(node, request.user.id)
    return json_response({'markNodeResponse': {}})


# ################### User Infos ##########################################
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


# ################### User Interactions #######################################
@ViewErrorHandling
def login(request):
    request_data = json.loads(request.body)
    username = request_data['username']
    password = request_data['password']
    if not username or not password:
        raise InvalidLogin()
    user = assert_active_user(username)
    user = authenticate(username=user.username, password=password)
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


@ViewErrorHandling
def store_settings(request):
    assert_authentication(request)
    request_data = json.loads(request.body)
    user = User.objects.get(id=request.user.id)
    assert_request_data_parameters(request_data, ['description',
                                                  'displayName'])
    if check_username_sanity(request_data['displayName']):
        display_name = request_data['displayName']
    else:
        raise InvalidUsername(request_data['displayName'])
    if display_name != user.username:
        try:
            u = User.objects.get(username__iexact=display_name)
            if u != user:
                raise UsernameNotAvailable(display_name)
        except User.DoesNotExist:
            pass
        user.username = display_name

    user.profile.description = escape(request_data['description'])
    email = request_data['email']
    if email != user.email:
        assert_valid_email(email)
        eact = EmailActivation.create(user, email)
        try:
            confirm_url = settings.FINDECO_BASE_URL + '/confirm_email/' + \
                str(eact.key)
            send_mail(ugettext('mail_verification_email_subject'),
                      ugettext('mail_verification_email_body{url}').format(
                      url=confirm_url),
                      settings.EMAIL_HOST_USER,
                      [email],
                      fail_silently=False)
        except SMTPException:
            # This means we can't send mails, so we can't change the mail
            eact.delete()
            raise
    if 'wantsMailNotification' in request_data:
        wants = request_data['wantsMailNotification']
        if isinstance(wants, str):
            wants = wants.lower() == 'true'
        user.profile.wants_mail_notification = wants

    if 'helpEnabled' in request_data:
        user.profile.help_enabled = request_data['helpEnabled']

    if 'preferredLanguage' in request_data:
        user.profile.preferred_language = request_data['preferredLanguage']

    user.save()
    return json_response({'storeSettingsResponse': {}})


@ViewErrorHandling
def mark_user_follow(request, name):
    assert_authentication(request)
    user = request.user
    followee = assert_active_user(username=name)
    user.profile.followees.add(followee.profile)
    return json_response({'markUserResponse': {
        'followees': [{'displayName': u.user.username}
                      for u in user.profile.followees.all()]}})


@ViewErrorHandling
def mark_user_unfollow(request, name):
    followee = assert_active_user(username=name)
    user = request.user
    user.profile.followees.remove(followee.profile)
    return json_response({'markUserResponse': {
        'followees': [{'displayName': u.user.username}
                      for u in user.profile.followees.all()]}})


@ViewErrorHandling
def change_password(request):
    assert_authentication(request)
    user = User.objects.get(id=request.user.id)
    user.set_password(json.loads(request.body)['password'])
    user.save()
    return json_response({'changePasswordResponse': {}})


@ViewErrorHandling
def delete_user(request):
    assert_authentication(request)
    user = User.objects.get(id=request.user.id)
    anonymous = User.objects.filter(username='anonymous').all()[0]
    # prevent cascading deletion of objects with foreign key to this user by
    # changing this foreign key to anonymous
    change_authorship_to(user, anonymous)
    # delete the user
    user.delete()
    return json_response({'deleteUserResponse': {}})


# ###################### Registration #########################################
@ViewErrorHandling
def account_registration(request):
    request_data = json.loads(request.body)
    assert_request_data_parameters(request_data, ['displayName', 'password',
                                                  'emailAddress'])

    email_address = request_data['emailAddress']
    password = request_data['password']
    if check_username_sanity(request_data['displayName']):
        display_name = request_data['displayName']
    else:
        raise InvalidUsername(request_data['displayName'])

    assert_valid_email(email_address)

    # validate username
    if not check_username_sanity(display_name):
        raise InvalidUsername(display_name)

    # Check for already existing Username
    if User.objects.filter(username__iexact=display_name).count():
        raise UsernameNotAvailable(display_name)

    # Check for already existing Mail
    if User.objects.filter(email__iexact=email_address).count():
        raise EmailAddressNotAvailable(email_address)

    user = create_user(display_name,
                       description="",
                       mail=email_address,
                       password=password,
                       groups=['texters', 'voters', 'bloggers'])
    user.is_active = False
    user.save()
    activation = Activation.create(user)
    try:
        activation_url = settings.FINDECO_BASE_URL + '/activate/' + \
            str(activation.key)
        send_mail(ugettext('registration_email_subject'),
                  ugettext('registration_email_body{url}').format(
                      url=activation_url),
                  settings.EMAIL_HOST_USER,
                  [email_address],
                  fail_silently=False)
    except SMTPException:
        # This means we can't send mails, so we can't create users
        user.delete()
        activation.delete()
        raise

    return json_response({'accountRegistrationResponse': {}})


@ViewErrorHandling
def account_activation(request):
    request_data = json.loads(request.body)
    assert_request_data_parameters(request_data, ['activationKey'])
    activation_key = request_data['activationKey']
    try:
        act = Activation.objects.get(key=activation_key)
        act.resolve()
        return json_response({'accountActivationResponse': {}})
    except Activation.DoesNotExist:
        raise InvalidActivationKey()


@ViewErrorHandling
def account_reset_request_by_name(request):
    request_data = json.loads(request.body)
    assert_request_data_parameters(request_data, ['displayName'])
    display_name = request_data['displayName']

    user = assert_active_user(display_name)
    recovery = PasswordRecovery.create(user)
    try:
        recovery_url = settings.FINDECO_BASE_URL + '/confirm/' + \
            str(recovery.key)

        send_mail(ugettext('password_recovery_email_subject'),
                  ugettext('password_recovery_email_body{url}').format(
                      url=recovery_url),
                  settings.EMAIL_HOST_USER,
                  [user.email])

        return json_response({'accountResetRequestByNameResponse': {}})
    except SMTPException:
        recovery.delete()
        raise


@ViewErrorHandling
def account_reset_request_by_mail(request):
    request_data = json.loads(request.body)
    assert_request_data_parameters(request_data, ['emailAddress'])
    email_address = request_data['emailAddress']
    user = assert_active_user(email=email_address)
    recovery = PasswordRecovery.create(user)
    try:
        recovery_url = settings.FINDECO_BASE_URL + '/confirm/' + \
            str(recovery.key)
        send_mail(ugettext('password_recovery_email_subject'),
                  ugettext('password_recovery_email_body{url}').format(
                      url=recovery_url),
                  settings.EMAIL_HOST_USER,
                  [user.email])

        return json_response({'accountResetRequestByMailResponse': {}})
    except SMTPException:
        recovery.delete()
        raise


@ViewErrorHandling
def account_reset_confirmation(request):
    request_data = json.loads(request.body)
    assert_request_data_parameters(request_data, ['activationKey'])
    recovery_key = request_data['activationKey']
    try:
        rec = PasswordRecovery.objects.get(key=recovery_key)
        new_password = rec.resolve()
        send_mail(ugettext('password_recovery_success_email_subject'),
                  ugettext('password_recovery_success_email_body{password}'
                           ).format(password=str(new_password)),
                  settings.EMAIL_HOST_USER,
                  [rec.user.email])
        return json_response({'accountResetConfirmationResponse': {}})
    except PasswordRecovery.DoesNotExist:
        raise InvalidRecoveryKey()


@ViewErrorHandling
def email_change_confirmation(request):
    request_data = json.loads(request.body)
    assert_request_data_parameters(request_data, ['activationKey'])
    email_verify_key = request_data['activationKey']
    try:
        eac = EmailActivation.objects.get(key=email_verify_key)
        eac.resolve()
        return json_response({'accountResetConfirmationResponse': {}})
    except Activation.DoesNotExist:
        raise InvalidRecoveryKey()
