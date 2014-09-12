import hexchat
import os
import re
import datetime

__module_name__ = "URL Logger"
__module_author__ = "Poorchop, __import__"
__module_version__ = "0.2"
__module_description__ = "Log URLs from a specific channel to disk"

basedir = os.path.join(hexchat.get_info("configdir"), "logs")

events = ("Channel Message", "Channel Action",
          "Channel Msg Hilight", "Channel Action Hilight",
          "Private Message", "Private Action")
          
url_regex = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

def log_url(message, sender, network, chan):
    directory = os.path.join(basedir, network)
    if not os.path.exists(directory):
        os.makedirs(directory)
    directory = os.path.join(directory, chan + ".log")
    
    timestamp = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
    
    with open(directory, "a") as f:
        f.write("{0}\t{1}\t{2}\n".format(timestamp, sender, message))

def contains_url(word, network, chan):
    if url_regex.match(word):
        return True
        
    return False

def chan_check_cb(word, word_eol, userdata):
    sender = hexchat.strip(word[0])
        
    recipient = hexchat.get_info('channel')
    
    if recipient[0] != '#':
        recipient = sender
        
    network = hexchat.get_info('network')
    msg = word[1]
    
    if contains_url(msg, network, recipient):
        log_url(msg, sender, network, recipient)
        
for event in events:
    hexchat.hook_print(event, chan_check_cb)

hexchat.prnt(__module_name__ + " version " + __module_version__ + " loaded")
hexchat.prnt("Outputting to " + basedir)