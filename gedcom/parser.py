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
Module containing the actual `gedcom.parser.Parser` used to generate elements
out of each line - which can in return be manipulated.
"""

import re as regex
from sys import stdout
from sys import version_info
from typing import Tuple, List, IO

import gedcom.tags as tags
import gedcom.standards as standards

from gedcom.detect import get_encoding, get_version
from gedcom.elements import ELEMENT_TYPES
from gedcom.elements.element import Element
from gedcom.elements.family import FamilyElement
from gedcom.elements.individual import IndividualElement
from gedcom.elements.root import RootElement

from gedcom.errors import GedcomVersionUnsupportedError
from gedcom.errors import GedcomFormatUnsupportedError
from gedcom.errors import GedcomFormatViolationError
from gedcom.errors import NotAnActualIndividualError
from gedcom.errors import NotAnActualFamilyError

ERROR_TEMPLATE = "Line <{0}:{1}> of document violates GEDCOM format {2}\nSee: {3}"

FAMILY_MEMBERS_TYPE_ALL = "ALL"
FAMILY_MEMBERS_TYPE_CHILDREN = tags.GEDCOM_TAG_CHILD
FAMILY_MEMBERS_TYPE_HUSBAND = tags.GEDCOM_TAG_HUSBAND
FAMILY_MEMBERS_TYPE_PARENTS = "PARENTS"
FAMILY_MEMBERS_TYPE_WIFE = tags.GEDCOM_TAG_WIFE


class Parser():
    """Parses and manipulates GEDCOM formatted data.

    For documentation of the different GEDCOM standards see the
    links defined in `gedcom.standards`

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

    def get_element_list(self) -> List[Element]:
        """Returns a list containing all elements from within the GEDCOM file.

        By default elements are in the same order as they appeared in the file.

        This list gets generated on-the-fly, but gets cached. If the database
        was modified, you should call `gedcom.parser.Parser.invalidate_cache()` once
        to let this method return updated data.

        Consider using `gedcom.parser.Parser.get_root_element()` or
        `gedcom.parser.Parser.get_root_child_elements()` to access
        the hierarchical GEDCOM tree, unless you rarely modify the database.
        """
        if not self.__element_list:
            for element in self.get_root_child_elements():
                self.__build_list(element, self.__element_list)
        return self.__element_list

    def get_element_dictionary(self) -> dict:
        """Returns a dictionary containing all elements, identified by a pointer,
        from within the GEDCOM file.

        Only elements identified by a pointer are listed in the dictionary.
        The keys for the dictionary are the pointers.

        This dictionary gets generated on-the-fly, but gets cached. If the
        database was modified, you should call `invalidate_cache()` once to let
        this method return updated data.
        """
        if not self.__element_dictionary:
            self.__element_dictionary = {
                element.get_pointer():
                element for element in self.get_root_child_elements() if element.get_pointer()
            }

        return self.__element_dictionary

    def get_root_element(self) -> RootElement:
        """Returns a virtual root element containing all logical records as children.

        When printed, this element converts to an empty string.
        """
        return self.__root_element

    def get_root_child_elements(self) -> List[Element]:
        """Returns a list of logical records in the GEDCOM file.

        By default, elements are in the same order as they appeared in the file.
        """
        return self.get_root_element().get_child_elements()

    def parse_file(self, file_path: str, strict: bool = True):
        """Opens and parses a file, from the given file path, as GEDCOM formatted data.
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

    def parse(self, gedcom_stream: IO, strict: bool = True):
        """Parses a stream, or an array of lines, as GEDCOM formatted data.
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
    def __parse_line(line_number: int, line: str, last_element: Element,
                     strict: bool = True) -> Element:
        """Parse a line from a GEDCOM formatted document.

        Each line should have the following (bracketed items optional):
        level + ' ' + [pointer + ' ' +] tag + [' ' + line_value]
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
        if tag in ELEMENT_TYPES:
            element = ELEMENT_TYPES[tag](level, pointer, tag, value, crlf, multi_line=False)
        else:
            element = Element(level, pointer, tag, value, crlf, multi_line=False)

        # Start with last element as parent, back up if necessary.
        parent_element = last_element

        while parent_element.get_level() > level - 1:
            parent_element = parent_element.get_parent_element()

        # Add child to parent & parent to child.
        parent_element.add_child_element(element)

        return element

    def __build_list(self, element: Element, element_list: List[Element]):
        """Recursively add elements to a list containing elements.
        """
        element_list.append(element)
        for child in element.get_child_elements():
            self.__build_list(child, element_list)

    # Methods for analyzing individuals and relationships between individuals

    def get_marriages(self, individual: IndividualElement) -> Tuple[str, str]:
        """Returns a list of marriages of an individual formatted as a tuple:
        (`str` date, `str` place)
        """
        marriages = []
        if not isinstance(individual, IndividualElement):
            raise NotAnActualIndividualError(
                "Operation only valid for elements with %s tag" % tags.GEDCOM_TAG_INDIVIDUAL
            )
        # Get and analyze families where individual is spouse.
        families = self.get_families(individual, tags.GEDCOM_TAG_FAMILY_SPOUSE)
        for family in families:
            for family_data in family.get_child_elements():
                if family_data.get_tag() == tags.GEDCOM_TAG_MARRIAGE:
                    date = ''
                    place = ''
                    for marriage_data in family_data.get_child_elements():
                        if marriage_data.get_tag() == tags.GEDCOM_TAG_DATE:
                            date = marriage_data.get_value()
                        if marriage_data.get_tag() == tags.GEDCOM_TAG_PLACE:
                            place = marriage_data.get_value()
                    marriages.append((date, place))
        return marriages

    def get_marriage_years(self, individual: IndividualElement) -> List[int]:
        """Returns a list of marriage years for an individual.
        """
        dates = []

        if not isinstance(individual, IndividualElement):
            raise NotAnActualIndividualError(
                "Operation only valid for elements with %s tag" % tags.GEDCOM_TAG_INDIVIDUAL
            )

        # Get and analyze families where individual is spouse.
        families = self.get_families(individual, tags.GEDCOM_TAG_FAMILY_SPOUSE)
        for family in families:
            for child in family.get_child_elements():
                if child.get_tag() == tags.GEDCOM_TAG_MARRIAGE:
                    for gchild in child.get_child_elements():
                        if gchild.get_tag() == tags.GEDCOM_TAG_DATE:
                            date = gchild.get_value().split()[-1]
                            try:
                                dates.append(int(date))
                            except ValueError:
                                pass
        return dates

    def marriage_year_match(self, individual: IndividualElement, year: int) -> bool:
        """Checks if one of the marriage years of an individual matches the supplied year.
        Year is an integer.
        """
        if not isinstance(individual, IndividualElement):
            raise NotAnActualIndividualError(
                "Operation only valid for elements with %s tag" % tags.GEDCOM_TAG_INDIVIDUAL
            )

        years = self.get_marriage_years(individual)
        return year in years

    def marriage_range_match(self, individual: IndividualElement,
                             from_year: int, to_year: int) -> bool:
        """Check if one of the marriage years of an individual is in a given range.
        Years are integers.
        """
        if not isinstance(individual, IndividualElement):
            raise NotAnActualIndividualError(
                "Operation only valid for elements with %s tag" % tags.GEDCOM_TAG_INDIVIDUAL
            )

        years = self.get_marriage_years(individual)
        for year in years:
            if from_year <= year <= to_year:
                return True
        return False

    def get_families(self, individual: IndividualElement,
                     family_type: str = tags.GEDCOM_TAG_FAMILY_SPOUSE) -> List[FamilyElement]:
        """Return family elements listed for an individual.

        Optional argument `family_type` can be used to return specific subsets:

        `tags.GEDCOM_TAG_FAMILY_SPOUSE`: Default, families where the individual is a spouse.

        `tags.GEDCOM_TAG_FAMILY_CHILD`: Families where the individual is a child.
        """
        if not isinstance(individual, IndividualElement):
            raise NotAnActualIndividualError(
                "Operation only valid for elements with %s tag" % tags.GEDCOM_TAG_INDIVIDUAL
            )

        families = []
        element_dictionary = self.get_element_dictionary()

        for child_element in individual.get_child_elements():
            is_family = (child_element.get_tag() == family_type
                         and child_element.get_value() in element_dictionary
                         and element_dictionary[child_element.get_value()].is_family())
            if is_family:
                families.append(element_dictionary[child_element.get_value()])

        return families

    def get_ancestors(self, individual: IndividualElement,
                      ancestor_type: str = "ALL") -> List[Element]:
        """Return elements corresponding to ancestors of an individual.

        Optional argument `ancestor_type` can be used to return specific subsets:

        "ALL": Default, returns all ancestors.

        "NAT": Return only natural (genetic) ancestors.
        """
        if not isinstance(individual, IndividualElement):
            raise NotAnActualIndividualError(
                "Operation only valid for elements with %s tag" % tags.GEDCOM_TAG_INDIVIDUAL
            )

        parents = self.get_parents(individual, ancestor_type)
        ancestors = []
        ancestors.extend(parents)

        for parent in parents:
            ancestors.extend(self.get_ancestors(parent))

        return ancestors

    def get_parents(self, individual: IndividualElement,
                    parent_type: str = "ALL") -> List[IndividualElement]:
        """Return elements corresponding to parents of an individual.

        Optional argument `parent_type` can be used to return specific subsets:

        "ALL": Default, returns all parents.

        "NAT": Return only natural (genetic) parents.
        """
        if not isinstance(individual, IndividualElement):
            raise NotAnActualIndividualError(
                "Operation only valid for elements with %s tag" % tags.GEDCOM_TAG_INDIVIDUAL
            )

        parents = []
        families = self.get_families(individual, tags.GEDCOM_TAG_FAMILY_CHILD)

        for family in families:
            if parent_type == "NAT":
                for family_member in family.get_child_elements():

                    if family_member.get_tag() == tags.GEDCOM_TAG_CHILD \
                            and family_member.get_value() == individual.get_pointer():

                        for child in family_member.get_child_elements():
                            if child.get_value() == "Natural":
                                if child.get_tag() == tags.GEDCOM_PROGRAM_DEFINED_TAG_MREL:
                                    parents += self.get_family_members(family,
                                                                       tags.GEDCOM_TAG_WIFE)
                                elif child.get_tag() == tags.GEDCOM_PROGRAM_DEFINED_TAG_FREL:
                                    parents += self.get_family_members(family,
                                                                       tags.GEDCOM_TAG_HUSBAND)
            else:
                parents += self.get_family_members(family, "PARENTS")

        return parents

    def find_path_to_ancestor(self, descendant: IndividualElement,
                              ancestor: IndividualElement, path: str = None):
        """Return path from descendant to ancestor.
        :rtype: object
        """
        if not isinstance(descendant, IndividualElement) and isinstance(ancestor,
                                                                        IndividualElement):
            raise NotAnActualIndividualError(
                "Operation only valid for elements with %s tag." % tags.GEDCOM_TAG_INDIVIDUAL
            )

        if not path:
            path = [descendant]

        if path[-1].get_pointer() == ancestor.get_pointer():
            return path

        parents = self.get_parents(descendant, "NAT")
        for parent in parents:
            potential_path = self.find_path_to_ancestor(parent, ancestor, path + [parent])
            if potential_path is not None:
                return potential_path

        return None

    def get_family_members(self, family: FamilyElement,
                           members_type: str = FAMILY_MEMBERS_TYPE_ALL) -> List[IndividualElement]:
        """Return array of family members: individual, spouse, and children.

        Optional argument `members_type` can be used to return specific subsets:

        "FAMILY_MEMBERS_TYPE_ALL": Default, return all members of the family

        "FAMILY_MEMBERS_TYPE_PARENTS": Return individuals with "HUSB" and "WIFE" tags (parents)

        "FAMILY_MEMBERS_TYPE_HUSBAND": Return individuals with "HUSB" tags (father)

        "FAMILY_MEMBERS_TYPE_WIFE": Return individuals with "WIFE" tags (mother)

        "FAMILY_MEMBERS_TYPE_CHILDREN": Return individuals with "CHIL" tags (children)
        """
        if not isinstance(family, FamilyElement):
            raise NotAnActualFamilyError(
                "Operation only valid for element with %s tag." % tags.GEDCOM_TAG_FAMILY
            )

        family_members = []
        element_dictionary = self.get_element_dictionary()

        for child_element in family.get_child_elements():
            # Default is ALL
            is_family = (child_element.get_tag() == tags.GEDCOM_TAG_HUSBAND
                         or child_element.get_tag() == tags.GEDCOM_TAG_WIFE
                         or child_element.get_tag() == tags.GEDCOM_TAG_CHILD)

            if members_type == FAMILY_MEMBERS_TYPE_PARENTS:
                is_family = (child_element.get_tag() == tags.GEDCOM_TAG_HUSBAND
                             or child_element.get_tag() == tags.GEDCOM_TAG_WIFE)
            elif members_type == FAMILY_MEMBERS_TYPE_HUSBAND:
                is_family = child_element.get_tag() == tags.GEDCOM_TAG_HUSBAND
            elif members_type == FAMILY_MEMBERS_TYPE_WIFE:
                is_family = child_element.get_tag() == tags.GEDCOM_TAG_WIFE
            elif members_type == FAMILY_MEMBERS_TYPE_CHILDREN:
                is_family = child_element.get_tag() == tags.GEDCOM_TAG_CHILD

            if is_family and child_element.get_value() in element_dictionary:
                family_members.append(element_dictionary[child_element.get_value()])

        return family_members

    # Other methods

    def to_gedcom_string(self, recursive: bool = False) -> str:
        """Formats all elements and optionally all of the sub-elements into a
        GEDCOM string.
        """
        is_gte_python_3 = version_info[0] >= 3
        output = '' if is_gte_python_3 else b''

        for element in self.get_root_child_elements():
            if is_gte_python_3:
                output += element.to_gedcom_string(recursive)
            else:
                output += element.to_gedcom_string(recursive).encode('utf-8-sig')

        return output

    def print_gedcom(self):
        """Write GEDCOM data to stdout."""
        self.save_gedcom(stdout)

    def save_gedcom(self, open_file: IO, recursive: bool = True):
        """Save GEDCOM data to a file.
        """
        open_file.write(self.to_gedcom_string(recursive))
