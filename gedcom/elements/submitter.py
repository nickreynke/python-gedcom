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
GEDCOM element for a `SUBMITTER_RECORD` submitter record identified by the
`gedcom.tags.GEDCOM_TAG_SUBMITTER` tag.
"""

import gedcom.tags as tags
from gedcom.elements.element import Element
from gedcom.subparsers.address_structure import parse_address_structure
from gedcom.subparsers.note_structure import parse_note_structure
from gedcom.subparsers.change_date import parse_change_date
from gedcom.subparsers.multimedia_link import parse_multimedia_link


class SubmitterElement(Element):
    """Element associated with a `SUBMITTER_RECORD`"""

    def get_tag(self) -> str:
        return tags.GEDCOM_TAG_SUBMITTER

    def get_record(self) -> dict:
        """Parse and return the record in dictionary format
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
                record['address'] = parse_address_structure(self)
                continue

            if child.get_tag() == tags.GEDCOM_TAG_NOTE:
                record['notes'].append(parse_note_structure(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_OBJECT:
                record['media'].append(parse_multimedia_link(child))
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
                record['change_date'] = parse_change_date(child)

        return record
