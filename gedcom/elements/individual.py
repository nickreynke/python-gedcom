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
GEDCOM element for a `INDIVIDUAL_RECORD` individual record identified by the
`gedcom.tags.GEDCOM_TAG_INDIVIDUAL` tag.
"""

from typing import Tuple, List
import re as regex

import gedcom.tags as tags
from gedcom.elements.element import Element
from gedcom.subparsers.personal_name_structure import parse_personal_name_structure
from gedcom.subparsers.individual_event_structure import parse_individual_event_structure
from gedcom.subparsers.individual_attribute_structure import parse_individual_attribute_structure
from gedcom.subparsers.lds_individual_ordinance import parse_lds_individual_ordinance
from gedcom.subparsers.child_to_family_link import parse_child_to_family_link
from gedcom.subparsers.spouse_to_family_link import parse_spouse_to_family_link
from gedcom.subparsers.association_structure import parse_association_structure
from gedcom.subparsers.user_reference_number import parse_user_reference_number
from gedcom.subparsers.change_date import parse_change_date
from gedcom.subparsers.note_structure import parse_note_structure
from gedcom.subparsers.source_citation import parse_source_citation
from gedcom.subparsers.multimedia_link import parse_multimedia_link
from gedcom.helpers import deprecated

INDIVIDUAL_SINGLE_TAGS = {
    tags.GEDCOM_TAG_RESTRICTION: 'restriction',
    tags.GEDCOM_TAG_SEX: 'sex',
    tags.GEDCOM_TAG_REC_ID_NUMBER: 'record_id',
    tags.GEDCOM_TAG_REC_FILE_NUMBER: 'permanent_file_number',
    tags.GEDCOM_TAG_AFN: 'ancestral_file_number'
}


class IndividualElement(Element):
    """Element associated with an `INDIVIDUAL_RECORD`"""

    def get_tag(self) -> str:
        return tags.GEDCOM_TAG_INDIVIDUAL

    def get_record(self) -> dict:
        """Parse and return the full record in dictionary format.
        """
        record = {
            'key_to_individual': self.get_pointer(),
            'restriction': '',
            'names': [],
            'sex': 'U',
            'events': parse_individual_event_structure(self),
            'attributes': parse_individual_attribute_structure(self),
            'child_to_family': [],
            'spouse_to_family': [],
            'submitters': [],
            'associates': [],
            'aliases': [],
            'ancestors_interest': [],
            'descendants_interest': [],
            'permanent_file_number': '',
            'ancestral_file_number': '',
            'references': [],
            'record_id': '',
            'change_date': {},
            'notes': [],
            'citations': [],
            'media': []
        }
        lds_events = parse_lds_individual_ordinance(self)
        if len(lds_events) > 0:
            for event in lds_events:
                record['events'].append(event)

        for child in self.get_child_elements():
            if child.get_tag() in INDIVIDUAL_SINGLE_TAGS:
                record[INDIVIDUAL_SINGLE_TAGS[child.get_tag()]] = child.get_value()
                continue

            if child.get_tag() == tags.GEDCOM_TAG_NAME:
                record['names'].append(parse_personal_name_structure(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_FAMILY_CHILD:
                record['child_to_family'].append(parse_child_to_family_link(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_FAMILY_SPOUSE:
                record['spouse_to_family'].append(parse_spouse_to_family_link(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_NOTE:
                record['notes'].append(parse_note_structure(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_SOURCE:
                record['citations'].append(parse_source_citation(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_MEDIA:
                record['media'].append(parse_multimedia_link(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_SUBMITTER:
                record['submitters'].append(child.get_value())
                continue

            if child.get_tag() == tags.GEDCOM_TAG_ASSOCIATES:
                record['associates'].append(parse_association_structure(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_ALIAS:
                record['aliases'].append(child.get_value())
                continue

            if child.get_tag() == tags.GEDCOM_TAG_ANCES_INTEREST:
                record['ancestors_interest'].append(child.get_value())
                continue

            if child.get_tag() == tags.GEDCOM_TAG_DESCENDANTS_INT:
                record['descendants_interest'].append(child.get_value())
                continue

            if child.get_tag() == tags.GEDCOM_TAG_REFERENCE:
                record['references'].append(parse_user_reference_number(child))
                continue

            if child.get_tag() == tags.GEDCOM_TAG_CHANGE:
                record['changed'] = parse_change_date(child)

        return record

    def is_deceased(self) -> bool:
        """Checks if this individual is deceased.
        """
        for child in self.get_child_elements():
            if child.get_tag() == tags.GEDCOM_TAG_DEATH:
                return True

        return False

    def is_child(self) -> bool:
        """Checks if this element is a child of a family.
        """
        found_child = False

        for child in self.get_child_elements():
            if child.get_tag() == tags.GEDCOM_TAG_FAMILY_CHILD:
                found_child = True

        return found_child

    def is_private(self) -> bool:
        """Checks if this individual is marked private.
        """
        for child in self.get_child_elements():
            if child.get_tag() == tags.GEDCOM_TAG_PRIVATE:
                private = child.get_value()
                if private == 'Y':
                    return True

        return False

    def get_name(self) -> Tuple[str, str]:
        """Returns an individual's names as a tuple: (`str` given_name, `str` surname)
        """
        given_name = ""
        surname = ""

        # Return the first tags.GEDCOM_TAG_NAME that is found.
        # Alternatively as soon as we have both the tags.GEDCOM_TAG_GIVEN_NAME
        # and _SURNAME return those.
        found_given_name = False
        found_surname_name = False

        for child in self.get_child_elements():
            if child.get_tag() == tags.GEDCOM_TAG_NAME:
                # Some GEDCOM files don't use child tags but instead
                # place the name in the value of the NAME tag.
                if child.get_value() != "":
                    name = child.get_value().split('/')

                    if len(name) > 0:
                        given_name = name[0].strip()
                        if len(name) > 1:
                            surname = name[1].strip()

                    return given_name, surname

                for gchild in child.get_child_elements():

                    if gchild.get_tag() == tags.GEDCOM_TAG_GIVEN_NAME:
                        given_name = gchild.get_value()
                        found_given_name = True

                    if gchild.get_tag() == tags.GEDCOM_TAG_SURNAME:
                        surname = gchild.get_value()
                        found_surname_name = True

                if found_given_name and found_surname_name:
                    return given_name, surname

        # If we reach here we are probably returning empty strings
        return given_name, surname

    def get_all_names(self) -> List[str]:
        """Return all names."""
        return [a.get_value() for a in self.get_child_elements()
                if a.get_tag() == tags.GEDCOM_TAG_NAME]

    def surname_match(self, surname_to_match: str) -> bool:
        """Matches a string with the surname of an individual.
        """
        (given_name, surname) = self.get_name()
        return regex.search(surname_to_match, surname, regex.IGNORECASE)

    @deprecated
    def given_match(self, name: str) -> bool:
        """Matches a string with the given name of an individual.
        ::deprecated:: As of version 1.0.0 use `given_name_match()` method instead
        """
        return self.given_name_match(name)

    def given_name_match(self, given_name_to_match: str) -> bool:
        """Matches a string with the given name of an individual.
        """
        (given_name, surname) = self.get_name()
        return regex.search(given_name_to_match, given_name, regex.IGNORECASE)

    def get_gender(self) -> str:
        """Returns the gender of a person in string format.
        """
        gender = ""

        for child in self.get_child_elements():
            if child.get_tag() == tags.GEDCOM_TAG_SEX:
                gender = child.get_value()

        return gender

    def get_birth_data(self) -> Tuple[str, str, List[str]]:
        """Returns the birth data of a person formatted as a tuple:
        (`str` date, `str` place, `list` sources)
        """
        date = ""
        place = ""
        sources = []

        for child in self.get_child_elements():
            if child.get_tag() == tags.GEDCOM_TAG_BIRTH:
                for gchild in child.get_child_elements():

                    if gchild.get_tag() == tags.GEDCOM_TAG_DATE:
                        date = gchild.get_value()

                    if gchild.get_tag() == tags.GEDCOM_TAG_PLACE:
                        place = gchild.get_value()

                    if gchild.get_tag() == tags.GEDCOM_TAG_SOURCE:
                        sources.append(gchild.get_value())

        return date, place, sources

    def get_birth_year(self) -> int:
        """Returns the birth year of a person in integer format.
        """
        date = ""

        for child in self.get_child_elements():
            if child.get_tag() == tags.GEDCOM_TAG_BIRTH:
                for gchild in child.get_child_elements():
                    if gchild.get_tag() == tags.GEDCOM_TAG_DATE:
                        date_split = gchild.get_value().split()
                        date = date_split[len(date_split) - 1]

        if date == "":
            return -1
        try:
            return int(date)
        except ValueError:
            return -1

    def get_death_data(self) -> Tuple[str, str, List[str]]:
        """Returns the death data of a person formatted as a tuple:
        (`str` date, `str` place, `list` sources)
        """
        date = ""
        place = ""
        sources = []

        for child in self.get_child_elements():
            if child.get_tag() == tags.GEDCOM_TAG_DEATH:
                for gchild in child.get_child_elements():
                    if gchild.get_tag() == tags.GEDCOM_TAG_DATE:
                        date = gchild.get_value()
                    if gchild.get_tag() == tags.GEDCOM_TAG_PLACE:
                        place = gchild.get_value()
                    if gchild.get_tag() == tags.GEDCOM_TAG_SOURCE:
                        sources.append(gchild.get_value())

        return date, place, sources

    def get_death_year(self) -> int:
        """Returns the death year of a person in integer format.
        """
        date = ""

        for child in self.get_child_elements():
            if child.get_tag() == tags.GEDCOM_TAG_DEATH:
                for gchild in child.get_child_elements():
                    if gchild.get_tag() == tags.GEDCOM_TAG_DATE:
                        date_split = gchild.get_value().split()
                        date = date_split[len(date_split) - 1]

        if date == "":
            return -1
        try:
            return int(date)
        except ValueError:
            return -1

    @deprecated
    def get_burial(self) -> Tuple[str, str, List[str]]:
        """Returns the burial data of a person formatted as a tuple:
        (`str` date, `str´ place, `list` sources)
        ::deprecated:: As of version 1.0.0 use `get_burial_data()` method instead
        """
        self.get_burial_data()

    def get_burial_data(self) -> Tuple[str, str, List[str]]:
        """Returns the burial data of a person formatted as a tuple:
        (`str` date, `str´ place, `list` sources)
        """
        date = ""
        place = ""
        sources = []

        for child in self.get_child_elements():
            if child.get_tag() == tags.GEDCOM_TAG_BURIAL:
                for gchild in child.get_child_elements():

                    if gchild.get_tag() == tags.GEDCOM_TAG_DATE:
                        date = gchild.get_value()

                    if gchild.get_tag() == tags.GEDCOM_TAG_PLACE:
                        place = gchild.get_value()

                    if gchild.get_tag() == tags.GEDCOM_TAG_SOURCE:
                        sources.append(gchild.get_value())

        return date, place, sources

    @deprecated
    def get_census(self) -> List[Tuple[str, str, List[str]]]:
        """Returns a list of censuses of an individual formatted as tuples:
        (`str` date, `str´ place, `list` sources)
        ::deprecated:: As of version 1.0.0 use `get_census_data()` method instead
        """
        self.get_census_data()

    def get_census_data(self) -> List[Tuple[str, str, List[str]]]:
        """Returns a list of censuses of an individual formatted as tuples:
        (`str` date, `str´ place, `list` sources)
        """
        census = []

        for child in self.get_child_elements():
            if child.get_tag() == tags.GEDCOM_TAG_CENSUS:

                date = ''
                place = ''
                sources = []

                for gchild in child.get_child_elements():

                    if gchild.get_tag() == tags.GEDCOM_TAG_DATE:
                        date = gchild.get_value()

                    if gchild.get_tag() == tags.GEDCOM_TAG_PLACE:
                        place = gchild.get_value()

                    if gchild.get_tag() == tags.GEDCOM_TAG_SOURCE:
                        sources.append(gchild.get_value())

                census.append((date, place, sources))

        return census

    def get_last_change_date(self) -> str:
        """Returns the date of when the person data was last changed formatted as a string.
        """
        date = ""

        for child in self.get_child_elements():
            if child.get_tag() == tags.GEDCOM_TAG_CHANGE:
                for gchild in child.get_child_elements():
                    if gchild.get_tag() == tags.GEDCOM_TAG_DATE:
                        date = gchild.get_value()

        return date

    def get_occupation(self) -> str:
        """Returns the occupation of a person.
        """
        occupation = ""

        for child in self.get_child_elements():
            if child.get_tag() == tags.GEDCOM_TAG_OCCUPATION:
                occupation = child.get_value()

        return occupation

    def birth_year_match(self, year: int) -> bool:
        """Returns `True` if the given year matches the birth year of this person.
        """
        return self.get_birth_year() == year

    def birth_range_match(self, from_year: int, to_year: int) -> bool:
        """Checks if the birth year of a person lies within the given range.
        """
        birth_year = self.get_birth_year()

        if from_year <= birth_year <= to_year:
            return True

        return False

    def death_year_match(self, year: int) -> bool:
        """Returns `True` if the given year matches the death year of this person.
        """
        return self.get_death_year() == year

    def death_range_match(self, from_year: int, to_year: int) -> bool:
        """Checks if the death year of a person lies within the given range.
        """
        death_year = self.get_death_year()

        if from_year <= death_year <= to_year:
            return True

        return False

    def criteria_match(self, criteria: str) -> bool:
        """Checks if this individual matches all of the given criteria.

        `criteria` is a colon-separated list, where each item in the
        list has the form [name]=[value]. The following criteria are supported:

        surname=[name]
             Match a person with [name] in any part of the `surname`.
        given_name=[given_name]
             Match a person with [given_name] in any part of the given `given_name`.
        birth=[year]
             Match a person whose birth year is a four-digit [year].
        birth_range=[from_year-to_year]
             Match a person whose birth year is in the range of years from
             [from_year] to [to_year], including both [from_year] and [to_year].
        """

        # Check if criteria is a valid criteria and can be split by `:` and `=` characters
        try:
            for criterion in criteria.split(':'):
                criterion.split('=')
        except ValueError:
            return False

        match = True

        for criterion in criteria.split(':'):
            key, value = criterion.split('=')

            if key == "surname" and not self.surname_match(value):
                match = False
            elif key == "name" and not self.given_name_match(value):
                match = False
            elif key == "birth":

                try:
                    year = int(value)
                    if not self.birth_year_match(year):
                        match = False
                except ValueError:
                    match = False

            elif key == "birth_range":

                try:
                    from_year, to_year = value.split('-')
                    from_year = int(from_year)
                    to_year = int(to_year)
                    if not self.birth_range_match(from_year, to_year):
                        match = False
                except ValueError:
                    match = False

            elif key == "death":

                try:
                    year = int(value)
                    if not self.death_year_match(year):
                        match = False
                except ValueError:
                    match = False

            elif key == "death_range":

                try:
                    from_year, to_year = value.split('-')
                    from_year = int(from_year)
                    to_year = int(to_year)
                    if not self.death_range_match(from_year, to_year):
                        match = False
                except ValueError:
                    match = False

        return match
