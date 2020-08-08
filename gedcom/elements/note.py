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
GEDCOM element for a `NOTE_RECORD` note record identified by the
`gedcom.tags.GEDCOM_TAG_NOTE` tag.
"""

import gedcom.tags as tags
from gedcom.elements.element import Element
from gedcom.subparsers.source_citation import parse_source_citation
from gedcom.subparsers.change_date import parse_change_date
from gedcom.subparsers.user_reference_number import parse_user_reference_number


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
                record['references'].append(parse_user_reference_number(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_REC_ID_NUMBER:
                record['record_id'] = child.get_value()
                continue

            if child.get_tag() == tags.GEDCOM_TAG_SOURCE:
                record['citations'].append(parse_source_citation(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_CHANGE:
                record['change_date'] = parse_change_date(child)

        return record
