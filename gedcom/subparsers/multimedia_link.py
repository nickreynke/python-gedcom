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
Substructure parser for the MULTIMEDIA_LINK record identified by the
`gedcom.tags.GEDCOM_TAG_OBJECT` tag.
"""

import gedcom.tags as tags

MEDIA_TAGS = {
    tags.GEDCOM_TAG_FILE: 'file',
    tags.GEDCOM_TAG_FORMAT: 'format',
    tags.GEDCOM_TAG_MEDIA: 'type',
    tags.GEDCOM_TAG_TITLE: 'title',
    tags.GEDCOM_PROGRAM_DEFINED_TAG_PHOTO: 'preferred',
    tags.GEDCOM_PROGRAM_DEFINED_TAG_PRIMARY: 'preferred'
}


def multimedia_link(element):
    """Parse and extract a MULTIMEDIA_LINK
    :rtype: dict
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
