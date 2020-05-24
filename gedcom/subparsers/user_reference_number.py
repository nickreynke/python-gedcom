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
Parser for a USER_REFERENCE_NUMBER structure identified by the top level
`gedcom.tags.GEDCOM_TAG_REFERENCE` tag.
"""

import gedcom.tags as tags

def user_reference_number(element):
    """Parse and extract USER_REFERENCE_NUMBER
    :rtype: dict
    """
    record = {
        'reference': element.get_value(),
        'type': ''
    }
    for child in element.get_child_elements():
        if child.get_tag() == tags.GEDCOM_TAG_TYPE:
            record['type'] = child.get_value()

    return record
