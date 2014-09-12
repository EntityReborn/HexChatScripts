"""
The MIT License (MIT)

Copyright (c) 2014 Jason Unger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import hexchat
import re

__module_name__ = 'urlhl'
__module_author__ = 'EntityReborn, based on work from TingPing'
__module_version__ = '3'
__module_description__ = 'Highlights URLs'

beforeHL = '\037\00320'
afterHL = '\00399\037'
url_regex = '(.*?)(http(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*?(:(0-9)*)*?(\/?)([a-zA-Z0-9\-‌​\.\?\,\'\/\\\+&amp;%\$#_]*)?)(.*)'

edited = False

def print_cb(word, word_eol, event, attr):
    global edited
    # Ignore our own events, bouncer playback, empty messages
    if edited or attr.time or not len(word) > 1:
        return

    msg = word[1]
    if re.compile(url_regex).match(msg):
        msg = re.sub(url_regex, "\\1" + beforeHL + "\\2" + afterHL + "\\9", msg).strip()

        edited = True
        hexchat.emit_print(event, word[0], msg)
        edited = False

        return hexchat.EAT_HEXCHAT

events = ("Channel Message", "Channel Action",
          "Channel Msg Hilight", "Channel Action Hilight",
          "Private Message", "Private Action")
          
for hook in events:
    hexchat.hook_print_attrs(hook, print_cb, hook, priority=hexchat.PRI_LOW)