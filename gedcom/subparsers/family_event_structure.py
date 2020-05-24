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
Substructure parser for the FAMILY_EVENT_STRUCTURE embedded record. As this is
referenced in place as part of another structure there is no identifier tag.
"""

import gedcom.tags as tags
from gedcom.subparsers.family_event_detail import family_event_detail

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


def family_event_structure(element):
    """Parses and extracts the FAMILY_EVENT_STRUCTURE
    :rtype: dict
    """
    records = []
    for child in element.get_child_elements():
        if child.get_tag() in EVENT_TAGS:
            record = family_event_detail(child)
            record['description'] = child.get_multi_line_value()
            record['tag'] = child.get_tag()
            record['event'] = EVENT_TAGS[child.get_tag()]
            records.append(record)

    return records
