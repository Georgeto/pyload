# -*- coding: utf-8 -*-

import re

from module.plugins.internal.SimpleHoster import SimpleHoster


class FileStoreTo(SimpleHoster):
    __name__    = "FileStoreTo"
    __type__    = "hoster"
    __version__ = "0.09"
    __status__  = "testing"

    __pattern__ = r'http://(?:www\.)?filestore\.to/\?d=(?P<ID>\w+)'
    __config__  = [("activated"   , "bool", "Activated"                                        , True),
                   ("use_premium" , "bool", "Use premium account if available"                 , True),
                   ("fallback"    , "bool", "Fallback to free download if premium fails"       , True),
                   ("chk_filesize", "bool", "Check file size"                                  , True),
                   ("max_wait"    , "int" , "Reconnect if waiting time is greater than minutes", 10  )]

    __description__ = """FileStore.to hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("Walter Purcaro", "vuolter@gmail.com"),
                       ("stickell", "l.stickell@yahoo.it")]


    INFO_PATTERN         = r'File: <span.*?>(?P<N>.+?)<.*>Size: (?P<S>[\d.,]+) (?P<U>[\w^_]+)'
    OFFLINE_PATTERN      = r'>Download-Datei wurde nicht gefunden<'
    TEMP_OFFLINE_PATTERN = r'>Der Download ist nicht bereit !<'


    def setup(self):
        self.resume_download = True
        self.multiDL        = True


    def handle_free(self, pyfile):
        self.wait(10)
        self.link = self.load("http://filestore.to/ajax/download.php",
                              get={'D': re.search(r'"D=(\w+)', self.data).group(1)})
