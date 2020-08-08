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
Substructure parser for the `INDIVIDUAL_ATTRIBUTE_STRUCTURE` embedded record.

This is referenced as part of a larger structure so there is no anchor tag.
"""

from typing import List

import gedcom.tags as tags
from gedcom.element.element import Element
from gedcom.subparsers.individual_event_detail import individual_event_detail

ATTRIBUTE_TAGS = {
    tags.GEDCOM_TAG_CASTE: 'caste',
    tags.GEDCOM_TAG_PHY_DESCRIPTION: 'physical_description',
    tags.GEDCOM_TAG_EDUCATION: 'eduction',
    tags.GEDCOM_TAG_IDENT_NUMBER: 'identity_number',
    tags.GEDCOM_TAG_NATIONALITY: 'nationality',
    tags.GEDCOM_TAG_CHILDREN_COUNT: 'number_of_children',
    tags.GEDCOM_TAG_MARRIAGE_COUNT: 'number_of_marriages',
    tags.GEDCOM_TAG_OCCUPATION: 'occupation',
    tags.GEDCOM_TAG_PROPERTY: 'property',
    tags.GEDCOM_TAG_RELIGION: 'religion',
    tags.GEDCOM_TAG_RESIDENCE: 'residence',
    tags.GEDCOM_TAG_SOC_SEC_NUMBER: 'social_security_number',
    tags.GEDCOM_TAG_TITLE: 'title',
    tags.GEDCOM_TAG_FACT: 'fact',
    tags.GEDCOM_PROGRAM_DEFINED_TAG_DCAUSE: 'cause_of_death'
}


def individual_attribute_structure(element: Element) -> List[dict]:
    """Parses and extracts the `INDIVIDUAL_ATTRIBUTE_STRUCTURE` structures.

    The `element` should be the parent that contains them.
    """
    records = []
    for child in element.get_child_elements():
        if child.get_tag() in ATTRIBUTE_TAGS:
            record = individual_event_detail(child)
            record['description'] = child.get_multi_line_value()
            record['tag'] = child.get_tag()
            record['attribute'] = ATTRIBUTE_TAGS[child.get_tag()]
            records.append(record)
            continue

    return records
