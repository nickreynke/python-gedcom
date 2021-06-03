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
GEDCOM element for a `MULTIMEDIA_RECORD` media record identified by the
`gedcom.tags.GEDCOM_TAG_OBJECT` tag.
"""

import gedcom.tags as tags
from gedcom.elements.element import Element
from gedcom.subparsers.note_structure import parse_note_structure
from gedcom.subparsers.source_citation import parse_source_citation
from gedcom.subparsers.change_date import parse_change_date
from gedcom.subparsers.user_reference_number import parse_user_reference_number


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
                record['notes'].append(parse_note_structure(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_SOURCE:
                record['citations'].append(parse_source_citation(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_REFERENCE:
                record['references'].append(parse_user_reference_number(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_REC_ID_NUMBER:
                record['record_id'] = child.get_value()
                continue

            if child.get_tag() == tags.GEDCOM_TAG_CHANGE:
                record['change_date'] = parse_change_date(child)

        return record
