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
Substructure parser for a `LDS_INDIVIDUAL_ORDINANCE` embedded record.

This is referenced as part of a larger structure so there is no anchor tag.
"""

from typing import List

import gedcom.tags as tags
from gedcom.element.element import Element
from gedcom.subparsers.note_structure import note_structure
from gedcom.subparsers.source_citation import source_citation

ORDINANCE_TAGS = {
    tags.GEDCOM_TAG_BAPTISM_LDS: 'lds_baptism',
    tags.GEDCOM_TAG_CONFIRMATION_L: 'lds_confirmation',
    tags.GEDCOM_TAG_ENDOWMENT: 'lds_endowment',
    tags.GEDCOM_TAG_SEALING_CHILD: 'lds_sealing_child'
}

ORDINANCE_ATTRIBUTE_TAGS = {
    tags.GEDCOM_TAG_DATE: 'date',
    tags.GEDCOM_TAG_TEMPLE: 'temple',
    tags.GEDCOM_TAG_PLACE: 'place',
    tags.GEDCOM_TAG_FAMILY_CHILD: 'key_to_family'
}


def lds_individual_ordinance(element: Element) -> List[dict]:
    """Parses and extracts a `LDS_INDIVIDUAL_ORDINANCE` structure.

    The `element` should be the parent that contains it.
    """
    records = []
    for child in element.get_child_elements():
        if child.get_tag() in ORDINANCE_TAGS:
            record = {
                'date': '',
                'temple': '',
                'place': '',
                'status': '',
                'status_change': '',
                'notes': [],
                'citations': [],
                'tag': child.get_tag(),
                'event': ORDINANCE_TAGS[child.get_tag()]
            }
            if child.get_tag() == tags.GEDCOM_TAG_SEALING_CHILD:
                record.update({'key_to_family': ''})
            for gchild in child.get_child_elements():
                if gchild.get_tag() in ORDINANCE_ATTRIBUTE_TAGS:
                    record[ORDINANCE_ATTRIBUTE_TAGS[gchild.get_tag()]] = gchild.get_value()
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
