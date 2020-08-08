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
Substructure parser for the `ASSOCIATION_STRUCTURE` record.

This is anchored by the `gedcom.tags.GEDCOM_TAG_ASSOCIATES` tag.
"""

import gedcom.tags as tags
from gedcom.elements.element import Element
from gedcom.subparsers.note_structure import note_structure
from gedcom.subparsers.source_citation import source_citation


def association_structure(element: Element) -> dict:
    """Parses and extracts the `ASSOCIATION_STRUCTURE` structure.

    The `element` should contain the `gedcom.tags.GEDCOM_TAG_ASSOCIATES` tag.
    """
    record = {
        'key_to_individual': element.get_value(),
        'relationship': '',
        'citations': [],
        'notes': []
    }
    for child in element.get_child_elements():
        if child.get_tag() == tags.GEDCOM_TAG_RELATIONSHIP:
            record['relationship'] = child.get_value()
            continue

        if child.get_tag() == tags.GEDCOM_TAG_NOTE:
            record['notes'].append(note_structure(child))
            continue

        if child.get_tag() == tags.GEDCOM_TAG_SOURCE:
            record['citations'].append(source_citation(child))

    return record
