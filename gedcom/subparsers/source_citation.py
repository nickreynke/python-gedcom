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
Substructure parser for the SOURCE_CITATION record identified by the
`gedcom.tags.GEDCOM_TAG_SOURCE` tag.
"""

import gedcom.tags as tags
from gedcom.subparsers.multimedia_link import multimedia_link
from gedcom.subparsers.note_structure import note_structure

CITATION_TAGS = {
    tags.GEDCOM_TAG_PAGE: 'page',
    tags.GEDCOM_TAG_DATE: 'date',
    tags.GEDCOM_TAG_QUALITY_OF_DATA: 'quality',
    tags.GEDCOM_PROGRAM_DEFINED_TAG_APID: 'apid'
}

def source_citation(element):
    """Parse and extract a SOURCE_CITATION
    :rtype: dict
    """
    record = {
        'key_to_source': element.get_value(),
        'source': '',
        'page': '',
        'event': '',
        'role': '',
        'date': '',
        'text': '',
        'media': [],
        'notes': [],
        'quality': '',
        'apid': ''
    }
    if record['key_to_source'] not in [None, '']:
        if '@' not in record['key_to_source']:
            record['key_to_source'] = ''
            record['source'] = element.get_multi_line_value()

    for child in element.get_child_elements():
        if child.get_tag() in CITATION_TAGS:
            record[CITATION_TAGS[child.get_tag()]] = child.get_value()
            continue

        if child.get_tag() == tags.GEDCOM_TAG_EVENT:
            record['event'] = child.get_value()
            for gchild in child.get_child_elements():
                if gchild.get_tag() == tags.GEDCOM_TAG_ROLE:
                    record['role'] = gchild.get_value()
            continue

        if child.get_tag() == tags.GEDCOM_TAG_DATA:
            for gchild in child.get_child_elements():
                if gchild.get_tag() == tags.GEDCOM_TAG_DATE:
                    record['date'] = gchild.get_value()
                    continue
                if gchild.get_tag() == tags.GEDCOM_TAG_TEXT:
                    record['text'] = gchild.get_multi_line_value()
            continue

        if child.get_tag() == tags.GEDCOM_TAG_OBJECT:
            record['media'].append(multimedia_link(child))
            continue

        if child.get_tag() == tags.GEDCOM_TAG_NOTE:
            record['notes'].append(note_structure(child))
            continue

        if child.get_tag() == tags.GEDCOM_TAG_TEXT:
            record['text'] = child.get_multi_line_value()

    return record
