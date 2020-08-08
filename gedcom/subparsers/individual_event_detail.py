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
Substructure parser for a `INDIVIDUAL_EVENT_DETAIL` emdedded record.

This is referenced as part of a larger structure so there is no anchor tag.
"""

import gedcom.tags as tags
from gedcom.element.element import Element
from gedcom.subparsers.event_detail import event_detail


def individual_event_detail(element: Element) -> dict:
    """Parses and extracts a `INDIVIDUAL_EVENT_DETAIL` structure.

    The `element` should be the parent that contains it.
    """
    record = event_detail(element)
    record['age'] = ''
    for child in element.get_child_elements():
        if child.get_tag() == tags.GEDCOM_TAG_AGE:
            record['age'] = child.get_value()

    return record
