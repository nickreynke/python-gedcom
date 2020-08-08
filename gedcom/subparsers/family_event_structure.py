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
Substructure parser for a `FAMILY_EVENT_STRUCTURE` embedded record.

This is referenced as part of a larger structure so there is no anchor tag.
"""

from typing import List

import gedcom.tags as tags
from gedcom.elements.element import Element
from gedcom.subparsers.family_event_detail import parse_family_event_detail

EVENT_TAGS = {
    tags.GEDCOM_TAG_ANNULMENT: 'annulment',
    tags.GEDCOM_TAG_CENSUS: 'census',
    tags.GEDCOM_TAG_DIVORCE: 'divorce',
    tags.GEDCOM_TAG_DIVORCE_FILED: 'divorce_filed',
    tags.GEDCOM_TAG_ENGAGEMENT: 'engagement',
    tags.GEDCOM_TAG_MARRIAGE: 'marriage',
    tags.GEDCOM_TAG_MARRIAGE_BANN: 'marriage_bann',
    tags.GEDCOM_TAG_MARR_CONTRACT: 'marriage_contract',
    tags.GEDCOM_TAG_MARR_LICENSE: 'marriage_license',
    tags.GEDCOM_TAG_MARR_SETTLEMENT: 'marriage_settlement',
    tags.GEDCOM_TAG_RESIDENCE: 'residence',
    tags.GEDCOM_TAG_EVENT: 'event'
}


def parse_family_event_structure(element: Element) -> List[dict]:
    """Parses and extracts a `FAMILY_EVENT_STRUCTURE` structure.

    The `element` should be the parent that contains it.
    """
    records = []
    for child in element.get_child_elements():
        if child.get_tag() in EVENT_TAGS:
            record = parse_family_event_detail(child)
            record['description'] = child.get_multi_line_value()
            record['tag'] = child.get_tag()
            record['event'] = EVENT_TAGS[child.get_tag()]
            records.append(record)

    return records
