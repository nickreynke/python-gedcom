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
Substructure parser for a `MULTIMEDIA_LINK` record.

This is anchored by the `gedcom.tags.GEDCOM_TAG_OBJECT` tag.
"""

import gedcom.tags as tags
from gedcom.elements.element import Element

MEDIA_TAGS = {
    tags.GEDCOM_TAG_FILE: 'file',
    tags.GEDCOM_TAG_FORMAT: 'format',
    tags.GEDCOM_TAG_MEDIA: 'type',
    tags.GEDCOM_TAG_TITLE: 'title',
    tags.GEDCOM_PROGRAM_DEFINED_TAG_PHOTO: 'preferred',
    tags.GEDCOM_PROGRAM_DEFINED_TAG_PRIMARY: 'preferred'
}


def parse_multimedia_link(element: Element) -> dict:
    """Parse and extract a `MULTIMEDIA_LINK` structure.

    The `element` should contain the `gedcom.tags.GEDCOM_TAG_OBJECT` tag.
    """
    record = {
        'key_to_object': element.get_value(),
        'file': '',
        'format': '',
        'type': '',
        'title': '',
        'preferred': ''
    }
    if record['key_to_object'] not in [None, '']:
        if '@' in record['key_to_object']:
            return record

    record['key_to_object'] = ''
    for child in element.get_child_elements():
        if child.get_tag() == tags.GEDCOM_TAG_FILE:
            record['file'] = child.get_value()
            for gchild in child.get_child_elements():
                if gchild.get_tag() == tags.GEDCOM_TAG_FORMAT:
                    record['format'] = gchild.get_value()
                    for ggchild in gchild.get_child_elements():
                        if ggchild.get_tag() == tags.GEDCOM_TAG_MEDIA:
                            record['type'] = ggchild.get_value()
                    continue
            continue

        if child.get_tag() in MEDIA_TAGS:
            record[MEDIA_TAGS[child.get_tag()]] = child.get_value()

    return record
