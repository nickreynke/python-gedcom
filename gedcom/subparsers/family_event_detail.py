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
Substructure parser for the FAMILY_EVENT_DETAIL emdedded record. As this is
referenced in place as part of another structure there is no identifier tag.
"""

import gedcom.tags as tags
from gedcom.subparsers.event_detail import event_detail


def family_event_detail(element):
    """Parses and extracts the FAMILY_EVENT_DETAIL
    :rtype: dict
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
