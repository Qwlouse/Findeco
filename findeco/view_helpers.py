#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
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
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import division, print_function, unicode_literals
import json
import functools
import re
from django.contrib.auth.models import Permission, User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q
from django.http import HttpResponse

from .api_validation import USERNAME
from .api_validation import validate_response
from .error_handling import *
from .paths import parse_suffix
import node_storage as backend
from node_storage import get_node_for_path, get_ordered_children_for, parse
from node_storage import create_structure_from_structure_node_schema
from node_storage.factory import create_argument, create_vote
from node_storage.factory import create_structureNode, create_slot
from node_storage.models import Argument
from node_storage.path_helpers import get_good_path_for_structure_node
from node_storage.structure_parser import turn_into_valid_short_title


def json_response(data):
    return HttpResponse(json.dumps(data),
                        mimetype='application/json')


def ValidPaths(*allowed_path_types):
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(request, path, *args, **kwargs):
            _, path_type = parse_suffix(path)

            if 'arg_id' in path_type:
                path_type = 'Argument'
            elif 'arg_type' in path_type:
                path_type = 'ArgumentCategory'
            elif 'slot' in path_type:
                path_type = 'Slot'
            else:
                path_type = 'StructureNode'
            if path_type not in allowed_path_types:
                return json_error_response('_IllegalPath', path)
                #noinspection PyCallingNonCallable
            response = f(request, path, *args, **kwargs)
            validate_response(response.content, f.__name__)
            return response

        return wrapped

    return wrapper


def assert_node_for_path(path):
    try:
        node = backend.get_node_for_path(path)
    except backend.IllegalPath:
        raise UnknownNode(path)
    return node


def assert_authentication(request):
    if not request.user.is_authenticated():
        raise NotAuthenticated()


def assert_active_user(username=None, email=None):
    assert username or email
    if username:
        users = User.objects.filter(username__iexact=username)
    else:
        users = User.objects.filter(email__iexact=email)

    if not users.count() == 1:
        raise UnknownUser(username or email)
    user = users[0]
    if not user.is_active:
        raise UnknownUser(username or email)

    return user


def assert_permissions(request, permissions):
    assert isinstance(permissions, list)
    for p in permissions:
        if not request.user.has_perm(p):
            raise PermissionDenied()


def assert_post_parameters(request, parameters):
    for p in parameters:
        if not p in request.POST:
            raise MissingPOSTParameter(p)


def get_index_nodes_for_path(path):
    path = path.strip().strip('/')
    try:  # to get from cache
        index_cache = backend.IndexCache.objects.get(path=path)
        index_nodes = json.loads(index_cache.index_nodes)
    except backend.IndexCache.DoesNotExist:
        node = assert_node_for_path(path)
        slot_list = backend.get_ordered_children_for(node)
        index_nodes = [create_index_node_for_slot(slot) for slot in slot_list]
        # write to cache
        index_cache = json.dumps(index_nodes)
        backend.IndexCache.objects.create(path=path, index_nodes=index_cache)
    return index_nodes


def create_user_info(user):
    user_info = dict(
        displayName=user.username,
        description=user.profile.description,
    )
    return user_info


def create_user_settings(user):
    rights = 0
    if user.groups.filter(name='texters').count() > 0:
        rights += 1
    if user.groups.filter(name='voters').count() > 0:
        rights += 2
    if user.is_superuser:
        rights += 4
    user_settings = dict(
        followers=[{'displayName': u.user.username} for u in
                   user.profile.followers.all()],
        followees=[{'displayName': u.user.username} for u in
                   user.profile.followees.all()],
        blockedUsers=[{'displayName': u.user.username} for u in
                      user.profile.blocked.all()],
        userRights=rights,
        email=user.email
    )
    return user_settings


def create_index_node_for_slot(slot):
    favorite = slot.favorite
    index_node = dict(
        shortTitle=slot.title,
        fullTitle=favorite.title,
        index=favorite.get_index(slot),
        authorGroup=[create_user_info(a) for a in favorite.text.authors.all()]
    )
    return index_node


def create_index_node_for_argument(argument, user_id):
    index_node = dict(
        argType=Argument.long_arg_type(argument.arg_type),
        fullTitle=argument.title,
        index=argument.index,
        authorGroup=[create_user_info(a) for a in argument.text.authors.all()],
        isFollowing=get_is_following(user_id, argument),
        isFlagging=get_is_flagging(user_id, argument)
    )
    return index_node


def create_paragraph_for_node(node, path, depth=1):
    depth = max(min(depth, 6), 1)
    markup = "=" * depth
    if depth == 1:
        text_pattern = "{markup} {title} {markup}\n{text}"
    else:
        text_pattern = "{markup} [[#/{path}|{title}]] {markup}\n{text}"

    text = text_pattern.format(
        markup=markup,
        path=node.get_a_path(),
        title=node.title,
        text=node.text.text
    )
    return {
        'wikiText': text,
        'path': path,
        '_node_id': node.id,
        'authorGroup': [create_user_info(a) for a in node.text.authors.all()]}


def create_paragraph_list_for_node(node, path, depth=1):
    paragraphs = [create_paragraph_for_node(node, path, depth=depth)]
    for slot in backend.get_ordered_children_for(node):
        favorite = slot.favorite
        slot_path = path + "/" + slot.title
        fav_path = get_good_path_for_structure_node(favorite, slot, slot_path)
        paragraphs += create_paragraph_list_for_node(favorite,
                                                     fav_path,
                                                     depth=depth + 1)
    return paragraphs


def create_graph_data_node_for_structure_node(node, slot=None, path=None,
                                              slot_path=None, title=None):
    if slot_path:
        slot = get_node_for_path(slot_path)

    if not path:
        path = get_good_path_for_structure_node(node, slot, slot_path)

    if slot:
        if not slot_path:
            slot_path = slot.get_a_path()
        origin_group = [slot_path + '.' + str(n.get_index(slot)) for n in
                        node.sources.filter(parents__in=[slot]).all()]
        origin_group += [n.get_a_path() for n in
                         node.sources.exclude(parents__in=[slot]).all()]
    else:
        origin_group = [n.get_a_path() for n in node.sources.all()]

    graph_data_node = dict(
        path=path,
        authorGroup=[create_user_info(a) for a in node.text.authors.all()],
        follows=node.votes.count(),
        spamFlags=node.spam_flags.count(),
        unFollows=node.get_unfollows(),
        newFollows=node.get_newfollows(),
        title=node.title,
        originGroup=[o.rstrip('/') for o in origin_group]
    )
    return graph_data_node


def store_structure_node(path, wiki_text, author):
    slot_path = path.rsplit('.', 1)[0]
    slot = get_node_for_path(slot_path)
    structure = backend.parse(wiki_text, None)
    structure_node = backend.create_structure_from_structure_node_schema(
        structure, slot, [author])
    # add auto follow
    create_vote(author, [structure_node])
    return structure_node, get_good_path_for_structure_node(structure_node,
                                                            slot, slot_path)


def store_argument(path, arg_text, arg_type, author):
    node = get_node_for_path(path)
    title, arg_text = backend.split_title_from_text(arg_text)
    original_argument = create_argument(node, arg_type, title, arg_text,
                                        [author])
    # add auto follow
    create_vote(author, [original_argument])
    # copy argument for all derivates
    for d in node.traverse_derivates():
        new_argument = create_argument(d, arg_type, title, arg_text, [author])
        original_argument.add_derivate(new_argument)
    return path + "." + arg_type + "." + str(node.arguments.count())


def store_derivate(path, arg_text, arg_type, derivate_wiki_text, author):
    new_node, new_path = store_structure_node(path, derivate_wiki_text, author)
    node = get_node_for_path(path)
    arg_title, arg_text = backend.split_title_from_text(arg_text)
    arg = node.add_derivate(new_node, arg_type=arg_type,
                            title=arg_title,
                            text=arg_text, authors=[author])
    # add auto follow
    create_vote(author, [arg])
    return new_path


def fork_node_and_add_slot(path, user, wikiText):
    source_node = assert_node_for_path(path)
    authors = list(source_node.text.authors.all()) + [user]
    title = source_node.title
    # create fork
    fork = create_structureNode(title,
                                source_node.text.text,
                                authors)
    parent_slot_path = path.rsplit('.', 1)[0]
    parent_slot = get_node_for_path(parent_slot_path)
    parent_slot.append_child(fork)
    fork_path = parent_slot_path + '.' + str(fork.get_index(parent_slot))
    short_titles = set()
    for slot in get_ordered_children_for(source_node):
        fork.append_child(slot)
        short_titles.add(slot.title)
    # create new slot plus node
    schema = parse(wikiText, 'foo')
    short_title = turn_into_valid_short_title(schema['title'], short_titles)
    new_slot = create_slot(short_title)
    fork.append_child(new_slot)
    node = create_structure_from_structure_node_schema(schema, new_slot, [user])
    arg_title = "Abschnitt über '{0}' fehlt.".format(schema['title'])
    source_node.add_derivate(fork, 'con', arg_title, authors=[user])
    # auto follow
    follow_node(fork, user.id)
    follow_node(node, user.id)
    return fork_path


def get_permission(name):
    a, _, n = name.partition('.')
    return Permission.objects.get(content_type__app_label=a, codename=n)


def get_is_following(user_id, node):
    isFollowing = 0
    v = node.votes.filter(user=user_id)
    if v.count() > 0:
        v = v[0]
        isFollowing = 1  # at least transitive follow
        if v.nodes.order_by('id')[0].id == node.id:
            isFollowing = 2  # explicit follow
    return isFollowing


def get_is_flagging(user_id, node):
    return node.spam_flags.filter(user_id=user_id).count()


def follow_node(node, user_id):
    marks = node.votes.filter(user=user_id).all()
    if marks.count() >= 1:
        mark = marks[0]
        if mark.head() != node:
            mark.nodes.remove(node)
            new_mark = backend.Vote()
            new_mark.user_id = user_id
            new_mark.save()
            new_mark.nodes.add(node)
            for n in node.traverse_derivates(subset=mark.nodes.all()):
                mark.nodes.remove(n)
                new_mark.nodes.add(n)
            mark.save()
            new_mark.save()
            node.update_favorite_for_all_parents()
            for n in node.traverse_derivates(subset=mark.nodes.all()):
                n.update_favorite_for_all_parents()
    else:
        mark = backend.Vote()
        mark.user_id = user_id
        mark.save()
        mark.nodes.add(node)
        for n in node.traverse_derivates(condition=lambda n: n.votes.filter(
                user=user_id).all().count() == 0):
            mark.nodes.add(n)
        mark.save()
        node.update_favorite_for_all_parents()
        for n in node.traverse_derivates(condition=lambda n: n.votes.filter(
                user=user_id).all().count() == 0):
            n.update_favorite_for_all_parents()


def unfollow_node(node, user_id):
    marks = node.votes.filter(user=user_id).all()
    if marks.count() > 0:
        mark = marks[0]
        if mark.nodes.count() == 1:
            mark.delete()
            node.update_favorite_for_all_parents()
        else:
            mark.nodes.remove(node)
            for n in node.traverse_derivates(subset=mark.nodes.all()):
                mark.nodes.remove(n)
                n.update_favorite_for_all_parents()
            if mark.nodes.count() == 0:
                mark.delete()


def normalize_query(query_string):
    """
    Splits the query string in invidual keywords, getting rid of unecessary
    spaces and grouping quoted words together.
    Example:
    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
    ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    """
    findterms = re.compile(r'"([^"]+)"|(\S+)').findall
    normspace = re.compile(r'\s{2,}').sub
    return [normspace(' ', (t[0] or t[1]).strip())
            for t in findterms(query_string)]


def get_query(query_string, search_fields):
    """
    Returns a query, that is a combination of Q objects. That combination aims
    to search keywords within a model by testing the given search fields.
    """
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query &= or_query
    return query


def change_authorship_to(old_user, new_user):
    """
    Queries all content and removes old_user from author lists. If new_user is
    not already in the author list he will
    be added. This will be used mostly with new_user being the anonymous user.
    """
    # Changing authorship in texts
    for text in old_user.author_in.all():
        text.authors.remove(old_user)
        if not new_user in text.authors.all():
            text.authors.add(new_user)
        text.save()
    # Changing authorship in microblogging
    for post in old_user.microblogging_posts.all():
        post.author = new_user
        post.save()


def check_username_sanity(username):
    if re.match(USERNAME + "$", username):
        return True
    else:
        return False


def assert_valid_email(email):
    try:
        validate_email(email)
    except ValidationError:
        raise InvalidEmailAddress()