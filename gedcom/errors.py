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
Module containing the exception handling classes.
"""


class GedcomFormatViolationError(Exception):
    """Raised when the document format does not appear to conform
    to the GEDCOM standard and strict parsing required.
    """


class GedcomStructureViolationError(Exception):
    """Raised when the structure of a record does not conform to
    the GEDCOM standard.
    """


class GedcomCharacterSetUnsupportedError(Exception):
    """Raised when a GEDCOM appears to contain a character set
    the standard or the parser does not support.
    """


class GedcomVersionUnsupportedError(Exception):
    """Raised when a particular GEDCOM version is not supported
    by the parser and the standard for the version requires the
    parser to reject it.
    """


class GedcomFormatUnsupportedError(Exception):
    """Raised if the GEDCOM format is not recognized by the
    parser. Note some misspellings as documented on page 148
    in the 5.5.5 standard are treated as LINEAGE-LINKED and
    allowed.
    """


class NotAnActualIndividualError(Exception):
    """Raised if record does not appear to be an `INDIVIDUAL_RECORD`"""


class NotAnActualFamilyError(Exception):
    """Raised if record does not appear to be a `FAM_RECORD`"""


class NotAnActualSourceError(Exception):
    """Raised if record does not appear to be a `SOURCE_RECORD`"""


class NotAnActualRepositoryError(Exception):
    """Raised if record does not appear to be a `REPOSITORY_RECORD`"""


class NotAnActualNoteError(Exception):
    """Raised if record does not appear to be a `NOTE_RECORD`"""


class NotAnActualObjectError(Exception):
    """Raised if record does not appear to be a `MULTIMEDIA_RECORD`"""


class NotAnActualHeaderError(Exception):
    """Raised if record does not appear to be a `HEADER`"""


class NotAnActualSubmitterError(Exception):
    """Raised if record does not appear to be a `SUBMITTER_RECORD`"""


class NotAnActualSubmissionError(Exception):
    """Raised if record does not appear to be a `SUBMISSION_RECORD`"""
