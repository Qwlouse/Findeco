#!/usr/bin/python
# coding=utf-8
# This file is part of the Naga library published under the GPL3 license.
# Copyright (C) 2012  Klaus Greff
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


########################### Test the API calls #################################
valid_routes = [
    #### loadUserSettings
    dict(url='/.json_loadUserSettings',
        view_name='codebar.views.load_user_settings'),

    #### loadIndex
    dict(url='/.json_loadIndex/some.1/path.2',
        view_name='codebar.views.load_index',
        kwargs=dict(path='/some.1/path.2', arguments='')),

    dict(url='/.json_loadIndex/some.1/path.2.pro',
        view_name='codebar.views.load_index',
        kwargs=dict(path='/some.1/path.2', arguments='pro')),

    dict(url='/.json_loadIndex/some.1/path.2.neut',
        view_name='codebar.views.load_index',
        kwargs=dict(path='/some.1/path.2', arguments='neut')),

    dict(url='/.json_loadIndex/some.1/path.2.con',
        view_name='codebar.views.load_index',
        kwargs=dict(path='/some.1/path.2', arguments='con')),

    ]