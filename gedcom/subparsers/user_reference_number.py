# -*- coding: utf-8 -*-

# Python GEDCOM Parser
#
# Copyright (C) 2020 Christopher Horn (cdhorn at embarqmail dot com)
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
Parser for a `USER_REFERENCE_NUMBER` structure.

This is anchored by the `gedcom.tags.GEDCOM_TAG_REFERENCE` tag.

This is not a formally documented structure in the standard but it is
a substructure that repeats itself in a number of record types.
"""

import gedcom.tags as tags
from gedcom.element.element import Element


def user_reference_number(element: Element) -> dict:
    """Parse and extract a `USER_REFERENCE_NUMBER` structure.

    The `element` should contain the `gedcom.tags.GEDCOM_TAG_REFERENCE` tag.
    """
    record = {
        'reference': element.get_value(),
        'type': ''
    }
    for child in element.get_child_elements():
        if child.get_tag() == tags.GEDCOM_TAG_TYPE:
            record['type'] = child.get_value()

    return record
