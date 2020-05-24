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
GEDCOM element for a `NOTE_RECORD` note record identified by the
`gedcom.tags.GEDCOM_TAG_NOTE` tag.
"""

import gedcom.tags as tags
from gedcom.element.element import Element
from gedcom.subparsers.source_citation import source_citation
from gedcom.subparsers.change_date import change_date
from gedcom.subparsers.user_reference_number import user_reference_number


class NoteElement(Element):
    """Element associated with a `NOTE_RECORD`"""

    def get_tag(self) -> str:
        return tags.GEDCOM_TAG_NOTE

    def get_record(self) -> dict:
        """Parse and return the full record in dictionary format.
        """
        record = {
            'key_to_note': self.get_pointer(),
            'note': self.get_multi_line_value(),
            'references': [],
            'record_id': '',
            'citations': [],
            'change_date': {}
        }
        for child in self.get_child_elements():
            if child.get_tag() == tags.GEDCOM_TAG_REFERENCE:
                record['references'].append(user_reference_number(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_REC_ID_NUMBER:
                record['record_id'] = child.get_value()
                continue

            if child.get_tag() == tags.GEDCOM_TAG_SOURCE:
                record['citations'].append(source_citation(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_CHANGE:
                record['change_date'] = change_date(child)

        return record
