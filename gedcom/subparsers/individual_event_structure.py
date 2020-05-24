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
Substructure parser for the INDIVIDUAL_EVENT_STRUCTURE embedded record. As this is
referenced in place as part of another structure there is no identifier tag.
"""

import gedcom.tags as tags
from gedcom.subparsers.individual_event_detail import individual_event_detail

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

def individual_event_structure(element):
    """Parses and extracts the INDIVIDUAL_EVENT_STRUCTURE
    :rtype: dict
    """
    records = []
    for child in element.get_child_elements():
        if child.get_tag() in BIRTH_EVENT_TAGS:
            record = individual_event_detail(child)
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
            record = individual_event_detail(child)
            record['tag'] = child.get_tag()
            record['event'] = EVENT_TAGS[child.get_tag()]
            record['description'] = child.get_multi_line_value()
            records.append(record)
            continue

        if child.get_tag() == tags.GEDCOM_TAG_ADOPTION:
            record = individual_event_detail(child)
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
