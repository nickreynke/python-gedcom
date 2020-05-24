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
Substructure parser for the NOTE_STRUCTURE record identified by the
`gedcom.tags.GEDCOM_TAG_NOTE` tag.
"""

def note_structure(element):
    """Parse and extract a NOTE_STRUCTURE
    :rtype: dict
    """
    record = {
        'key_to_note': element.get_value(),
        'note': ''
    }
    if record['key_to_note'] not in [None, '']:
        if '@' in record['key_to_note']:
            return record
    record['key_to_note'] = ''
    record['note'] = element.get_multi_line_value()

    return record
