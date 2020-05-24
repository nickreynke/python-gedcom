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
Substructure parser for the PLACE_STRUCTURE record identified by the
`gedcom.tags.GEDCOM_TAG_PLACE` tag.
"""

import gedcom.tags as tags
from gedcom.subparsers.note_structure import note_structure

def place_structure(element):
    """Parse and extract a PLACE_STRUCTURE
    :rtype: dict
    """
    record = {
        'name': element.get_value(),
        'hierarchy': '',
        'phonetic': [],
        'romanized': [],
        'latitude': '',
        'longitude': '',
        'notes': []
    }
    for child in element.get_child_elements():
        if child.get_tag() == tags.GEDCOM_TAG_FORMAT:
            record['hierarchy'] = child.get_value()
            continue

        if child.get_tag() == tags.GEDCOM_TAG_NOTE:
            record['notes'].append(note_structure(child))
            continue

        if child.get_tag() == tags.GEDCOM_TAG_PHONETIC:
            subrecord = {
                'name': child.get_value(),
                'type': ''
            }
            for gchild in child.get_child_elements():
                if gchild.get_tag() == tags.GEDCOM_TAG_TYPE:
                    subrecord['type'] = gchild.get_value()
            record['phonetic'].append(subrecord)
            continue

        if child.get_tag() == tags.GEDCOM_TAG_ROMANIZED:
            subrecord = {
                'name': child.get_value(),
                'type': ''
            }
            for gchild in child.get_child_elements():
                if gchild.get_tag() == tags.GEDCOM_TAG_TYPE:
                    subrecord['type'] = gchild.get_value()
            record['romanized'].append(subrecord)
            continue

        if child.get_tag() == tags.GEDCOM_TAG_MAP:
            for gchild in child.get_child_elements():
                if gchild.get_tag() == tags.GEDCOM_TAG_LATITUDE:
                    record['latitude'] = gchild.get_value()
                    continue

                if gchild.get_tag() == tags.GEDCOM_TAG_LONGITUDE:
                    record['longitude'] = gchild.get_value()

    return record
