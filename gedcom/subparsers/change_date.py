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
Substructure parser for a `CHANGE_DATE` record.

This is anchored by the `gedcom.tags.GEDCOM_TAG_CHANGE` tag.
"""

import gedcom.tags as tags
from gedcom.element.element import Element
from gedcom.subparsers.note_structure import note_structure


def change_date(element: Element) -> dict:
    """Parses and extracts a `CHANGE_DATE` structure.

    The `element` should contain the `gedcom.tags.GEDCOM_TAG_CHANGE` tag.
    """
    record = {
        'date': '',
        'time': '',
        'notes': []
    }
    for child in element.get_child_elements():
        if child.get_tag() == tags.GEDCOM_TAG_DATE:
            record['date'] = child.get_value()
            for gchild in child.get_child_elements():
                if gchild.get_tag() == tags.GEDCOM_TAG_TIME:
                    record['time'] = gchild.get_value()
                    continue
            continue

        if child.get_tag() == tags.GEDCOM_TAG_NOTE:
            record['notes'].append(note_structure(child))

    return record
