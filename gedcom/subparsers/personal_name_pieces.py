# -*- coding: utf-8 -*-

# Python GEDCOM Parser
#
# Copyright (C) 2020 Christopher Horn (cdhorn at embarqmail dot com)
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
Substructure parser for the PERSONAL_NAME_PIECES embedded record. As this is
referenced in place in part of another structure there is no identifier tag.
"""

import gedcom.tags as tags
from gedcom.subparsers.note_structure import note_structure
from gedcom.subparsers.source_citation import source_citation

NAME_TAGS = {
    tags.GEDCOM_TAG_NAME_PREFIX: 'prefix',
    tags.GEDCOM_TAG_GIVEN_NAME: 'given',
    tags.GEDCOM_TAG_NICKNAME: 'nick',
    tags.GEDCOM_TAG_SURN_PREFIX: 'surname_prefix',
    tags.GEDCOM_TAG_SURNAME: 'surname',
    tags.GEDCOM_TAG_NAME_SUFFIX: 'suffix',
    tags.GEDCOM_PROGRAM_DEFINED_TAG_RUFNAME: 'rufname'
}

def personal_name_pieces(element):
    """Parse and extract PERSONAL_NAME_PIECES
    :rtype: dict
    """
    record = {
        'prefix': '',
        'given': '',
        'nick': '',
        'surname_prefix': '',
        'surname': '',
        'suffix': '',
        'rufname': '',
        'notes': [],
        'citations': []
    }
    for child in element.get_child_elements():
        if child.get_tag() in NAME_TAGS:
            record[NAME_TAGS[child.get_tag()]] = child.get_value()
            continue

        if child.get_tag() == tags.GEDCOM_TAG_NOTE:
            record['notes'].append(note_structure(child))
            continue

        if child.get_tag() == tags.GEDCOM_TAG_SOURCE:
            record['citations'].append(source_citation(child))
            continue

    return record
