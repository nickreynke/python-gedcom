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
Substructure parser for a `SOURCE_CITATION` record.

This is anchored by the `gedcom.tags.GEDCOM_TAG_SOURCE` tag.
"""

import gedcom.tags as tags
from gedcom.element.element import Element
from gedcom.subparsers.multimedia_link import multimedia_link
from gedcom.subparsers.note_structure import note_structure

CITATION_TAGS = {
    tags.GEDCOM_TAG_PAGE: 'page',
    tags.GEDCOM_TAG_DATE: 'date',
    tags.GEDCOM_TAG_QUALITY_OF_DATA: 'quality',
    tags.GEDCOM_PROGRAM_DEFINED_TAG_APID: 'apid'
}


def source_citation(element: Element) -> dict:
    """Parse and extract a `SOURCE_CITATION` structure.

    The `element` should contain the `gedcom.tags.GEDCOM_TAG_SOURCE` tag.
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
