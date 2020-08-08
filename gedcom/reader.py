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
Module containing a `gedcom.reader.Reader` with higher order methods than the
base `gedcom.parser.Parser` for extracting records as structured data.
"""

from typing import Union

from gedcom.parser import Parser
from gedcom.elements.header import HeaderElement
from gedcom.elements.individual import IndividualElement
from gedcom.elements.family import FamilyElement
from gedcom.elements.note import NoteElement
from gedcom.elements.object import ObjectElement
from gedcom.elements.source import SourceElement
from gedcom.elements.submission import SubmissionElement
from gedcom.elements.submitter import SubmitterElement
from gedcom.elements.repository import RepositoryElement

ELEMENT_TYPES = {
    'header': HeaderElement,
    'individual': IndividualElement,
    'family': FamilyElement,
    'note': NoteElement,
    'media': ObjectElement,
    'source': SourceElement,
    'submission': SubmissionElement,
    'submitter': SubmitterElement,
    'repository': RepositoryElement
}

RECORD_KEYS = {
    'header': None,
    'individual': 'key_to_individual',
    'family': 'key_to_family',
    'media': 'key_to_object',
    'note': 'key_to_note',
    'source': 'key_to_source',
    'submission': 'key_to_submission',
    'submitter': 'key_to_submitter',
    'repository': 'key_to_repository'
}


class Reader(Parser):
    """Simple wrapper around the core `gedcom.parser.Parser` with methods for
    extracting parsed records as structured data.
    """

    def get_records_by_type(self, record_type: str,
                            return_output_as_list: bool = True) -> Union[list, dict]:
        """Return either a list or dictionary with all of the requested records for the
        given `gedcom.records` record type.
        """
        record_list = []
        record_dict = {}

        for element in self.get_root_child_elements():
            if isinstance(element, ELEMENT_TYPES[record_type]):
                record = element.get_record()
                if return_output_as_list:
                    record_list.append(record)
                else:
                    if RECORD_KEYS[record_type] is not None:
                        record_dict.update({record[RECORD_KEYS[record_type]]: record})
                    else:
                        record_dict.update({'@HEAD@': record})

        if return_output_as_list:
            return record_list

        return record_dict

    def get_all_records(self, return_entries_as_list: bool = True) -> dict:
        """Return a dictionary with all of the available records in the GEDCOM broken
        down by record type."""
        record_dict = {}

        for key in RECORD_KEYS:
            if return_entries_as_list:
                record_dict.update({key: []})
            else:
                record_dict.update({key: {}})

        for element in self.get_root_child_elements():
            for key in ELEMENT_TYPES:
                if isinstance(element, ELEMENT_TYPES[key]):
                    record = element.get_record()
                    if return_entries_as_list:
                        record_dict[key].append(record)
                    else:
                        if key != 'header':
                            record_dict[key].update({record[RECORD_KEYS[key]]: record})
                        else:
                            record_dict['header'].update({'@HEAD@': record})

        return record_dict
