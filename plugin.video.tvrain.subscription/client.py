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

import cookielib
import json
import urllib
import urllib2

__author__ = 'Oleg Larin'

class TvRainClient(object):
    class ClientError(Exception):
        pass

    ERROR_PAGE_NOT_FOUND = "32043"
    ERROR_PAGE_FORBIDEN = "32042"
    ERROR_NO_SUBSCRIPTION = "32045"
    ERROR_EMPTY_CREDENTIALS = "32044"

    def __init__(self, plugin):
        self.plugin = plugin
        self.streams_url = "https://api.tvrain.ru/api_v2/live/"
        self.login_url = "https://tvrain.ru/login/"

    def get_feed(self):
        opener = self.get_opener()
        try:
            response = opener.open(self.streams_url)
        except urllib2.HTTPError, err:
            if err.code == 404:
                error_msg = self.plugin.get_string(self.ERROR_PAGE_NOT_FOUND)
            elif err.code == 403:
                error_msg = self.plugin.get_string(self.ERROR_PAGE_FORBIDEN)
            elif err.code == 402:
                error_msg = self.plugin.get_string(self.ERROR_NO_SUBSCRIPTION)
            else:
                error_msg = "Unknown remote server error. Error code %s" % err.code
            raise self.ClientError(error_msg)
        data = json.loads(response.read())
        return data

    def get_opener(self):
        cookie_jar = cookielib.MozillaCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
        opener.addheaders = [('X-User-Agent', 'TV Client (Browser); API_CONSUMER_KEY=a908545f-80af-4f99-8dac-fb012cec'),
                             ('Accept', 'application/tvrain.api.2.8+json'),
                             ('Accept-Language', 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'),
                             ('Accept-Charset', 'utf-8, utf-16, *;q=0.1'),
                             ('Accept-Encoding', 'plain'),
                             ('X-Result-Define-Thumb-Width', '200'),
                             ('X-Result-Define-Thumb-height', '110'),
                             ('Connection', 'keep-alive'),
                             ('Origin', 'http://tvrain.ru'),
                             ('Referer', 'http://tvrain.ru/')]

        opener.open(self.login_url)

        csrf_token = [x.value for x in cookie_jar
                      if x.name == "YII_CSRF_TOKEN"][0]

        email = self.plugin.get_setting("email")
        password = self.plugin.get_setting("password")
        if not (len(email) and len(password)):
            raise self.ClientError(self.plugin.get_string(
                self.ERROR_EMPTY_CREDENTIALS))

        credentials = {"User[email]": email,
                       "User[password]": password,
                       "YII_CSRF_TOKEN": csrf_token,
                       "yt0": "Войти"}

        login_data = urllib.urlencode(credentials)
        opener.open(self.login_url, login_data)
        return opener
