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
Substructure parser for a `CHILD_TO_FAMILY_LINK` record.

This is anchored by the `gedcom.tags.GEDCOM_TAG_FAMILY_CHILD` tag.
"""

import gedcom.tags as tags
from gedcom.element.element import Element
from gedcom.subparsers.note_structure import note_structure


def child_to_family_link(element: Element) -> dict:
    """Parses and extracts a `CHILD_TO_FAMILY_LINK` structure.

    The `element` should contain the `gedcom.tags.GEDCOM_TAG_FAMILY_CHILD` tag.
    """
    record = {
        'key_to_family': element.get_value(),
        'pedigree': '',
        'status': '',
        'notes': []
    }
    for child in element.get_child_elements():
        if child.get_tag() == tags.GEDCOM_TAG_PEDIGREE:
            record['pedigree'] = child.get_value()
            continue

        if child.get_tag() == tags.GEDCOM_TAG_STATUS:
            record['status'] = child.get_value()
            continue

        if child.get_tag() == tags.GEDCOM_TAG_NOTE:
            record['notes'].append(note_structure(child))

    return record
