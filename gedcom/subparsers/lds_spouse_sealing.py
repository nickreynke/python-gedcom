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
Substructure parser for a `LDS_SPOUSE_SEALING` embedded record.

This is referenced as part of a larger structure so there is no anchor tag.
"""

from typing import List

import gedcom.tags as tags
from gedcom.elements.element import Element
from gedcom.subparsers.note_structure import parse_note_structure
from gedcom.subparsers.source_citation import parse_source_citation

SEALING_TAGS = {
    tags.GEDCOM_TAG_DATE: 'date',
    tags.GEDCOM_TAG_TEMPLE: 'temple',
    tags.GEDCOM_TAG_PLACE: 'place',
    tags.GEDCOM_TAG_FAMILY_CHILD: 'key_to_family'
}


def parse_lds_spouse_sealing(element: Element) -> List[dict]:
    """Parses and extracts a `LDS_SPOUSE_SEALING` structure.

    The `element` should be the parent that contains it.
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
                    record['notes'].append(parse_note_structure(child))
                    continue

                if gchild.get_tag() == tags.GEDCOM_TAG_SOURCE:
                    record['citations'].append(parse_source_citation(child))
                    continue

            records.append(record)
            continue

    return records
