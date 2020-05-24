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
Module containing functions for detecting GEDCOM file encoding and version.
"""

from typing import Tuple
import chardet
import ansel

import gedcom.tags as tags
import gedcom.standards as standards
from gedcom.errors import GedcomFormatViolationError
from gedcom.errors import GedcomCharacterSetUnsupportedError

ansel.register()


def __validate_encoding(file_path, codec):
    """Check the encoding is compatible with the encoding as reported by the
    `gedcom.tags.GEDCOM_TAG_CHARACTER` header tag.
    """
    with open(file_path, 'r', encoding=codec) as gedcom_data:
        for line in gedcom_data:
            if tags.GEDCOM_TAG_CHARACTER in line:
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


def get_encoding(file_path: str) -> str:
    """Probe a GEDCOM file to determine the encoding and validate it against the encoding
    as reported in the `HEADER` record by the `gedcom.tags.GEDCOM_TAG_CHARACTER` tag.

    Returns: codec
    """
    with open(file_path, 'rb') as gedcom_data:
        sample_data = gedcom_data.read(262144)

    # Note chardet reports Ansel as ISO-8859-1 or ISO-8859-2 at this time
    # depending on sample size, and could be making a faulty assumption here
    # by treating it as Ansel. The ansel module supports both ansel and a
    # gedcom codec with some gedcom specific extensions so we use that.
    codec = 'unknown'
    probe = chardet.detect(sample_data)
    if probe['encoding'] in ['UTF-8', 'UTF-8-SIG']:
        codec = 'utf-8-sig'
    elif probe['encoding'] == 'UTF-16':
        codec = 'utf-16'
    elif probe['encoding'] == 'ASCII':
        codec = 'ascii'
    elif probe['encoding'] == 'ANSEL':
        codec = 'ansel'
    elif 'ISO-8859' in probe['encoding']:
        codec = 'gedcom'

    if codec == 'unknown':
        errmsg = "Unable to properly identify a supported GEDCOM character encoding for" + \
            "the file.\nSee: {0}".format(standards.GEDCOM_5_5_1)
        raise GedcomCharacterSetUnsupportedError(errmsg)

    __validate_encoding(file_path, codec)
    return codec


def get_version(file_path: str, codec: str) -> Tuple[str, str, str]:
    """Probe a GEDCOM file to identify the version of the standard used as some reported 5.5
    files are really 5.5.1.

    Returns: probed version, reported version, reported format
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

    probed_version = gedcom_version

    # UTF was added in the 5.5.1 specification
    if gedcom_version == '5.5' and 'utf' in codec:
        probed_version = gedcom_version

    return probed_version, gedcom_version, gedcom_format
