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
Substructure parser for a `NOTE_STRUCTURE` record.

This is anchored by the `gedcom.tags.GEDCOM_TAG_NOTE` tag.
"""

from gedcom.elements.element import Element


def parse_note_structure(element: Element) -> dict:
    """Parse and extract a `NOTE_STRUCTURE` structure.

    The `element` should contain the `gedcom.tags.GEDCOM_TAG_NOTE` tag.
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
