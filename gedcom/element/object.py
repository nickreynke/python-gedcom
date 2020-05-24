# -*- coding: utf-8 -*-

# Python GEDCOM Parser
#
# Copyright (C) 2020 Christopher Horn (cdhorn at embarqmail dot com)
# Copyright (C) 2018 Damon Brodie (damon.brodie at gmail.com)
# Copyright (C) 2018-2019 Nicklas Reincke (contact at reynke.com)
# Copyright (C) 2016 Andreas Oberritter
# Copyright (C) 2012 Madeleine Price Ball
# Copyright (C) 2005 Daniel Zappala (zappala at cs.byu.edu)
# Copyright (C) 2005 Brigham Young University
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
GEDCOM element for a `MULTIMEDIA_RECORD` media record identified by the
`gedcom.tags.GEDCOM_TAG_OBJECT` tag.
"""

import gedcom.tags as tags
from gedcom.element.element import Element
from gedcom.subparsers.note_structure import note_structure
from gedcom.subparsers.source_citation import source_citation
from gedcom.subparsers.change_date import change_date
from gedcom.subparsers.user_reference_number import user_reference_number


class ObjectElement(Element):
    """Element associated with a `MULTIMEDIA_RECORD`"""

    def get_tag(self) -> str:
        return tags.GEDCOM_TAG_OBJECT

    def get_record(self) -> dict:
        """Parse and return the full record in dictionary format.
        """
        record = {
            'key_to_object': self.get_pointer(),
            'file': '',
            'format': '',
            'type': '',
            'title': '',
            'references': [],
            'record_id': '',
            'citations': [],
            'notes': [],
            'change_date': {}
        }
        for child in self.get_child_elements():
            if child.get_tag() == tags.GEDCOM_TAG_FILE:
                record['file'] = child.get_value()

                for gchild in child.get_child_elements():
                    if gchild.get_tag() == tags.GEDCOM_TAG_FORMAT:
                        record['format'] = gchild.get_value()

                        for ggchild in gchild.get_child_elements():
                            if ggchild.get_tag() == tags.GEDCOM_TAG_TYPE:
                                record['type'] = ggchild.get_value()
                        continue

                    if gchild.get_tag() == tags.GEDCOM_TAG_TITLE:
                        record['title'] = gchild.get_value()
                        continue
                continue

            if child.get_tag() == tags.GEDCOM_TAG_FORMAT:
                record['format'] = child.get_value()
                continue

            if child.get_tag() == tags.GEDCOM_TAG_TYPE:
                record['type'] = child.get_value()
                continue

            if child.get_tag() == tags.GEDCOM_TAG_NOTE:
                record['notes'].append(note_structure(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_SOURCE:
                record['citations'].append(source_citation(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_REFERENCE:
                record['references'].append(user_reference_number(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_REC_ID_NUMBER:
                record['record_id'] = child.get_value()
                continue

            if child.get_tag() == tags.GEDCOM_TAG_CHANGE:
                record['change_date'] = change_date(child)

        return record
