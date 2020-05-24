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
Substructure parser for the CHANGE_DATE record identified by the
`gedcom.tags.GEDCOM_TAG_CHANGE` tag.
"""

import gedcom.tags as tags
from gedcom.subparsers.note_structure import note_structure

def change_date(element):
    """Parses and extracts the CHANGE_DATE
    :rtype: dict
    """
    record = {
        'date': '',
        'time': '',
        'notes': []
    }
    for child in element.get_child_elements():
        if child.get_tag() == tags.GEDCOM_TAG_DATE:
            record['date'] = child.get_value()
            for gchild in child.get_child_elements():
                if gchild.get_tag() == tags.GEDCOM_TAG_TIME:
                    record['time'] = gchild.get_value()
                    continue
            continue

        if child.get_tag() == tags.GEDCOM_TAG_NOTE:
            record['notes'].append(note_structure(child))

    return record
