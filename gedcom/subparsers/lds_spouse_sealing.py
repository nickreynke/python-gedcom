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
Substructure parser for the LDS_SPOUSE_SEALING embedded record. As this is
referenced in place as part of another structure there is no identifier tag.
"""

import gedcom.tags as tags
from gedcom.subparsers.note_structure import note_structure
from gedcom.subparsers.source_citation import source_citation

SEALING_TAGS = {
    tags.GEDCOM_TAG_DATE: 'date',
    tags.GEDCOM_TAG_TEMPLE: 'temple',
    tags.GEDCOM_TAG_PLACE: 'place',
    tags.GEDCOM_TAG_FAMILY_CHILD: 'key_to_family'
}


def lds_spouse_sealing(element):
    """Parses and extracts the LDS_SPOUSE_SEALING
    :rtype: dict
    """
    records = []
    for child in element.get_child_elements():
        if child.get_tag() == tags.GEDCOM_TAG_SEALING_SPOUSE:
            record = {
                'date': '',
                'temple': '',
                'place': '',
                'status': '',
                'status_change': '',
                'notes': [],
                'citations': [],
                'tag': tags.GEDCOM_TAG_SEALING_SPOUSE,
                'event': 'lds_spouse_sealing'
            }
            for gchild in child.get_child_elements():
                if gchild.get_tag() in SEALING_TAGS:
                    record[SEALING_TAGS[gchild.get_tag()]] = gchild.get_value()
                    continue

                if gchild.get_tag() == tags.GEDCOM_TAG_STATUS:
                    record['status'] = gchild.get_value()
                    for ggchild in gchild.get_child_elements():
                        if ggchild.get_tag() == tags.GEDCOM_TAG_DATE:
                            record['status_change'] = ggchild.get_value()
                    continue

                if gchild.get_tag() == tags.GEDCOM_TAG_NOTE:
                    record['notes'].append(note_structure(child))
                    continue

                if gchild.get_tag() == tags.GEDCOM_TAG_SOURCE:
                    record['citations'].append(source_citation(child))
                    continue

            records.append(record)
            continue

    return records
