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
GEDCOM element for a `HEADER` header record identified by the
`gedcom.tags.GEDCOM_TAG_HEADER` tag.
"""

import gedcom.tags as tags
from gedcom.elements.element import Element
from gedcom.subparsers.address_structure import address_structure
from gedcom.subparsers.note_structure import note_structure

HEADER_TAGS = {
    tags.GEDCOM_TAG_DESTINATION: 'destination',
    tags.GEDCOM_TAG_SUBMITTER: 'key_to_submitter',
    tags.GEDCOM_TAG_SUBMISSION: 'key_to_submission',
    tags.GEDCOM_TAG_FILE: 'file',
    tags.GEDCOM_TAG_COPYRIGHT: 'copyright',
    tags.GEDCOM_TAG_LANGUAGE: 'language',
    tags.GEDCOM_PROGRAM_DEFINED_TAG_HOME_PERSON: 'key_to_home_person'
}


class HeaderElement(Element):
    """Element associated with a `HEADER`"""

    def get_tag(self) -> str:
        return tags.GEDCOM_TAG_HEADER

    def get_record(self) -> dict:
        """Parse and return the full record in dictionary format.
        """
        record = {
            'source': '',
            'product': {
                'version': '',
                'name': '',
                'corporation': '',
                'address': {}
            },
            'data': {
                'source_data': '',
                'published': '',
                'copyright': ''
            },
            'destination': '',
            'transmission_date': '',
            'transmission_time': '',
            'key_to_submitter': '',
            'key_to_submission': '',
            'file': '',
            'copyright': '',
            'gedcom': {
                'version': '',
                'format': '',
            },
            'character_set': '',
            'character_set_version': '',
            'language': '',
            'place_hierarchy': '',
            'key_to_home_person': '',
            'notes': []
        }
        for child in self.get_child_elements():
            if child.get_tag() == tags.GEDCOM_TAG_SOURCE:
                record['source'] = child.get_value()
                for gchild in child.get_child_elements():
                    if gchild.get_tag() == tags.GEDCOM_TAG_VERSION:
                        record['product']['version'] = gchild.get_value()
                        continue

                    if gchild.get_tag() == tags.GEDCOM_TAG_NAME:
                        record['product']['name'] = gchild.get_value()
                        continue

                    if gchild.get_tag() == tags.GEDCOM_TAG_CORPORATE:
                        record['product']['corporation'] = gchild.get_value()

                        for ggchild in gchild.get_child_elements():
                            if ggchild.get_tag() == tags.GEDCOM_TAG_ADDRESS:
                                record['product']['address'] = address_structure(gchild)
                        continue

                    if gchild.get_tag() == tags.GEDCOM_TAG_DATA:
                        record['data']['source_data'] = gchild.get_value()
                        for ggchild in gchild.get_child_elements():
                            if ggchild.get_tag() == tags.GEDCOM_TAG_DATE:
                                record['data']['published'] = ggchild.get_value()
                                continue

                            if ggchild.get_tag() == tags.GEDCOM_TAG_COPYRIGHT:
                                record['data']['copyright'] = ggchild.get_multi_line_value()
                        continue
                continue

            if child.get_tag() in HEADER_TAGS:
                record[HEADER_TAGS[child.get_tag()]] = child.get_value()
                continue

            if child.get_tag() == tags.GEDCOM_TAG_DATE:
                record['transmission_date'] = child.get_value()
                for gchild in child.get_child_elements():
                    if gchild.get_tag() == tags.GEDCOM_TAG_TIME:
                        record['transmission_time'] = gchild.get_value()
                continue

            if child.get_tag() == tags.GEDCOM_TAG_GEDCOM:
                for gchild in child.get_child_elements():
                    if gchild.get_tag() == tags.GEDCOM_TAG_VERSION:
                        record['gedcom']['version'] = gchild.get_value()
                        continue

                    if gchild.get_tag() == tags.GEDCOM_TAG_FORMAT:
                        record['gedcom']['format'] = gchild.get_value()
                continue

            if child.get_tag() == tags.GEDCOM_TAG_CHARACTER:
                record['character_set'] = child.get_value()
                for gchild in child.get_child_elements():
                    if gchild.get_tag() == tags.GEDCOM_TAG_VERSION:
                        record['character_set_version'] = gchild.get_value()
                continue

            if child.get_tag() == tags.GEDCOM_TAG_PLACE:
                for gchild in child.get_child_elements():
                    if gchild.get_tag() == tags.GEDCOM_TAG_FORMAT:
                        record['place_hierarchy'] = gchild.get_value()
                continue

            if child.get_tag() == tags.GEDCOM_TAG_NOTE:
                record['notes'].append(note_structure(child))

        return record
