# -*- coding: utf-8 -*-

# Python GEDCOM Parser
#
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
Base GEDCOM element.
"""

from sys import version_info
from typing import List

from gedcom.helpers import deprecated
import gedcom.tags


class Element(object):
    """GEDCOM element.

    Each line in a GEDCOM file is an element with the format:

    `level [pointer] tag [value]`

    where `level` and `tag` are required, and `pointer` and `value` are
    optional.  Elements are arranged hierarchically according to their
    level, and elements with a level of zero are at the top level.
    Elements with a level greater than zero are children of their
    parent.

    A pointer has the format `@pname@`, where `pname` is any sequence of
    characters and numbers. The pointer identifies the object being
    pointed to, so that any pointer included as the value of any
    element points back to the original object.  For example, an
    element may have a `FAMS` tag whose value is `@F1@`, meaning that this
    element points to the family record in which the associated person
    is a spouse. Likewise, an element with a tag of `FAMC` has a value
    that points to a family record in which the associated person is a
    child.

    See a GEDCOM file for examples of tags and their values.

    Tags available to an element are seen here: `gedcom.tags`
    """

    def __init__(self, level: int, pointer: str, tag: str, value: str,
                 crlf: str = "\n", multi_line: bool = True):
        # basic element info
        self.__level = level
        self.__pointer = pointer
        self.__tag = tag
        self.__value = value
        self.__crlf = crlf

        # structuring
        self.__children = []
        self.__parent = None

        if multi_line:
            self.set_multi_line_value(value)

    def get_level(self) -> int:
        """Returns the level of this element from within the GEDCOM file.
        """
        return self.__level

    def get_pointer(self) -> str:
        """Returns the pointer of this element from within the GEDCOM file.
        """
        return self.__pointer

    def get_tag(self) -> str:
        """Returns the tag of this element from within the GEDCOM file.
        """
        return self.__tag

    def get_value(self) -> str:
        """Return the value of this element from within the GEDCOM file.
        """
        return self.__value

    def set_value(self, value: str):
        """Sets the value of this element.
        """
        self.__value = value

    def get_multi_line_value(self) -> str:
        """Returns the value of this element including concatenations or continuations.
        """
        result = self.get_value()
        last_crlf = self.__crlf
        for element in self.get_child_elements():
            tag = element.get_tag()
            if tag == gedcom.tags.GEDCOM_TAG_CONCATENATION:
                result += element.get_value()
                last_crlf = element.__crlf
            elif tag == gedcom.tags.GEDCOM_TAG_CONTINUED:
                result += last_crlf + element.get_value()
                last_crlf = element.__crlf
        return result

    def __available_characters(self) -> int:
        """Get the number of available characters of the elements original string
        """
        element_characters = len(self.to_gedcom_string())
        return 0 if element_characters > 255 else 255 - element_characters

    def __line_length(self, line: str) -> int:
        """Return line length.
        """
        total_characters = len(line)
        available_characters = self.__available_characters()
        if total_characters <= available_characters:
            return total_characters
        spaces = 0
        while spaces < available_characters and line[available_characters - spaces - 1] == ' ':
            spaces += 1
        if spaces == available_characters:
            return available_characters
        return available_characters - spaces

    def __set_bounded_value(self, value: str) -> int:
        """@TODO Write docs.
        """
        line_length = self.__line_length(value)
        self.set_value(value[:line_length])
        return line_length

    def __add_bounded_child(self, tag: str, value: str) -> int:
        """@TODO Write docs.
        """
        child = self.new_child_element(tag)
        return child.__set_bounded_value(value)

    def __add_concatenation(self, string: str):
        """@TODO Write docs.
        """
        index = 0
        size = len(string)
        while index < size:
            index += self.__add_bounded_child(gedcom.tags.GEDCOM_TAG_CONCATENATION, string[index:])

    def set_multi_line_value(self, value: str):
        """Sets the value of this element, adding concatenation and continuation lines
        when necessary.
        """
        self.set_value('')
        self.get_child_elements()[:] = [child for child in self.get_child_elements() if
                                        child.get_tag() not in
                                        (gedcom.tags.GEDCOM_TAG_CONCATENATION,
                                         gedcom.tags.GEDCOM_TAG_CONTINUED)]

        lines = value.splitlines()
        if lines:
            line = lines.pop(0)
            n = self.__set_bounded_value(line)
            self.__add_concatenation(line[n:])

            for line in lines:
                n = self.__add_bounded_child(gedcom.tags.GEDCOM_TAG_CONTINUED, line)
                self.__add_concatenation(line[n:])

    def get_child_elements(self) -> List[Element]:
        """Returns the direct child elements of this element.
        """
        return self.__children

    def new_child_element(self, tag: str, pointer: str = "",
                          value: str = "") -> Element:
        """Creates and returns a new child element of this element.
        """
        from gedcom.element.family import FamilyElement
        from gedcom.element.individual import IndividualElement
        from gedcom.element.note import NoteElement
        from gedcom.element.object import ObjectElement
        from gedcom.element.repository import RepositoryElement
        from gedcom.element.source import SourceElement
        from gedcom.element.submitter import SubmitterElement
        from gedcom.element.submission import SubmissionElement
        from gedcom.element.header import HeaderElement

        # Differentiate between the type of the new child element
        if tag == gedcom.tags.GEDCOM_TAG_FAMILY:
            child_element = FamilyElement(self.get_level() + 1, pointer, tag,
                                          value, self.__crlf)
        elif tag == gedcom.tags.GEDCOM_TAG_INDIVIDUAL:
            child_element = IndividualElement(self.get_level() + 1, pointer, tag,
                                              value, self.__crlf)
        elif tag == gedcom.tags.GEDCOM_TAG_NOTE:
            child_element = NoteElement(self.get_level() + 1, pointer, tag,
                                        value, self.__crlf)
        elif tag == gedcom.tags.GEDCOM_TAG_OBJECT:
            child_element = ObjectElement(self.get_level() + 1, pointer, tag,
                                          value, self.__crlf)
        elif tag == gedcom.tags.GEDCOM_TAG_REPOSITORY:
            child_element = RepositoryElement(self.get_level() + 1, pointer, tag,
                                              value, self.__crlf)
        elif tag == gedcom.tags.GEDCOM_TAG_SOURCE:
            child_element = SourceElement(self.get_level() + 1, pointer, tag,
                                          value, self.__crlf)
        elif tag == gedcom.tags.GEDCOM_TAG_SUBMITTER:
            child_element = SubmitterElement(self.get_level() + 1, pointer, tag,
                                             value, self.__crlf)
        elif tag == gedcom.tags.GEDCOM_TAG_SUBMISSION:
            child_element = SubmissionElement(self.get_level() + 1, pointer, tag,
                                              value, self.__crlf)
        elif tag == gedcom.tags.GEDCOM_TAG_HEADER:
            child_element = HeaderElement(self.get_level() + 1, pointer, tag,
                                          value, self.__crlf)
        else:
            child_element = Element(self.get_level() + 1, pointer, tag,
                                    value, self.__crlf)

        self.add_child_element(child_element)

        return child_element

    def add_child_element(self, element: Element):
        """Adds a child element to this element.
        """
        self.get_child_elements().append(element)
        element.set_parent_element(self)

        return element

    def get_parent_element(self) -> Element:
        """Returns the parent element of this element.
        """
        return self.__parent

    def set_parent_element(self, element: Element):
        """Adds a parent element to this element.

        There's usually no need to call this method manually,
        `add_child_element()` calls it automatically.
        """
        self.__parent = element

    @deprecated
    def get_individual(self) -> str:
        """Returns this element and all of its sub-elements represented as a GEDCOM string.
        ::deprecated:: As of version 1.0.0 use `to_gedcom_string()` method instead
        """
        return self.to_gedcom_string(True)

    def to_gedcom_string(self, recursive: bool = False) -> str:
        """Formats this element and optionally all of its sub-elements into a GEDCOM string.
        """

        result = str(self.get_level())

        if self.get_pointer() != "":
            result += ' ' + self.get_pointer()

        result += ' ' + self.get_tag()

        if self.get_value() != "":
            result += ' ' + self.get_value()

        result += self.__crlf

        if self.get_level() < 0:
            result = ''

        if recursive:
            for child_element in self.get_child_elements():
                result += child_element.to_gedcom_string(True)

        return result

    def __str__(self) -> str:
        """:rtype: str"""
        if version_info[0] >= 3:
            return self.to_gedcom_string()

        return self.to_gedcom_string().encode('utf-8-sig')
