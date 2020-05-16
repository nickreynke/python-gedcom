# -*- coding: utf-8 -*-

# Python GEDCOM Parser
#
# Copyright (C) 2020 Christopher Horn
# Copyright (C) 2018 Damon Brodie (damon.brodie at gmail.com)
# Copyright (C) 2018-2019 Nicklas Reincke (contact at reynke.com)
# Copyright (C) 2016 Andreas Oberritter
# Copyright (C) 2012 Madeleine Price Ball
# Copyright (C) 2005 Daniel Zappala (zappala at cs.byu.edu)
# Copyright (C) 2005 Brigham Young University
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
GEDCOM tags.
"""

GEDCOM_PROGRAM_DEFINED_TAG_APID = "_APID"
"""Value: `_APID`

Ancestry page id for a citation, points to page in database of record."""

GEDCOM_PROGRAM_DEFINED_TAG_DCAUSE = "_DCAUSE"
"""Value: `_DCAUSE`

Cause of death."""

GEDCOM_PROGRAM_DEFINED_TAG_DEGREE = "_DEG"
"""Value: `_DEG`

Degree or recognition of accomplishment received by an individual."""

GEDCOM_PROGRAM_DEFINED_TAG_FREL = "_FREL"
"""Value: `_FREL`

Relationship to a father."""

GEDCOM_PROGRAM_DEFINED_TAG_FUNERAL = "_FUN"
"""Value: `_FUN`

Funeral for an individual."""

GEDCOM_PROGRAM_DEFINED_TAG_MEDICAL = "_MDCL"
"""Value: `_MDCL`

Medical information about an individual."""

GEDCOM_PROGRAM_DEFINED_TAG_MILITARY = "_MILT"
"""Value: `_MILT`

A military related event in the individuals life."""

GEDCOM_PROGRAM_DEFINED_TAG_MREL = "_MREL"
"""Value: `_MREL`

Relationship to a mother."""

GEDCOM_PROGRAM_DEFINED_TAG_PHOTO = "_PHOTO"
"""Value: `_PHOTO`

Used by some programs to identify the primary multimedia object for an 
individual, the same as `gedcom.tags.GEDCOM_PROGRAM_DEFINED_TAG_PRIMARY`."""

GEDCOM_PROGRAM_DEFINED_TAG_PREFERRED = "_PREF"
"""Value: `_PREF`

Indicates a preferred spouse, child or parents."""

GEDCOM_PROGRAM_DEFINED_TAG_PRIMARY = "_PRIM"
"""Value: `_PRIM`

Primary multimedia object for an individual."""

GEDCOM_TAG_ABBREVIATION = "ABBR"
"""Value: `ABBR`

A short name of a title, description, or name."""

GEDCOM_TAG_ADDRESS = "ADDR"
"""Value: `ADDR`

The contemporary place, usually required for postal purposes, of an individual,
a submitter of information, a repository, a business, a school, or a company."""

GEDCOM_TAG_ADDRESS1 = "ADR1"
"""Value: `ADR1`

The first line of an address."""

GEDCOM_TAG_ADDRESS2 = "ADR2"
"""Value: `ADR2`

The second line of an address."""

GEDCOM_TAG_ADOPTION = "ADOP"
"""Value: `ADOP`

Pertaining to creation of a child-parent relationship that does not exist
biologically."""

GEDCOM_TAG_AGE = "AFN"
"""Value: `AFN`

Ancestral File Number, a unique permanent record file number of an individual
record stored in Ancestral File."""

GEDCOM_TAG_AGE = "AGE"
"""Value: `AGE`

The age of the individual at the time an event occurred, or the age listed in
the document."""

GEDCOM_TAG_AGENCY = "AGNC"
"""Value: `AGNC`

The institution or individual having authority and/or responsibility to manage
or govern."""

GEDCOM_TAG_ALIAS = "ALIA"
"""Value: `ALIA`

An indicator to link different record descriptions of a person who may be the
same person."""

GEDCOM_TAG_ANCESTORS = "ANCE"
"""Value: `ANCE`

Pertaining to forbearers of an individual."""

GEDCOM_TAG_ANCES_INTEREST = "ANCI"
"""Value: `ANCI`

Indicates an interest in additional research for ancestors of this individual.
(See also `gedcom.tags.GEDCOM_TAG_DESCENDANTS_INT`)"""

GEDCOM_TAG_ANNULMENT = "ANUL"
"""Value: `ANUL`

Declaring a marriage void from the beginning (never existed)."""

GEDCOM_TAG_ASSOCIATES = "ASSO"
"""Value: `ASSO`

An indicator to link friends, neighbors, relatives, or associates of an
individual."""

GEDCOM_TAG_AUTHOR = "AUTH"
"""Value: `AUTH`

The name of the individual who created or compiled information."""

GEDCOM_TAG_BAPTISM_LDS = "BAPL"
"""Value: `BAPL`

The event of baptism performed at age eight or later by priesthood authority
of the LDS Church. (See also `gedcom.tags.GEDCOM_TAG_BAPTISM`)"""

GEDCOM_TAG_BAPTISM = "BAPM"
"""Value: `BAPM`

The event of baptism (not LDS), performed in infancy or later."""

GEDCOM_TAG_BAR_MITZVAH = "BARM"
"""Value: `BARM`

The ceremonial event held when a Jewish boy reaches age 13."""

GEDCOM_TAG_BAS_MITZVAH = "BASM"
"""Value: `BASM`

The ceremonial event held when a Jewish girl reaches age 13, also known as
Bat Mitzvah."""

GEDCOM_TAG_BIRTH = "BIRT"
"""Value: `BIRT`

The event of entering into life."""

GEDCOM_TAG_BLESSING = "BLES"
"""Value: `BLES`

A religious event of bestowing divine care or intercession. Sometimes given
in connection with a naming ceremony."""

GEDCOM_TAG_BURIAL = "BURI"
"""Value: `BURI`

The event of the proper disposing of the mortal remains of a deceased person."""

GEDCOM_TAG_CALL_NUMBER = "CALN"
"""Value: `CALN`

The number used by a repository to identify the specific items in its
collections."""

GEDCOM_TAG_CASTE = "CAST"
"""Value: `CAST`

The name of an individual's rank or status in society, based on racial or
religious differences, or differences in wealth, inherited rank, profession,
occupation, etc."""

GEDCOM_TAG_CAUSE = "CAUSE"
"""Value: `CAUS`

A description of the cause of the associated event or fact, such as the cause
of death."""

GEDCOM_TAG_CENSUS = "CENS"
"""Value: `CENS`.

The event of the periodic count of the population for a designated locality,
such as a national or state Census."""

GEDCOM_TAG_CHANGE = "CHAN"
"""Value: `CHAN`

Indicates a change, correction, or modification. Typically used in connection
with a `gedcom.tags.GEDCOM_TAG_DATE` to specify when a change in information
occurred."""

GEDCOM_TAG_CHARACTER = "CHAR"
"""Value: `CHAR`

An indicator of the character set used in writing this automated information."""

GEDCOM_TAG_CHILD = "CHIL"
"""Value: `CHIL`

The natural, adopted, or sealed (LDS) child of a father and a mother."""

GEDCOM_TAG_CHRISTENING = "CHR"
"""Value: `CHR`

The religious event (not LDS) of baptizing and/or naming a child."""

GEDCOM_TAG_ADULT_CHRISTENING = "CHRA"
"""Value: `CHRA`

The religious event (not LDS) of baptizing and/or naming an adult person."""

GEDCOM_TAG_CITY = "CITY"
"""Value: `CITY`

A lower level jurisdictional unit. Normally an incorporated municipal unit."""

GEDCOM_TAG_CONCATENATION = "CONC"
"""Value: `CONC`

An indicator that additional data belongs to the superior value. The information
from the `CONC` value is to be connected to the value of the superior preceding
line without a space and without a carriage return and/or new line character.
Values that are split for a `CONC` tag must always be split at a non-space. If
the value is split on a space the space will be lost when concatenation takes
place. This is because of the treatment that spaces get as a GEDCOM delimiter,
many GEDCOM values are trimmed of trailing spaces and some systems look for
the first non-space starting after the tag to determine the beginning of the
value."""

GEDCOM_TAG_CONFIRMATION = "CONF"
"""Value: `CONF`

The religious event (not LDS) of conferring the gift of the Holy Ghost and,
among protestants, full church membership."""

GEDCOM_TAG_CONFIRMATION_L = "CONL"
"""Value: `CONL`

The religious event by which a person receives membership in the LDS Church."""

GEDCOM_TAG_CONTINUED = "CONT"
"""Value: `CONT`

An indicator that additional data belongs to the superior value. The information
from the `CONT` value is to be connected to the value of the superior preceding
line with a carriage return and/or new line character. Leading spaces could be
important to the formatting of the resultant text. When importing values from
`CONT` lines the reader should assume only one delimiter character following
the `CONT` tag. Assume that the rest of the leading spaces are to be a part
of the value."""

GEDCOM_TAG_COPYRIGHT = "COPR"
"""Value: `COPR`

A statement that accompanies data to protect it from unlawful duplication
and distribution."""

GEDCOM_TAG_COPPORATE = "CORP"
"""Value: `CORP`

A name of an institution, agency, corporation, or company."""

GEDCOM_TAG_CREMATION = "CREM"
"""Value: `CREM`

Disposal of the remains of a person's body by fire."""

GEDCOM_TAG_COUNTRY = "CTRY"
"""Value: `CTRY`

The name or code of a country."""

GEDCOM_TAG_DATA = "DATA"
"""Value: `DATA`

Pertaining to stored automation information."""

GEDCOM_TAG_DATE = "DATE"
"""Value: `DATE`

The time of an event in a calendar format."""

GEDCOM_TAG_DEATH = "DEAT"
"""Value: `DEAT`

The event when mortal life terminates."""

GEDCOM_TAG_DESCENDANTS = "DESC"
"""Value: `DESC`

Pertaining to offspring of an individual."""

GEDCOM_TAG_DESCENDANTS_INT = "DESI"
"""Value: `DESI`

Indicates an interest in research to identify additional descendants of this
individual. (See also `gedcom.tags.GEDCOM_TAG_ANCES_INTEREST`)"""

GEDCOM_TAG_DESTINATION = "DEST"
"""Value: `DEST`

A system receiving data."""

GEDCOM_TAG_DIVORCE = "DIV"
"""Value: `DIV`

The event of disolving a marriage through civil action."""

GEDCOM_TAG_DIVORCE_FILED = "DIVF"
"""Value: `DIVF`

An event of filing for a divorce by a spouse."""

GEDCOM_TAG_PHY_DESCRIPTION = "DSCR"
"""Value: `DSCR`

The physical characteristics of a person, place, or thing."""

GEDCOM_TAG_EDUCATION = "EDUC"
"""Value: `EDUC`

Indicator of a level of education attained."""

GEDCOM_TAG_EMAIL = "EMAIL"
"""Value: `EMAIL`

An electronic address that can be used for contact such as an email address."""

GEDCOM_TAG_EMIGRATION = "EMIG"
"""Value: `EMIG`

An event of leaving one's homeland with the intent of residing elsewhere."""

GEDCOM_TAG_ENDOWMENT = "ENDL"
"""Value: `ENDL`

A religious event where an endowment ordinance for an individual was performed
by priesthood authority in an LDS temple."""

GEDCOM_TAG_ENGAGEMENT = "ENGA"
"""Value: `ENGA`

An event of recording or announcing an agreement between two people to become
married."""

GEDCOM_TAG_EVENT = "EVEN"
"""Value: `EVEN`

A noteworthy happening related to an individual, a group, or an organization."""

GEDCOM_TAG_FACT = "FACT"
"""Value: `FACT`

Pertaining to a noteworthy attribute or fact concerning an individual, a group,
or an organization. A `FACT` structure is usually qualified or classified by a
subordinate use of the `gedcom.tags.GEDCOM_TAG_TYPE` tag."""

GEDCOM_TAG_FAMILY = "FAM"
"""Value: `FAM`.

Identifies a legal, common law, or other customary relationship of man and woman
and their children, if any, or a family created by virtue of the birth of a
child to its biological father and mother."""

GEDCOM_TAG_FAMILY_CHILD = "FAMC"
"""Value: `FAMC`

Identifies the family in which an individual appears as a child."""

GEDCOM_TAG_FAMILY_FILE = "FAMF"
"""Value: `FAMF`

Pertaining to, or the name of, a family file. Names stored in a file that are
assigned to a family for doing temple ordinance work."""

GEDCOM_TAG_FAMILY_SPOUSE = "FAMS"
"""Value: `FAMS`

Identifies the family in which an individual appears as a spouse."""

GEDCOM_TAG_FAX = "FAX"
"""Value: `FAX`

A FAX telephone number appropriate for sending data facsimiles."""

GEDCOM_TAG_FIRST_COMMUNION = "FCOM"
"""Value: `FCOM`

A religious rite, the first act of sharing in the Lord's supper as part of
church worship."""

GEDCOM_TAG_FILE = "FILE"
"""Value: `FILE`

An information storage place that is ordered and arranged for preservation and
reference."""

GEDCOM_TAG_PHONETIC = "FONE"
"""Value: `FONE`

A phonetic variation of a superior text string."""

GEDCOM_TAG_FORMAT = "FORM"
"""Value: `FORM`

An assigned name given to a consistent format in which information can be
conveyed."""

GEDCOM_TAG_GEDCOM = "GEDC"
"""Value: `GEDC`

Information about the use of GEDCOM in a transmission."""

GEDCOM_TAG_GIVEN_NAME = "GIVN"
"""Value: `GIVN`

A given or earned name used for official identification of a person."""

GEDCOM_TAG_GRADUATION = "GRAD"
"""Value: `GRAD`

An event of awarding educational diplomas or degrees to individuals."""

GEDCOM_TAG_HEADER = "HEAD"
"""Value: `HEAD`

Identifies information pertaining to an entire GEDCOM transmission."""

GEDCOM_TAG_HUSBAND = "HUSB"
"""Value: `HUSB`

An individual in the family role of a married man or father."""

GEDCOM_TAG_IDENT_NUMBER = "IDNO"
"""Value: `IDNO`

A number assigned to identify a person within some significant external system."""

GEDCOM_TAG_IMMIGRATION = "IMMI"
"""Value: `IMMI`

An event of entering into a new locality witht he intent of residing there."""

GEDCOM_TAG_INDIVIDUAL = "INDI"
"""Value: `INDI`

A person."""

GEDCOM_TAG_LANGUAGE = "LANG"
"""Value: `LANG`

The name of the language used in a communication or transmission of information."""

GEDCOM_TAG_LATITUDE = "LATI"
"""Value: `LATI`

A value indicating a coordinate position on a line, plane, or space."""

GEDCOM_TAG_LEGATEE = "LEGA"
"""Value: `LEGA`

A role of an individual acting as a person receiving a bequest or legal devise."""

GEDCOM_TAG_LONGITUDE = "LONG"
"""Value: `LONG`

A value indicating a coordinate position on a line, plane, or space."""

GEDCOM_TAG_MAP = "MAP"
"""Value: `MAP`

Pertains to a representation of measurements usually presented in a graphical
form."""

GEDCOM_TAG_MARRIAGE_BANN = "MARB"
"""Value: `MARB`.

An event of an official public notice given that two people intend to marry."""

GEDCOM_TAG_MARR_CONTRACT = "MARC"
"""Value: `MARC`.

An event of recording a formal agreement of marriage, including the prenuptial
agreement in which marriage partners reach agreement about the property rights
of one or both, securing property to their children."""

GEDCOM_TAG_MARR_LICENSE = "MARL"
"""Value: `MARL`.

An event of obtaining a legal license to marry."""

GEDCOM_TAG_MARRIAGE = "MARR"
"""Value: `MARR`.

A legal, common-law, or customary event of creating a family unit of a man and
a woman as husband and wife."""

GEDCOM_TAG_MARR_SETTLEMENT = "MARS"
"""Value: `MARS`.

An event of creating an agreement between two people contemplating marriage,
at which time they agree to release or modify property rights that would
otherwise arise from the marriage."""

GEDCOM_TAG_MEDIA = "MEDI"
"""Value: `MEDI`.

Identifies information about the media or having to do with the medium in which
information is stored."""

GEDCOM_TAG_NAME = "NAME"
"""Value: `NAME`.

A word or combination of words used to help identify an individual, title, or
other item. More than one `NAME` line should be used for people who were known
by multiple names."""

GEDCOM_TAG_NATIONALITY = "NATI"
"""Value: `NATI`

The national heritage of an individual."""

GEDCOM_TAG_NATURALIZATION = "NATU"
"""Value: `NATU`

The event of obtaining citizenship."""

GEDCOM_TAG_CHILDREN_COUNT = "NCHI"
"""Value: `NCHI`

The number of children that this person is known to be the parent of (all
marriages) when subordinate to an individual, or that belong to this family
when subordinate to a `gedcom.tags.GEDCOM_TAG_FAMILY` record."""

GEDCOM_TAG_NICKNAME = "NICK"
"""Value: `NICK`

A descriptive or familiar that is used instead of, or in addition to, one's
proper name."""

GEDCOM_TAG_MARRIAGE_COUNT = "NMR"
"""Value: `NMR`

The number of times this person has participated in a family as a spouse or
parent."""

GEDCOM_TAG_NOTE = "NOTE"
"""Value: `NOTE`

Additional information provided by the submitter for understanding the
enclosing data."""

GEDCOM_TAG_NAME_PREFIX = "NPFX"
"""Value: `NPFX`

Text which appears on a name line before the given and surname parts of a name.
i.e. ( Lt. Cmndr. ) Joseph /Allen/ jr. In this example Lt. Cmndr. is considered
as the name prefix portion."""

GEDCOM_TAG_NAME_SUFFIX = "NSFX"
"""Value: `NSFX`

Text which appears on a name line after or behind the given and surname parts
of a name. i.e. Lt. Cmndr. Joseph /Allen/ ( jr. ) In this example jr. is
considered as the name suffix portion."""

GEDCOM_TAG_OBJECT = "OBJE"
"""Value: `OBJE`

Pertaining to a grouping of attributes used in describing something. Usually
referring to the data required to represent a multimedia object, such an audio
recording, a photograph of a person, or an image of a document."""

GEDCOM_TAG_OCCUPATION = "OCCU"
"""Value: `OCCU`

The type of work or profession of an individual."""

GEDCOM_TAG_ORDINANCE = "ORDI"
"""Value: `ORDI`

Pertaining to a religious ordinance in general."""

GEDCOM_TAG_ORDINATION = "ORDN"
"""Value: `ORDN`

A religious event of receiving authority to act in religious matters."""

GEDCOM_TAG_PAGE = "PAGE"
"""Value: `PAGE`

A number or description to identify where information can be found in a
referenced work."""

GEDCOM_TAG_PEDIGREE = "PEDI"
"""Value: `PEDI`

Information pertaining to an individual to parent lineage chart."""

GEDCOM_TAG_PHONE = "PHON"
"""Value: `PHON`

A unique number assigned to access a specific telephone."""

GEDCOM_TAG_PLACE = "PLAC"
"""Value: `PLAC`

A jurisdictional name to identify the place or location of an event."""

GEDCOM_TAG_POSTAL_CODE = "POST"
"""Value: `POST`

A code used by a postal service to identify an area to facilitate mail handling."""

GEDCOM_TAG_PRIVATE = "PRIV"
"""Value: `PRIV`

Flag for private address or event."""

GEDCOM_TAG_PROBATE = "PROB"
"""Value: `PROB`

An event of judicial determination of the validity of a will. May indicate
several related court activities over several dates."""

GEDCOM_TAG_PROPERTY = "PROP"
"""Value: `PROP`

Pertaining to possessions such as real estate or other property of interest."""

GEDCOM_TAG_PUBLICATION = "PUBL"
"""Value: `PUBL`

Refers to when and/or were a work was published or created."""

GEDCOM_TAG_QUALITY_OF_DATA = "QUAY"
"""Value: `QUAY`

An assessment of the certainty of the evidence to support the conclusion drawn
from evidence."""

GEDCOM_TAG_REFERENCE = "REFN"
"""Value: `REFN`

A description or number used to identify an item for filing, storage, or other
reference purposes."""

GEDCOM_TAG_RELATIONSHIP = "RELA"
"""Value: `RELA`

A relationship value between the indicated contexts."""

GEDCOM_TAG_RELIGION = "RELI"
"""Value: `RELI`

A religious denomination to which a person is affiliated or for which a record
applies."""

GEDCOM_TAG_REPOSITORY = "REPO"
"""Value: `REPO`

An institution or person that has the specified item as part of their 
collection(s)."""

GEDCOM_TAG_RESIDENCE = "RESI"
"""Value: `RESI`

The act of dwelling at a place for a period of time."""

GEDCOM_TAG_RESTRICTION = "RESN"
"""Value: `RESN`

A processing indicator signifying access to information has been denied or
otherwise restricted."""

GEDCOM_TAG_RETIREMENT = "RETI"
"""Value: `RETI`

An event of exiting an occupational relationship with an employer after a
qualifying time period."""

GEDCOM_TAG_REC_FILE_NUMBER = "RFN"
"""Value: `RFN`

A permanent number assigned to a record that uniquely identifies it within a
known file."""

GEDCOM_TAG_REC_ID_NUMBER = "RIN"
"""Value: `RIN`

A number assigned to a record by an originating automated system that can be
used by a receiving system to report results pertaining to that record."""

GEDCOM_TAG_ROLE = "ROLE"
"""Value: `ROLE`

A name given to a role played by an individual in connection with an event."""

GEDCOM_TAG_ROMANIZED = "ROMN"
"""Value: `ROMN`

A romanized variation of a superior text string."""

GEDCOM_TAG_SEX = "SEX"
"""Value: `SEX`

Indicates the sex of an individual--male or female."""

GEDCOM_TAG_SEALING_CHILD = "SLGC"
"""Value: `SLGC`

A religious event pertaining to the sealing of a child to his or her parents in
an LDS temple ceremony."""

GEDCOM_TAG_SEALING_SPOUSE = "SLGS"
"""Value: `SLGS`

A religious event pertaining to the sealing of a husband and wife in an LDS
temple ceremony."""

GEDCOM_TAG_SOURCE = "SOUR"
"""Value: `SOUR`

The initial or original material from which information was obtained."""

GEDCOM_TAG_SURN_PREFIX = "SPFX"
"""Value: `SPFX`

A name piece used as a non-indexing pre-part of a surname."""

GEDCOM_TAG_SOC_SEC_NUMBER = "SSN"
"""Value: `SSN`

A number assigned by the United States Social Security Administration. Used for
tax identification purposes."""

GEDCOM_TAG_STATE = "STAE"
"""Value: `STAE`

A geographical division of a larger jurisdictional area, such as a State within
the United States of America."""

GEDCOM_TAG_STATUS = "STAT"
"""Value: `STAT`

An assessment of the state or condition of something."""

GEDCOM_TAG_SUBMITTER = "SUBM"
"""Value: `SUBM`

An individual or organization who contributes genealogical data to a file or
transfers it to someone else."""

GEDCOM_TAG_SUBMISSION = "SUBN"
"""Value: `SUBN`

Pertains to a collection of data issued for processing."""

GEDCOM_TAG_SURNAME = "SURN"
"""Value: `SURN`

A family name passed on or used by members of a family."""

GEDCOM_TAG_TEMPLE = "TEMP"
"""Value: `TEMP`

The name or code that represents the name a temple of the LDS Church."""

GEDCOM_TAG_TEXT = "TEXT"
"""Value: `TEXT`

The exact wording found in an original source document."""

GEDCOM_TAG_TIME = "TIME"
"""Value: `TIME`

A time value in a 24-hour clock format, including hours, minutes, and optional
seconds, separated by a colon (:). Fractions of seconds are shown in decimal
notation."""

GEDCOM_TAG_TITLE = "TITL"
"""Value: `TITL`

A description of a specific writing or other work, such as the title of a book
when used in a source context, or a formal designation used by an individual
in connection with positions of royalty or other social status, such as Grand
Duke."""

GEDCOM_TAG_TRAILER = "TRLR"
"""Value: `TRLR`

At level 0, specifies the end of a GEDCOM transmission."""

GEDCOM_TAG_TYPE = "TYPE"
"""Value: `TYPE`

A further qualification to the meaning of the associated superior tag. The value
does not have any computer processing reliability. It is more in the form of a
short one or two word note that should be displayed any time the associated data
is displayed."""

GEDCOM_TAG_VERSION = "VERS"
"""Value: `VERS`

Indicates which version of a product, item, or publication is being used or
referenced."""

GEDCOM_TAG_WIFE = "WIFE"
"""Value: `WIFE`

An individual in the role as a mother and/or married woman."""

GEDCOM_TAG_WEB = "WWW"
"""Value: `WWW`

World Wide Web home page."""

GEDCOM_TAG_WILL = "WILL"
"""Value: `WILL`

A legal document treated as an event, by which a person disposes of his or her
estate, to take effect after death. The event date is the date the will was
signed while the person was alive. (See also `gedcom.tags.GEDCOM_TAG_PROBATE`)"""
