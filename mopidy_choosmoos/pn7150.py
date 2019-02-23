# https://gist.github.com/doronhorwitz/fc5c4234a9db9ed87c53213d79e63b6c

# https://www.nxp.com/docs/en/application-note/AN11697.pdf explains how to setup a demo of the PN7120/PN7150.
# With that demo comes an executable called 'nfcDemoApp'. This gist is a proof of concept for how to read from that
# executable in Python.

# The class (which is called PN7150, even though it also should support PN7120) reads the output from the PN7150 each
# time a tag is read. It finds the line starting with "Text :" and extracts out the text - which is the text stored
# by the NFC tag.
# The reading is done in a separate thread, which calls a callback with the text every time an NFC tag is read.

# Lots of inspiration and learning from various places including:
# https://github.com/NXPNFCLinux/linux_libnfc-nci/issues/49#issuecomment-326301669
# https://stackoverflow.com/a/4791612
# https://stackoverflow.com/a/38802275
# https://repolinux.wordpress.com/2012/10/09/non-blocking-read-from-stdin-in-python/
# https://stackoverflow.com/questions/18225816/indicate-no-more-input-without-closing-pty

import os
import pty
import subprocess
import threading


class PN7150(object):
    """
    Can use this class as follows:
    def text_callback(text):
       ... do something with text
    pn7150 = PN7150()
    pn7150.when_tag_read = text_callback
    pn7150.start_reading()
    ... do some things
    pn7150.stop_reading()
    """

    def __init__(self, nfc_demo_app_location='/usr/sbin'):
        self._nfc_demo_app_location = nfc_demo_app_location
        self._running = False
        self._proc = None
        self._slave = None
        self.when_tag_read = None

    def stop_reading(self):
        self._proc.terminate()
        self._running = False
        os.close(self._slave)

    def read_thread(self):
        master, self._slave = pty.openpty()
        self._proc = subprocess.Popen([os.path.join(self._nfc_demo_app_location, 'nfcDemoApp'), 'poll'],
                                      stdin=subprocess.PIPE, stdout=self._slave, stderr=self._slave)
        stdout = os.fdopen(master)

        self._running = True
        while self._running:
            try:
                line = stdout.readline()
                if 'Text :' in line:
                    first = line.find("'")
                    last = line.rfind("'")
                    text = line[first + 1:last]
                    if self.when_tag_read:
                        self.when_tag_read(text)
            except OSError:
                pass

    def start_reading(self):
        thread = threading.Thread(target=self.read_thread)
        thread.start()