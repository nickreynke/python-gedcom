# -*- coding: utf-8 -*-

#  Copyright (C) 2020
#
#  This file is part of the Python GEDCOM Parser.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#  For more, have a look at the GitHub repository at:
#  https://github.com/nickreynke/python-gedcom

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
    by the parser and the standard for that version requires the
    parser to reject it.
    """


class GedcomFormatUnsupportedError(Exception):
    """Raised if the GEDCOM format is not recognized by the
    parser. Note some common misspellings as documented on page 148
    in the 5.5.5 GEDCOM standard are treated as `LINEAGE-LINKED`
    and allowed when parsing older GEDCOM data.
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
