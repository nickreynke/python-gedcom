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
GEDCOM element for a `SUBMITTER_RECORD` submitter record identified by the
`gedcom.tags.GEDCOM_TAG_SUBMITTER` tag.
"""

import gedcom.tags as tags
from gedcom.element.element import Element
from gedcom.subparsers.address_structure import address_structure
from gedcom.subparsers.note_structure import note_structure
from gedcom.subparsers.change_date import change_date
from gedcom.subparsers.multimedia_link import multimedia_link

class SubmitterElement(Element):
    """Element associated with a `SUBMITTER_RECORD`"""

    def get_tag(self):
        return tags.GEDCOM_TAG_SUBMITTER

    def get_record(self):
        """Parse and return the record in dictionary format
        :rtype: dict
        """
        record = {
            'key_to_submitter': self.get_pointer(),
            'name': '',
            'address': {},
            'media': [],
            'language': '',
            'registered_file_number': '',
            'record_id': '',
            'notes': [],
            'change_date': {}
        }
        for child in self.get_child_elements():
            if child.get_tag() == tags.GEDCOM_TAG_NAME:
                record['name'] = child.get_value()
                continue

            if child.get_tag() == tags.GEDCOM_TAG_ADDRESS:
                record['address'] = address_structure(self)
                continue

            if child.get_tag() == tags.GEDCOM_TAG_NOTE:
                record['notes'].append(note_structure(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_OBJECT:
                record['media'].append(multimedia_link(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_LANGUAGE:
                record['language'] = child.get_value()
                continue

            if child.get_tag() == tags.GEDCOM_TAG_REC_FILE_NUMBER:
                record['registered_file_number'] = child.get_value()
                continue

            if child.get_tag() == tags.GEDCOM_TAG_REC_ID_NUMBER:
                record['record_id'] = child.get_value()
                continue

            if child.get_tag() == tags.GEDCOM_TAG_CHANGE:
                record['change_date'] = change_date(child)

        return record
