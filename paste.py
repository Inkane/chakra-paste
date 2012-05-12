#!/usr/bin/env python2
from  __future__ import print_function

__version__ = "0.2"

import json
import contextlib
import urllib
import urllib2
import argparse
import subprocess


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


def paste_text(text, language="text", paste_expire=8640, paste_user="paste.py",
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
    try:
        with contextlib.closing(urllib2.urlopen(PASTE_BASE_URL, urllib.urlencode(data))) as query:
            id = json.loads(query.read(), object_hook=Struct).result.id
            return PASTE_BASE_URL + id if return_link else id
    except urllib2.HTTPError as e:
        print("Error uploading file:")
        print(e.reason)


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


def main():
    parser = argparse.ArgumentParser(description="Pastes some files to "
            "paste.chakra.org and returns the URL to the paste")
    parser.add_argument("file", nargs="*", help="the files which are uploaded")
    parser.add_argument("--dmesg", help="upload the output of dmesg",
            action="store_true")
    parser.add_argument("--paclog", help="upload pacman.log",
            action="store_true")
    parser.add_argument("--pacconf", help="upload shortened pacman.log",
            action="store_true")
    parser.add_argument("--version", "-v", action="version", version=__version__)
    args = parser.parse_args()
    if args.dmesg:
        text = subprocess.check_output(["dmesg"])
        print(paste_text(text))
    if args.paclog:
        with open("/var/log/pacman.log") as text:
            print("pacman.log: ", paste_text(text.read()[-7000:]))
    if args.pacconf:
        with open("/etc/pacman.conf") as text:
            print("pacman.conf: ", paste_text(text.read()))
    for f in args.file:
        # paste all files
        with open(f) as text:
            print(paste_text(text.read()))

if __name__ == "__main__":
    main()
