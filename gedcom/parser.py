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
Module containing the actual `gedcom.parser.Parser` used to generate elements
out of each line - which can in return be manipulated.
"""

import re as regex

import gedcom.tags as tags
import gedcom.standards as standards

from gedcom.detect import get_encoding, get_version
from gedcom.element.element import Element
from gedcom.element.header import HeaderElement
from gedcom.element.family import FamilyElement
from gedcom.element.individual import IndividualElement
from gedcom.element.note import NoteElement
from gedcom.element.object import ObjectElement
from gedcom.element.source import SourceElement
from gedcom.element.submission import SubmissionElement
from gedcom.element.submitter import SubmitterElement
from gedcom.element.repository import RepositoryElement
from gedcom.element.root import RootElement

from gedcom.errors import GedcomVersionUnsupportedError
from gedcom.errors import GedcomFormatUnsupportedError
from gedcom.errors import GedcomFormatViolationError

ERROR_TEMPLATE = "Line <{0}:{1}> of document violates GEDCOM format {2}\nSee: {3}"

RECORD_ELEMENTS = {
    tags.GEDCOM_TAG_HEADER: HeaderElement,
    tags.GEDCOM_TAG_INDIVIDUAL: IndividualElement,
    tags.GEDCOM_TAG_FAMILY: FamilyElement,
    tags.GEDCOM_TAG_NOTE: NoteElement,
    tags.GEDCOM_TAG_OBJECT: ObjectElement,
    tags.GEDCOM_TAG_SOURCE: SourceElement,
    tags.GEDCOM_TAG_SUBMISSION: SubmissionElement,
    tags.GEDCOM_TAG_SUBMITTER: SubmitterElement,
    tags.GEDCOM_TAG_REPOSITORY: RepositoryElement
}


class Parser():
    """Parses and manipulates GEDCOM 5.5 format data

    For documentation of the GEDCOM 5.5 format, see:
    http://homepages.rootsweb.ancestry.com/~pmcbride/gedcom/55gctoc.htm

    This parser reads and parses a GEDCOM file.

    Elements may be accessed via:

    * a `list` through `gedcom.parser.Parser.get_element_list()`
    * a `dict` through `gedcom.parser.Parser.get_element_dictionary()`
    """

    def __init__(self):
        self.__element_list = []
        self.__element_dictionary = {}
        self.__root_element = RootElement()

    def invalidate_cache(self):
        """Empties the element list and dictionary to cause
        `gedcom.parser.Parser.get_element_list()` and
        `gedcom.parser.Parser.get_element_dictionary()` to return updated data.

        The update gets deferred until each of the methods actually gets called.
        """
        self.__element_list = []
        self.__element_dictionary = {}

    def get_element_list(self):
        """Returns a list containing all elements from within the GEDCOM file

        By default elements are in the same order as they appeared in the file.

        This list gets generated on-the-fly, but gets cached. If the database
        was modified, you should call `gedcom.parser.Parser.invalidate_cache()` once
        to let this method return updated data.

        Consider using `gedcom.parser.Parser.get_root_element()` or
        `gedcom.parser.Parser.get_root_child_elements()` to access
        the hierarchical GEDCOM tree, unless you rarely modify the database.

        :rtype: list of Element
        """
        if not self.__element_list:
            for element in self.get_root_child_elements():
                self.__build_list(element, self.__element_list)
        return self.__element_list

    def get_element_dictionary(self):
        """Returns a dictionary containing all elements, identified by a pointer,
        from within the GEDCOM file

        Only elements identified by a pointer are listed in the dictionary.
        The keys for the dictionary are the pointers.

        This dictionary gets generated on-the-fly, but gets cached. If the
        database was modified, you should call `invalidate_cache()` once to let
        this method return updated data.

        :rtype: dict of Element
        """
        if not self.__element_dictionary:
            self.__element_dictionary = {
                element.get_pointer():
                element for element in self.get_root_child_elements() if element.get_pointer()
            }

        return self.__element_dictionary

    def get_root_element(self):
        """Returns a virtual root element containing all logical records as children

        When printed, this element converts to an empty string.

        :rtype: RootElement
        """
        return self.__root_element

    def get_root_child_elements(self):
        """Returns a list of logical records in the GEDCOM file

        By default, elements are in the same order as they appeared in the file.

        :rtype: list of Element
        """
        return self.get_root_element().get_child_elements()

    def parse_file(self, file_path, strict=True):
        """Opens and parses a file, from the given file path, as GEDCOM 5.5 formatted data
        :type file_path: str
        :type strict: bool
        """
        codec = get_encoding(file_path)
        real_version, reported_version, reported_format = get_version(file_path, codec)

        if reported_version == '5.5.5':
            errmsg = "This parser does not properly support the GEDCOM " + reported_version + \
                " standard at this time\nSee: {0}".format(standards.GEDCOM_5_5_5)
            raise GedcomVersionUnsupportedError(errmsg)

        if reported_format not in ['LINEAGE-LINKED', 'LINEAGE_LINKED',
                                   'LINAGE-LINKED', 'Lineage - Linked']:
            errmsg = "This parser does not recognize the GEDCOM format " + reported_format + \
                " at this time\nSee: {0}".format(standards.GEDCOM_5_5_5)
            raise GedcomFormatUnsupportedError(errmsg)

        with open(file_path, 'r', encoding=codec) as gedcom_stream:
            self.parse(gedcom_stream, strict)

    def parse(self, gedcom_stream, strict=True):
        """Parses a stream, or an array of lines, as GEDCOM 5.5 formatted data
        :type gedcom_stream: a file stream, or str array of lines with new line at the end
        :type strict: bool
        """
        self.invalidate_cache()
        self.__root_element = RootElement()

        line_number = 1
        last_element = self.get_root_element()

        for line in gedcom_stream:
            last_element = self.__parse_line(line_number, line, last_element, strict)
            line_number += 1

    # Private methods

    @staticmethod
    def __parse_line(line_number, line, last_element, strict=True):
        """Parse a line from a GEDCOM 5.5 formatted document

        Each line should have the following (bracketed items optional):
        level + ' ' + [pointer + ' ' +] tag + [' ' + line_value]

        :type line_number: int
        :type line: str
        :type last_element: Element
        :type strict: bool

        :rtype: Element
        """

        # Level must start with non-negative int, no leading zeros.
        level_regex = '^(0|[1-9]+[0-9]*) '

        # Pointer optional, if it exists it must be flanked by `@`
        pointer_regex = '(@[^@]+@ |)'

        # Tag must be an alphanumeric string
        tag_regex = '([A-Za-z0-9_]+)'

        # Value optional, consists of anything after a space to end of line
        value_regex = '( [^\n\r]*|)'

        # End of line defined by `\n` or `\r`
        end_of_line_regex = '([\r\n]{1,2})'

        # Complete regex
        gedcom_line_regex = level_regex + pointer_regex + tag_regex + \
            value_regex + end_of_line_regex
        regex_match = regex.match(gedcom_line_regex, line)

        if regex_match is None:
            if strict:
                errmsg = ERROR_TEMPLATE.format(line_number, line, '5.5.1', standards.GEDCOM_5_5_1)
                raise GedcomFormatViolationError(errmsg)

            # Quirk check - see if this is a line without a CRLF (which could be the last line)
            last_line_regex = level_regex + pointer_regex + tag_regex + value_regex
            regex_match = regex.match(last_line_regex, line)
            if regex_match is not None:
                line_parts = regex_match.groups()

                level = int(line_parts[0])
                pointer = line_parts[1].rstrip(' ')
                tag = line_parts[2]
                value = line_parts[3][1:]
                crlf = '\n'
            else:
                # Quirk check - Sometimes a gedcom has a text field with a CR.
                # This creates a line without the standard level and pointer.
                # If this is detected then turn it into a CONC or CONT.
                line_regex = '([^\n\r]*|)'
                cont_line_regex = line_regex + end_of_line_regex
                regex_match = regex.match(cont_line_regex, line)
                line_parts = regex_match.groups()
                level = last_element.get_level()
                tag = last_element.get_tag()
                pointer = None
                value = line_parts[0][1:]
                crlf = line_parts[1]
                if tag not in [tags.GEDCOM_TAG_CONTINUED, tags.GEDCOM_TAG_CONCATENATION]:
                    # Increment level and change this line to a CONC
                    level += 1
                    tag = tags.GEDCOM_TAG_CONCATENATION
        else:
            line_parts = regex_match.groups()

            level = int(line_parts[0])
            pointer = line_parts[1].rstrip(' ')
            tag = line_parts[2]
            value = line_parts[3][1:]
            crlf = line_parts[4]

        # Check level: should never be more than one higher than previous line.
        if level > last_element.get_level() + 1:
            errmsg = "Line {0} of document violates GEDCOM format 5.5.1\n".format(line_number) + \
                "Lines must be no more than one level higher than previous line.\n" + \
                "See: {0}".format(standards.GEDCOM_5_5_1)
            raise GedcomFormatViolationError(errmsg)

        # Create element. Store in list and dict, create children and parents.
        if tag in RECORD_ELEMENTS:
            element = RECORD_ELEMENTS[tag](level, pointer, tag, value, crlf, multi_line=False)
        else:
            element = Element(level, pointer, tag, value, crlf, multi_line=False)

        # Start with last element as parent, back up if necessary.
        parent_element = last_element

        while parent_element.get_level() > level - 1:
            parent_element = parent_element.get_parent_element()

        # Add child to parent & parent to child.
        parent_element.add_child_element(element)

        return element

    def __build_list(self, element, element_list):
        """Recursively add elements to a list containing elements
        :type element: Element
        :type element_list: list of Element
        """
        element_list.append(element)
        for child in element.get_child_elements():
            self.__build_list(child, element_list)
