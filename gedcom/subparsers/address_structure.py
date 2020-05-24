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
Substructure parser for the ADDRESS_STRUCTURE embedded record.

Note this is usually referenced as part of a larger structure and the
`gedcom.tags.GEDCOM_TAG_ADDRESS` tag is at the same level as some of
the other parts of this structure.
"""

import gedcom.tags as tags

ADDRESS_TAGS = {
    tags.GEDCOM_PROGRAM_DEFINED_TAG_ADDRESSE: 'addresse',
    tags.GEDCOM_TAG_ADDRESS1: 'address1',
    tags.GEDCOM_TAG_ADDRESS2: 'address2',
    tags.GEDCOM_TAG_ADDRESS3: 'address3',
    tags.GEDCOM_TAG_CITY: 'city',
    tags.GEDCOM_TAG_STATE: 'state',
    tags.GEDCOM_TAG_POSTAL_CODE: 'postal_code',
    tags.GEDCOM_TAG_COUNTRY: 'country'
}

CONTACT_TAGS = {
    tags.GEDCOM_TAG_PHONE: 'phone',
    tags.GEDCOM_TAG_EMAIL: 'email',
    tags.GEDCOM_TAG_FAX: 'fax',
    tags.GEDCOM_TAG_WWW: 'www'
}

def address_structure(element):
    """Parses and extracts the ADDRESS_STRUCTURE
    :rtype: dict
    """
    record = {
        'address': '',
        'addresse': '',
        'address1': '',
        'address2': '',
        'address3': '',
        'city': '',
        'state': '',
        'postal_code': '',
        'country': '',
        'phone': [],
        'email': [],
        'fax': [],
        'www': []
    }
    for child in element.get_child_elements():
        if child.get_tag() == tags.GEDCOM_TAG_ADDRESS:
            record['address'] = child.get_multi_line_value()
            for gchild in child.get_child_elements():
                if gchild.get_tag() in ADDRESS_TAGS:
                    record[ADDRESS_TAGS[gchild.get_tag()]] = gchild.get_value()
            continue

        if child.get_tag() in CONTACT_TAGS:
            record[CONTACT_TAGS[child.get_tag()]].append(child.get_value())

    return record
