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
Substructure parser for a `FAMILY_EVENT_DETAIL` emdedded record.

This is referenced as part of a larger structure so there is no anchor tag.
"""

import gedcom.tags as tags
from gedcom.elements.element import Element
from gedcom.subparsers.event_detail import event_detail


def family_event_detail(element: Element) -> dict:
    """Parses and extracts a `FAMILY_EVENT_DETAIL` structure.

    The `element` shouldbe the parent that contains it.
    """
    record = event_detail(element)
    record['husband_age'] = ''
    record['wife_age'] = ''
    for child in element.get_child_elements():
        if child.get_tag() == tags.GEDCOM_TAG_HUSBAND:
            for gchild in child.get_child_elements():
                if gchild.get_tag() == tags.GEDCOM_TAG_AGE:
                    record['husband_age'] = gchild.get_value()
            continue

        if child.get_tag() == tags.GEDCOM_TAG_WIFE:
            for gchild in child.get_child_elements():
                if gchild.get_tag() == tags.GEDCOM_TAG_AGE:
                    record['wife_age'] = gchild.get_value()

    return record
