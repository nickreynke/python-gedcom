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
Substructure parser for a `PERSONAL_NAME_PIECES` embedded record.

This is referenced as part of a larger structure so there is no anchor tag.
"""

import gedcom.tags as tags
from gedcom.elements.element import Element
from gedcom.subparsers.note_structure import note_structure
from gedcom.subparsers.source_citation import source_citation

NAME_TAGS = {
    tags.GEDCOM_TAG_NAME_PREFIX: 'prefix',
    tags.GEDCOM_TAG_GIVEN_NAME: 'given',
    tags.GEDCOM_TAG_NICKNAME: 'nick',
    tags.GEDCOM_TAG_SURN_PREFIX: 'surname_prefix',
    tags.GEDCOM_TAG_SURNAME: 'surname',
    tags.GEDCOM_TAG_NAME_SUFFIX: 'suffix',
    tags.GEDCOM_PROGRAM_DEFINED_TAG_RUFNAME: 'rufname'
}


def personal_name_pieces(element: Element) -> dict:
    """Parse and extract a `PERSONAL_NAME_PIECES` structure.

    The `element` should be the parent that contains it.
    """
    record = {
        'prefix': '',
        'given': '',
        'nick': '',
        'surname_prefix': '',
        'surname': '',
        'suffix': '',
        'rufname': '',
        'notes': [],
        'citations': []
    }
    for child in element.get_child_elements():
        if child.get_tag() in NAME_TAGS:
            record[NAME_TAGS[child.get_tag()]] = child.get_value()
            continue

        if child.get_tag() == tags.GEDCOM_TAG_NOTE:
            record['notes'].append(note_structure(child))
            continue

        if child.get_tag() == tags.GEDCOM_TAG_SOURCE:
            record['citations'].append(source_citation(child))
            continue

    return record
