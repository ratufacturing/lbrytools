#!/usr/bin/env python3
# --------------------------------------------------------------------------- #
# The MIT License (MIT)                                                       #
#                                                                             #
# Copyright (c) 2021 Eliud Cabrera Castillo <e.cabrera-castillo@tum.de>       #
#                                                                             #
# Permission is hereby granted, free of charge, to any person obtaining       #
# a copy of this software and associated documentation files                  #
# (the "Software"), to deal in the Software without restriction, including    #
# without limitation the rights to use, copy, modify, merge, publish,         #
# distribute, sublicense, and/or sell copies of the Software, and to permit   #
# persons to whom the Software is furnished to do so, subject to the          #
# following conditions:                                                       #
#                                                                             #
# The above copyright notice and this permission notice shall be included     #
# in all copies or substantial portions of the Software.                      #
#                                                                             #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL     #
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         #
# DEALINGS IN THE SOFTWARE.                                                   #
# --------------------------------------------------------------------------- #
"""Auxiliary functions for other methods of the lbrytools package."""
import os
import regex
import requests
import subprocess
import time

try:
    import emoji
    EMOJI_LOADED = True
except ModuleNotFoundError:
    EMOJI_LOADED = False


def start_lbry():
    """Launch the lbrynet client through subprocess."""
    subprocess.run(["lbrynet", "start"], stdout=subprocess.DEVNULL)


def check_lbry(server="http://localhost:5279"):
    """Check if the LBRY daemon is running, and launch it if it's not.

    Send a `'status'` request to the server `'http://localhost:5279'`,
    and check for `'is_running'` being `True`.

    Start the service if it is not running.
    ::
        lbrynet start

    Other functions that need to call `lbrynet` should call this method
    before doing other things.

    Parameters
    ----------
    server: str, optional
        It defaults to `'http://localhost:5279'`.
        This is the address of the `lbrynet` daemon, which should be running
        in your computer before using any `lbrynet` command.
        Normally, there is no need to change this parameter from its default
        value.

    Returns
    -------
    bool
        It returns `True` if the LBRY daemon is already running.
        It returns `False` if the LBRY daemon was not running
        but it was started manually.
    """
    msg = {"method": "status"}
    try:
        output = requests.post(server, json=msg).json()
    except requests.exceptions.ConnectionError as err:
        # Trap all with requests.exceptions.RequestException
        print(err)
        start_lbry()
        return False

    if "result" not in output:
        print(">>> No 'result' in the JSON-RPC server output")
        start_lbry()
        return False

    if "is_running" in output["result"] and output["result"]["is_running"]:
        return True

    start_lbry()
    return False

    # Only really works in Linux
    # try:
    #     subprocess.run(["pidof", "lbrynet"], stdout=subprocess.DEVNULL)
    #     return True
    # except subprocess.CalledProcessError:
    #     start_lbry()
    #     return False


def server_exists(server="http://localhost:5279"):
    """Return True if the server is up, and False if not."""
    try:
        requests.post(server)
    except requests.exceptions.ConnectionError:
        print(f"Cannot establish connection to 'lbrynet' on {server}")
        print("Start server with:")
        print("  lbrynet start")
        return False
    return True


def print_content(output_list, file=None, fdate=None):
    """Print contents to the terminal or to a file."""
    fd = 0

    if file:
        dirn = os.path.dirname(file)
        base = os.path.basename(file)

        if fdate:
            fdate = time.strftime("%Y%m%d_%H%M", time.localtime()) + "_"
        else:
            fdate = ""

        file = os.path.join(dirn, fdate + base)

        try:
            fd = open(file, "w")
        except (FileNotFoundError, PermissionError) as err:
            print(f"Cannot open file for writing; {err}")

    content = "\n".join(output_list)

    if file and fd:
        print(content, file=fd)
        fd.close()
        print(f"Summary written: {file}")
    else:
        print(content)

    return content


def sanitize_name(text="random_string"):
    """Sanitize names with complex unicode characters.

    Some names have complex unicode characters, especially emojis.
    With this method we remove these `grapheme clusters` so that applications
    that receive the string don't cause an error.

    Many terminals and interface toolkits are able to display the emojis
    without problem but others such as Tkinter Text widgets
    may crash when trying to display such symbols.
    """
    # This will find unicode country flags, which are actually composed
    # of two or more characters together, like 'U' 'S' is the US flag,
    # and 'F' 'R' is the France flag.
    flags = regex.findall(u'[\U0001F1E6-\U0001F1FF]', text)

    name_normalized = ""

    # Only remove the emojis if we have the `emoji` package loaded
    if EMOJI_LOADED:
        emoji_dict = emoji.UNICODE_EMOJI['en']
    else:
        emoji_dict = ""

    for character in text:
        if character in emoji_dict or character in flags:
            name_normalized += "\u275A"  # monospace black box
        else:
            name_normalized += character

    return name_normalized
