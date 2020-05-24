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
Substructure parser for the INDIVIDUAL_ATTRIBUTE_STRUCTURE embedded record. As
this is referenced in place as part of another structure there is no identifier tag.
"""

import gedcom.tags as tags
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

def individual_attribute_structure(element):
    """Parses and extracts the INDIVIDUAL_ATTRIBUTE_STRUCTURE
    :rtype: dict
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
