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
Substructure parser for the ASSOCIATION_STRUCTURE record identified by the
`gedcom.tags.GEDCOM_TAG_ASSOCIATION` tag.
"""

import gedcom.tags as tags
from gedcom.subparsers.note_structure import note_structure
from gedcom.subparsers.source_citation import source_citation

def association_structure(element):
    """Parses and extracts the ASSOCIATION_STRUCTURE
    :rtype: dict
    """
    record = {
        'key_to_individual': element.get_value(),
        'relationship': '',
        'citations': [],
        'notes': []
    }
    for child in element.get_child_elements():
        if child.get_tag() == tags.GEDCOM_TAG_RELATIONSHIP:
            record['relationship'] = child.get_value()
            continue

        if child.get_tag() == tags.GEDCOM_TAG_NOTE:
            record['notes'].append(note_structure(child))
            continue

        if child.get_tag() == tags.GEDCOM_TAG_SOURCE:
            record['citations'].append(source_citation(child))

    return record
