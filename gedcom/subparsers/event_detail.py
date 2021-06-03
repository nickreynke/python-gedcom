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

"""
Substructure parser for a `EVENT_DETAIL` embedded record.

This is referenced as part of a larger structure so there is no anchor tag.
"""

import gedcom.tags as tags
from gedcom.elements.element import Element
from gedcom.subparsers.place_structure import parse_place_structure
from gedcom.subparsers.address_structure import parse_address_structure
from gedcom.subparsers.note_structure import parse_note_structure
from gedcom.subparsers.source_citation import parse_source_citation
from gedcom.subparsers.multimedia_link import parse_multimedia_link

EVENT_TAGS = {
    tags.GEDCOM_TAG_TYPE: 'type',
    tags.GEDCOM_TAG_DATE: 'date',
    tags.GEDCOM_TAG_AGENCY: 'responsible_agency',
    tags.GEDCOM_TAG_RELIGION: 'religious_affiliation',
    tags.GEDCOM_TAG_CAUSE: 'cause_of_event',
    tags.GEDCOM_TAG_RESTRICTION: 'restriction'
}


def parse_event_detail(element: Element) -> dict:
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
            record['place'] = parse_place_structure(child)
            continue

        if child.get_tag() == tags.GEDCOM_TAG_ADDRESS:
            record['address'] = parse_address_structure(element)
            continue

        if child.get_tag() == tags.GEDCOM_TAG_NOTE:
            record['notes'].append(parse_note_structure(child))
            continue

        if child.get_tag() == tags.GEDCOM_TAG_SOURCE:
            record['citations'].append(parse_source_citation(child))
            continue

        if child.get_tag() == tags.GEDCOM_TAG_OBJECT:
            record['media'].append(parse_multimedia_link(child))

    return record
