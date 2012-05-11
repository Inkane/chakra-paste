#!/usr/bin/env python2
from  __future__ import print_function

__version__ = "0.1"

import json
import contextlib
import urllib
import urllib2
import sys


class Struct(dict):
    """allows an easy access to the parsed json"""
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]

PASTE_SERVICE = "http://paste.chakra-project.org/api/json/all"
PASTE_BASE_URL = "http://paste.chakra-project.org/"


def paste_text(text, language="text", paste_expire=8640, paste_user="Chakra Bot",
        return_link=True):
    """paste text to the pasteboard"""
    # costruct url
    data = {"paste_data": text,
            "paste_lang": language,
            "api_submit": "true",
            "mode": "json",
            "paste_user": paste_user,
            "paste_expire": paste_expire
            }
    with contextlib.closing(urllib2.urlopen(PASTE_BASE_URL, urllib.urlencode(data))) as query:
        id = json.loads(query.read(), object_hook=Struct).result.id
        return PASTE_BASE_URL + id if return_link else id


def get_paste_list_json():
    """helper function which returns an object to access the last paste IDs"""
    with contextlib.closing(urllib2.urlopen(PASTE_SERVICE)) as text:
        return json.loads(text.read(), object_hook=Struct)


def get_latest_paste_id():
    a = get_paste_list_json()
    return a.result.pastes.paste_1


def get_link_to_paste(id):
    return PASTE_BASE_URL + str(id)


def get_archive():
    return PASTE_BASE_URL + "all/"

if __name__ == "__main__":
    for files in sys.argv[1:]:
        with open(files) as f:
            print(paste_text(f.read()))
