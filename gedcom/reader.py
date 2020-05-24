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
Module containing a `gedcom.reader.Reader` with higher order methods than the
base `gedcom.parser.Parser`
"""

from gedcom.parser import Parser
from gedcom.element.header import HeaderElement
from gedcom.element.individual import IndividualElement
from gedcom.element.family import FamilyElement
from gedcom.element.note import NoteElement
from gedcom.element.object import ObjectElement
from gedcom.element.source import SourceElement
from gedcom.element.submission import SubmissionElement
from gedcom.element.submitter import SubmitterElement
from gedcom.element.repository import RepositoryElement

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
    """Simple wrapper class around the core parser with simple methods for
    extracting parsed records as structured data.
    """

    def get_records_by_type(self, record_type, output='list'):
        """Return either a list or dictionary with all the requested records
        :type: record_type: str
        :type: output: str
        :rtype: list or dict
        """
        record_list = []
        record_dict = {}

        for element in self.get_root_child_elements():
            if isinstance(element, ELEMENT_TYPES[record_type]):
                record = element.get_record()
                if output == 'list':
                    record_list.append(record)
                else:
                    if RECORD_KEYS[record_type] is not None:
                        record_dict.update({record[RECORD_KEYS[record_type]]: record})
                    else:
                        record_dict.update({'@HEAD@': record})

        if output == 'list':
            return record_list

        return record_dict

    def get_all_records(self, entries='list'):
        """Return a dictionary with all the requested records
        :type: entries: str
        :rtype: dict
        """
        record_dict = {}
        for key in RECORD_KEYS:
            if entries == 'list':
                record_dict.update({key: []})
            else:
                record_dict.update({key: {}})

        for element in self.get_root_child_elements():
            for key in ELEMENT_TYPES:
                if isinstance(element, ELEMENT_TYPES[key]):
                    record = element.get_record()
                    if entries == 'list':
                        record_dict[key].append(record)
                    else:
                        if key != 'header':
                            record_dict[key].update({record[RECORD_KEYS[key]]: record})
                        else:
                            record_dict['header'].update({'@HEAD@': record})

        return record_dict
