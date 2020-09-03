# https://gist.github.com/doronhorwitz/fc5c4234a9db9ed87c53213d79e63b6c

# https://www.nxp.com/docs/en/application-note/AN11697.pdf explains how to
# setup a demo of the PN7120/PN7150. With that demo comes an executable called
# "nfcDemoApp". This gist is a proof of concept for how to read from that
# executable in Python.

# The class (which is called PN7150, even though it also should support PN7120)
# reads the output from the PN7150 each time a tag is read. It finds the line
# starting with "Text :" and extracts out the text - which is the text stored
# by the NFC tag. The reading is done in a separate thread, which calls a
# callback with the text every time an NFC tag is read. Writing and single
# synchronous reads are also supported

# Lots of inspiration and learning from various places including:
# https://github.com/NXPNFCLinux/linux_libnfc-nci/issues/49#issuecomment-326301
# 669
# https://stackoverflow.com/a/4791612
# https://stackoverflow.com/a/38802275
# https://repolinux.wordpress.com/2012/10/09/non-blocking-read-from-stdin-in-py
# thon/
# https://stackoverflow.com/questions/18225816/indicate-no-more-input-without-c
# losing-pty

import os
import pty
import shlex
import subprocess
import threading


_MAX_WRITE_RETRIES = 5
_OUTPUT_TEXT = "Text :"
_OUTPUT_TAG_WRITTEN = "Write Tag OK"
_OUTPUT_READ_FAILED = "Read NDEF Content Failed"
_OUTPUT_TAG_REMOVED = "NFC Tag Lost"
_CMD_POLL = "{nfc_demo_app_path} poll"
_CMD_WRITE = '{nfc_demo_app_path} write --type=Text -l en -r "{new_text}"'
_NFC_DEMO_APP_NAME = "nfcDemoApp"
_NFC_DEMO_APP_DEFAULT_LOCATION = "/usr/sbin"


class PN7150Exception(Exception):
    pass


class PN7150:
    """
    Can use this class as follows:

    pn7150 = PN7150()


    Start Continuous Reading
    ========================
    def text_callback(text):
       ... do something with text

    pn7150.when_tag_read = text_callback
    pn7150.start_reading()


    Stop Continuous Reading (be sure to do this before your program ends)
    =======================
    pn7150.stop_reading()


    Read Once
    =========
    text = pn7150.read_once()


    Write
    =====
    success = pn7150.write("some text")
    """

    def __init__(self, nfc_demo_app_location=_NFC_DEMO_APP_DEFAULT_LOCATION):
        self._nfc_demo_app_location = nfc_demo_app_location
        self._read_running = False
        self._proc = None
        self._slave = None
        self.when_tag_read = None

    def _open_process(self, mode, **cmd_arguments):
        if mode == "r":
            cmd_string = _CMD_POLL
        elif mode == "w":
            cmd_string = _CMD_WRITE
        else:
            raise PN7150Exception("mode must be 'r' or 'w'")

        cmd = cmd_string.format(
            nfc_demo_app_path=self._nfc_demo_app_path, **cmd_arguments
        )
        master, slave = pty.openpty()
        proc = subprocess.Popen(
            shlex.split(cmd), stdin=subprocess.PIPE, stdout=slave, stderr=slave
        )
        stdout = os.fdopen(master)

        return proc, slave, stdout

    def _read_thread(self):
        self._proc, self._slave, stdout = self._open_process("r")
        self._read_running = True
        while self._read_running:
            try:
                line = stdout.readline()
                if _OUTPUT_TEXT in line:
                    first = line.find("'")
                    last = line.rfind("'")
                    text = line[first + 1 : last]
                    if self.when_tag_read:
                        self.when_tag_read(text)
            except OSError:
                pass

    @property
    def _nfc_demo_app_path(self):
        return os.path.join(self._nfc_demo_app_location, _NFC_DEMO_APP_NAME)

    def start_reading(self):
        if not self._read_running:
            thread = threading.Thread(target=self._read_thread)
            thread.start()

    def stop_reading(self):
        if self._read_running:
            self._proc.terminate()
            self._read_running = False
            os.close(self._slave)

    def read_once(self, wait_for_tag_removal=True):
        if self._read_running:
            raise PN7150Exception("cannot read_once while a continuous read is running")

        proc, slave, stdout = self._open_process("r")

        been_read = False
        been_removed = not wait_for_tag_removal
        text = None
        while not been_read or not been_removed:
            line = stdout.readline()
            if _OUTPUT_TEXT in line:
                first = line.find("'")
                last = line.rfind("'")
                text = line[first + 1 : last]
                been_read = True
            elif _OUTPUT_READ_FAILED in line:
                been_read = True
            elif _OUTPUT_TAG_REMOVED in line:
                been_removed = True

        proc.terminate()
        os.close(slave)

        return text

    def _write(self, new_text, wait_for_tag_removal=True):
        proc, slave, stdout = self._open_process("w", new_text=new_text)

        been_written = False
        been_checked = False
        been_removed = not wait_for_tag_removal
        checked_text = None
        while not been_written or not been_checked or not been_removed:
            line = stdout.readline()
            if _OUTPUT_TAG_WRITTEN in line:
                been_written = True
            elif been_written and _OUTPUT_TEXT in line:
                first = line.find("'")
                last = line.rfind("'")
                checked_text = line[first + 1 : last]
                been_checked = True
            elif _OUTPUT_TAG_REMOVED in line:
                been_removed = True

        proc.terminate()
        os.close(slave)
        return checked_text == new_text

    def write(self, new_text, wait_for_tag_removal=True):
        if self._read_running:
            raise PN7150Exception("cannot write while a continuous read is running")

        existing_text = self.read_once(wait_for_tag_removal=wait_for_tag_removal)
        success = False
        if existing_text != new_text:
            count = 0
            while not success and count < _MAX_WRITE_RETRIES:
                success = self._write(
                    new_text, wait_for_tag_removal=wait_for_tag_removal
                )
            return success
        else:
            success = True

        return success
