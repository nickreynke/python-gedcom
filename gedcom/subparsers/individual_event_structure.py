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
Substructure parser for a `INDIVIDUAL_EVENT_STRUCTURE` embedded record.

This is referenced as part of a larger structure so there is no anchor tag.
"""

from typing import List

import gedcom.tags as tags
from gedcom.elements.element import Element
from gedcom.subparsers.individual_event_detail import parse_individual_event_detail

EVENT_TAGS = {
    tags.GEDCOM_TAG_DEATH: 'death',
    tags.GEDCOM_TAG_BURIAL: 'burial',
    tags.GEDCOM_TAG_CREMATION: 'cremation',
    tags.GEDCOM_TAG_BAPTISM: 'baptism',
    tags.GEDCOM_TAG_BAR_MITZVAH: 'bar_mitzvah',
    tags.GEDCOM_TAG_BAS_MITZVAH: 'bas_mitzvah',
    tags.GEDCOM_TAG_BLESSING: 'blessing',
    tags.GEDCOM_TAG_ADULT_CHRISTENING: 'adult_christening',
    tags.GEDCOM_TAG_CONFIRMATION: 'confirmation',
    tags.GEDCOM_TAG_FIRST_COMMUNION: 'first_communion',
    tags.GEDCOM_TAG_ORDINATION: 'ordination',
    tags.GEDCOM_TAG_NATURALIZATION: 'naturalization',
    tags.GEDCOM_TAG_EMIGRATION: 'emmigration',
    tags.GEDCOM_TAG_IMMIGRATION: 'immigration',
    tags.GEDCOM_TAG_CENSUS: 'census',
    tags.GEDCOM_TAG_PROBATE: 'probate',
    tags.GEDCOM_TAG_WILL: 'will',
    tags.GEDCOM_TAG_GRADUATION: 'graduation',
    tags.GEDCOM_TAG_RETIREMENT: 'retirement',
    tags.GEDCOM_TAG_EVENT: 'event',
    tags.GEDCOM_PROGRAM_DEFINED_TAG_DEGREE: 'degree',
    tags.GEDCOM_PROGRAM_DEFINED_TAG_FUNERAL: 'funeral',
    tags.GEDCOM_PROGRAM_DEFINED_TAG_MEDICAL: 'medical',
    tags.GEDCOM_PROGRAM_DEFINED_TAG_MILITARY: 'military'
}

BIRTH_EVENT_TAGS = {
    tags.GEDCOM_TAG_BIRTH: 'birth',
    tags.GEDCOM_TAG_CHRISTENING: 'christening'
}


def parse_individual_event_structure(element: Element) -> List[dict]:
    """Parses and extracts a `INDIVIDUAL_EVENT_STRUCTURE` structure.

    The `element` should be the parent that contains it.
    """
    records = []
    for child in element.get_child_elements():
        if child.get_tag() in BIRTH_EVENT_TAGS:
            record = parse_individual_event_detail(child)
            record['tag'] = child.get_tag()
            record['event'] = BIRTH_EVENT_TAGS[child.get_tag()]
            record['description'] = child.get_multi_line_value()
            record['family'] = ''
            for gchild in child.get_child_elements():
                if gchild.get_tag() == tags.GEDCOM_TAG_FAMILY_CHILD:
                    record['family'] = gchild.get_value()
            records.append(record)
            continue

        if child.get_tag() in EVENT_TAGS:
            record = parse_individual_event_detail(child)
            record['tag'] = child.get_tag()
            record['event'] = EVENT_TAGS[child.get_tag()]
            record['description'] = child.get_multi_line_value()
            records.append(record)
            continue

        if child.get_tag() == tags.GEDCOM_TAG_ADOPTION:
            record = parse_individual_event_detail(child)
            record['tag'] = child.get_tag()
            record['event'] = 'adoption'
            record['description'] = child.get_multi_line_value()
            record['family'] = ''
            record['parent'] = ''
            for gchild in child.get_child_elements():
                if gchild.get_tag() == tags.GEDCOM_TAG_FAMILY_CHILD:
                    record['family'] = gchild.get_value()
                    for ggchild in gchild.get_child_elements():
                        if ggchild.get_tag() == tags.GEDCOM_TAG_ADOPTION:
                            record['parent'] = ggchild.get_value()
            records.append(record)

    return records
