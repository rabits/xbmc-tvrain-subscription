# coding=utf-8
#
#   Copyright (c) 2014 Oleg Larin, E-mail: oleg.larin@gmail.com
#
#   This Program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2, or (at your option)
#   any later version.
#
#   This Program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; see the file COPYING.  If not, write to
#   the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#   http://www.gnu.org/licenses/gpl.html

from xbmcswift2 import Plugin
from xbmcswift2 import xbmcgui
from client import TvRainClient

__author__ = 'Oleg Larin'

plugin = Plugin()

def display_error(message, title=None):
    if not title:
        title = plugin.get_string("32046")
    dialog = xbmcgui.Dialog()
    dialog.ok(title, message)

@plugin.cached(TTL=60*24)
def get_api_data():
    client = TvRainClient(plugin)
    data = list()
    try:
        data = client.get_feed()
    except client.ClientError, err:
        display_error(unicode(err))
    return data

@plugin.route('/')
def index():
    items = list()
    api_response = get_api_data()

    if api_response:
        for item in api_response["video"]["RTMP"]:
            items.append(dict(label=item["label"], path=item["url"],
                              is_playable=True))
    return items


if __name__ == '__main__':
    plugin.run()
