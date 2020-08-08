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
GEDCOM element for a `SUBMISSION_RECORD` submission record identified by the
`gedcom.tags.GEDCOM_TAG_SUBMISSION` tag.
"""

import gedcom.tags as tags
from gedcom.elements.element import Element
from gedcom.subparsers.note_structure import note_structure
from gedcom.subparsers.change_date import change_date

SUBMISSION_TAGS = {
    tags.GEDCOM_TAG_SUBMITTER: 'key_to_submitter',
    tags.GEDCOM_TAG_FAMILY_FILE: 'family_file',
    tags.GEDCOM_TAG_TEMPLE: 'temple',
    tags.GEDCOM_TAG_ANCESTORS: 'generations_of_ancestors',
    tags.GEDCOM_TAG_DESCENDANTS: 'generations_of_decendants',
    tags.GEDCOM_TAG_ORDINANCE: 'ordinance_process_flag',
    tags.GEDCOM_TAG_REC_ID_NUMBER: 'record_id'
}


class SubmissionElement(Element):
    """Element associated with a `SUBMISSION_RECORD`"""

    def get_tag(self) -> str:
        return tags.GEDCOM_TAG_SUBMISSION

    def get_record(self) -> dict:
        """Parse and return the record in dictionary format
        """
        record = {
            'key_to_submission': self.get_pointer(),
            'key_to_submitter': '',
            'family_file': '',
            'temple': '',
            'generations_of_ancestors': '',
            'generations_of_descendants': '',
            'ordinance_process_flag': '',
            'record_id': '',
            'notes': [],
            'change_date': {}
        }
        for child in self.get_child_elements():
            if child.get_tag() in SUBMISSION_TAGS:
                record[SUBMISSION_TAGS[child.get_tag()]] = child.get_value()
                continue

            if child.get_tag() == tags.GEDCOM_TAG_NOTE:
                record['notes'].append(note_structure(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_CHANGE:
                record['change_date'] = change_date(child)

        return record
