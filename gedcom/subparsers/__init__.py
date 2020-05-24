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

"""Module containing parsers for extracting various substructures from the
different record types as defined in the GEDCOM standard."""

__all__ = [
    "address_structure",
    "association_structure",
    "change_date",
    "child_to_family_link",
    "event_detail",
    "family_event_detail",
    "family_event_structure",
    "individual_attribute_structure",
    "individual_event_detail",
    "individual_event_structure",
    "lds_individual_ordinance",
    "lds_spouse_sealing",
    "multimedia_link",
    "note_structure",
    "personal_name_pieces",
    "personal_name_structure",
    "place_structure",
    "source_citation",
    "source_repository_citation",
    "spouse_to_family_link",
    "user_reference_number"
]
