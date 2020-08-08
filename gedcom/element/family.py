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
GEDCOM element for a `FAM_RECORD` family record identified by the
`gedcom.tags.GEDCOM_TAG_FAMILY` tag.
"""

import gedcom.tags as tags
from gedcom.element.element import Element
from gedcom.subparsers.family_event_structure import family_event_structure
from gedcom.subparsers.change_date import change_date
from gedcom.subparsers.lds_spouse_sealing import lds_spouse_sealing
from gedcom.subparsers.note_structure import note_structure
from gedcom.subparsers.source_citation import source_citation
from gedcom.subparsers.multimedia_link import multimedia_link
from gedcom.subparsers.user_reference_number import user_reference_number

FAMILY_SINGLE_TAGS = {
    tags.GEDCOM_TAG_WIFE: 'key_to_wife',
    tags.GEDCOM_TAG_HUSBAND: 'key_to_husband',
    tags.GEDCOM_TAG_CHILDREN_COUNT: 'number_of_children',
    tags.GEDCOM_TAG_RESTRICTION: 'restriction',
    tags.GEDCOM_TAG_REC_ID_NUMBER: 'record_id'
}


class FamilyElement(Element):
    """Element associated with a `FAM_RECORD`"""

    def get_tag(self) -> str:
        return tags.GEDCOM_TAG_FAMILY

    def get_record(self) -> dict:
        """Parse and return the full record in dictionary format.
        """
        record = {
            'key_to_family': self.get_pointer(),
            'restriction': '',
            'events': family_event_structure(self),
            'key_to_husband': '',
            'key_to_wife': '',
            'children': [],
            'number_of_children': '',
            'submitters': [],
            'references': [],
            'record_id': '',
            'change_date': {},
            'notes': [],
            'citations': [],
            'media': []
        }
        lds_events = lds_spouse_sealing(self)
        if len(lds_events) > 0:
            for event in lds_events:
                record['events'].append(event)

        for child in self.get_child_elements():
            if child.get_tag() in FAMILY_SINGLE_TAGS:
                record[FAMILY_SINGLE_TAGS[child.get_tag()]] = child.get_value()
                continue

            if child.get_tag() == tags.GEDCOM_TAG_CHILD:
                entry = {
                    'key_to_child': child.get_value(),
                    'relationship_to_father': '',
                    'relationship_to_mother': ''
                }
                for gchild in child.get_child_elements():
                    if gchild.get_tag() == tags.GEDCOM_PROGRAM_DEFINED_TAG_FREL:
                        entry['relationship_to_father'] = gchild.get_value()
                        continue

                    if gchild.get_tag() == tags.GEDCOM_PROGRAM_DEFINED_TAG_MREL:
                        entry['relationship_to_mother'] = gchild.get_value()

                record['children'].append(entry)
                continue

            if child.get_tag() == tags.GEDCOM_TAG_NOTE:
                record['notes'].append(note_structure(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_SOURCE:
                record['citations'].append(source_citation(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_OBJECT:
                record['media'].append(multimedia_link(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_REFERENCE:
                record['references'].append(user_reference_number(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_CHANGE:
                record['change_date'] = change_date(child)
                continue

            if child.get_tag() == tags.GEDCOM_TAG_SUBMITTER:
                record['submitters'].append(child.get_value())
                continue

        return record
