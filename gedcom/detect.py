# -*- coding: utf-8 -*-

# Python GEDCOM Parser
#
# Copyright (C) 2020 Christopher Horn (cdhorn at embarqmail dot com)
# Copyright (C) 2018 Damon Brodie (damon.brodie at gmail.com)
# Copyright (C) 2018-2019 Nicklas Reincke (contact at reynke.com)
# Copyright (C) 2016 Andreas Oberritter
# Copyright (C) 2012 Madeleine Price Ball
# Copyright (C) 2005 Daniel Zappala (zappala at cs.byu.edu)
# Copyright (C) 2005 Brigham Young University
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Further information about the license: http://www.gnu.org/licenses/gpl-2.0.html

"""
Functions to detect GEDCOM encoding and version.
"""

import chardet

import gedcom.standards as standards

from gedcom.errors import GedcomFormatViolationError
from gedcom.errors import GedcomCharacterSetUnsupportedError

try:
    import ansel
    ansel.register()
    ANSEL_AVAILABLE = True
except ModuleNotFoundError:
    ANSEL_AVAILABLE = False

def validate_encoding(file_path, codec):
    """Check the encoding is compatible with the encoding reported
    :type file_path: str
    :type codec: str
    """
    with open(file_path, 'r', encoding=codec) as gedcom_data:
        for line in gedcom_data:
            if 'CHAR' in line:
                character_set = line.split(' ')[2].lower().strip()
                break

    if character_set == 'ansel' and codec == 'gedcom':
        return

    if character_set == 'ascii' and codec == 'utf-8':
        return

    if character_set not in codec:
        errmsg = "A " + codec + " encoding was detected but the GEDCOM reports using " + \
            "a " + character_set + " encoding.\n" + \
            "Processing aborted as unsure how to properly proceed.\n" + \
            "See: {0}".format(standards.GEDCOM_5_5_1)
        raise GedcomCharacterSetUnsupportedError(errmsg)

def get_encoding(file_path):
    """Examines file to determine encoding to use and then validates it
    :type file_path: str
    :rtype: str
    """
    with open(file_path, 'rb') as gedcom_data:
        sample_data = gedcom_data.read(262144)

    # Note chardet reports Ansel as ISO-8859-1 or ISO-8859-2 at this time
    # depending on sample size, and could be making a faulty assumption here
    # by treating it as Ansel. The ansel module supports both ansel and a
    # gedcom codec with some gedcom specific extensions so we use that.
    codec = 'unknown'
    probe = chardet.detect(sample_data)
    if probe['encoding'] == 'utf-8':
        codec = 'utf-8-sig'
    elif probe['encoding'] == 'utf-16':
        codec = 'utf-16'
    elif probe['encoding'] == 'ascii':
        codec = 'ascii'
    elif probe['encoding'] == 'ansel':
        codec = 'ansel'
    elif 'ISO-8859' in probe['encoding']:
        if ANSEL_AVAILABLE:
            codec = 'gedcom'
        else:
            errmsg = "This parser supports ANSEL but the Python ansel module is not " + \
                "available at this time.\nSee: {0}".format(standards.GEDCOM_5_5_1)
            raise GedcomCharacterSetUnsupportedError(errmsg)

    if codec == 'unknown':
        errmsg = "Unable to properly identify a supported GEDCOM character encoding for" + \
            "the file.\nSee: {0}".format(standards.GEDCOM_5_5_1)
        raise GedcomCharacterSetUnsupportedError(errmsg)

    validate_encoding(file_path, codec)
    return codec

def get_version(file_path, codec):
    """Probes Gedcom to identify version used, should expand this in future
    Returns probed version, reported version, reported format
    :type file_path: str
    :type encoding: str
    :rtype: str, str, str
    """
    in_gedc_tag = False
    gedcom_version = None
    gedcom_format = None
    with open(file_path, 'r', encoding=codec) as gedcom_data:
        for line in gedcom_data:
            if '1 GEDC' in line:
                in_gedc_tag = True
                continue
            if in_gedc_tag:
                if '2 VERS' in line:
                    gedcom_version = line.split(' ')[2].strip()
                    continue
                if '2 FORM' in line:
                    gedcom_format = line.split(' ')[2].strip()
                    break

    if gedcom_version is None or gedcom_format is None:
        errmsg = "Malformed GEDCOM file, the required version number or format were" + \
            " not found as expected.\nSee: {0}".format(standards.GEDCOM_5_5_1)
        raise GedcomFormatViolationError(errmsg)

    real_version = gedcom_version

    # UTF came in the 5.5.1 specification
    if gedcom_version == '5.5' and 'utf' in codec:
        real_version = gedcom_version

    return real_version, gedcom_version, gedcom_format
