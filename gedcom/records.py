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

"""Module containing the standard GEDCOM record types recognized by the
GEDCOM `gedcom.reader.Reader`."""


GEDCOM_RECORD_FAMILY = "family"
"""Value: `family`

Identifies the `FAM_RECORD` record type."""

GEDCOM_RECORD_HEADER = "header"
"""Value: `header`

Identifies the `HEADER` record type."""

GEDCOM_RECORD_INDIVIDUAL = "individual"
"""Value: `individual`

Identifies the `INDIVIDUAL_RECORD` record type."""

GEDCOM_RECORD_NOTE = "note"
"""Value: `note`

Identifies the `NOTE_RECORD` record type."""

GEDCOM_RECORD_SOURCE = "source"
"""Value: `source`

Identifies the `SOURCE_RECORD` record type."""

GEDCOM_RECORD_REPOSITORY = "repository"
"""Value: `repository`

Identifies the `REPOSITORY_RECORD` record type."""

GEDCOM_RECORD_SUBMISSION = "submission"
"""Value: `submission`

Identifies the `SUBMISSION_RECORD` record type."""

GEDCOM_RECORD_SUBMITTER = "submitter"
"""Value: `submitter`

Identifies the `SUBMITTER_RECORD` record type."""
