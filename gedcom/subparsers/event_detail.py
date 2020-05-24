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
Substructure parser for a `EVENT_DETAIL` embedded record.

This is referenced as part of a larger structure so there is no anchor tag.
"""

import gedcom.tags as tags
from gedcom.element.element import Element
from gedcom.subparsers.place_structure import place_structure
from gedcom.subparsers.address_structure import address_structure
from gedcom.subparsers.note_structure import note_structure
from gedcom.subparsers.source_citation import source_citation
from gedcom.subparsers.multimedia_link import multimedia_link

EVENT_TAGS = {
    tags.GEDCOM_TAG_TYPE: 'type',
    tags.GEDCOM_TAG_DATE: 'date',
    tags.GEDCOM_TAG_AGENCY: 'responsible_agency',
    tags.GEDCOM_TAG_RELIGION: 'religious_affiliation',
    tags.GEDCOM_TAG_CAUSE: 'cause_of_event',
    tags.GEDCOM_TAG_RESTRICTION: 'restriction'
}


def event_detail(element: Element) -> dict:
    """Parses and extracts a `EVENT_DETAIL` structure.

    The `element` should be the parent that contains it.
    """
    record = {
        'type': '',
        'date': '',
        'place': {},
        'address': {},
        'responsible_agency': '',
        'religious_affiliation': '',
        'cause_of_event': '',
        'restriction_notice': '',
        'notes': [],
        'citations': [],
        'media': []
    }
    for child in element.get_child_elements():
        if child.get_tag() in EVENT_TAGS:
            record[EVENT_TAGS[child.get_tag()]] = child.get_value()
            continue

        if child.get_tag() == tags.GEDCOM_TAG_PLACE:
            record['place'] = place_structure(child)
            continue

        if child.get_tag() == tags.GEDCOM_TAG_ADDRESS:
            record['address'] = address_structure(element)
            continue

        if child.get_tag() == tags.GEDCOM_TAG_NOTE:
            record['notes'].append(note_structure(child))
            continue

        if child.get_tag() == tags.GEDCOM_TAG_SOURCE:
            record['citations'].append(source_citation(child))
            continue

        if child.get_tag() == tags.GEDCOM_TAG_OBJECT:
            record['media'].append(multimedia_link(child))

    return record
