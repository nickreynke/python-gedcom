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

"""Module containing the standard GEDCOM record types recognized by the
GEDCOM `gedcom.reader.Reader`."""


GEDCOM_RECORD_FAMILY = 'family'
"""Identifies the `FAM_RECORD` record type."""

GEDCOM_RECORD_HEADER = 'header'
"""Identifies the `HEADER` record type."""

GEDCOM_RECORD_INDIVIDUAL = 'individual'
"""Identifies the `INDIVIDUAL_RECORD` record type."""

GEDCOM_RECORD_NOTE = 'note'
"""Identifies the `NOTE_RECORD` record type."""

GEDCOM_RECORD_SOURCE = 'source'
"""Identifies the `SOURCE_RECORD` record type."""

GEDCOM_RECORD_REPOSITORY = 'repository'
"""Identifies the `REPOSITORY_RECORD` record type."""

GEDCOM_RECORD_SUBMISSION = 'submission'
"""Identifies the `SUBMISSION_RECORD` record type."""

GEDCOM_RECORD_SUBMITTER = 'submitter'
"""Identifies the `SUBMITTER_RECORD` record type."""
