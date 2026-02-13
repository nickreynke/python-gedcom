<p align="center">
  <img src="logo.png">
</p>

<p align="center">
    <a href="https://pypi.org/project/python-gedcom/" target="_blank"><img src="https://img.shields.io/pypi/v/python-gedcom.svg" alt="PyPI"></a>
    <a href="https://github.com/nickreynke/python-gedcom/releases" target="_blank"><img src="https://img.shields.io/github/release/nickreynke/python-gedcom.svg" alt="GitHub release"></a>
    <img src="https://img.shields.io/badge/GEDCOM%20format%20version-5.5-yellowgreen.svg" alt="GEDCOM format version 5.5">
    <img src="https://img.shields.io/badge/Python%20versions-3.8%20to%203.12-yellowgreen.svg" alt="Python versions 3.8 to 3.12">
</p>

<p align="center">
    A Python module for parsing, analyzing, and manipulating GEDCOM files.
</p>

<p align="center">
    GEDCOM files contain ancestry data. The parser is currently supporting the GEDCOM 5.5 format which is detailed
    <a href="https://chronoplexsoftware.com/gedcomvalidator/gedcom/gedcom-5.5.pdf" target="_blank">here</a>.
</p>

## Documentation

Documentation can be found here: https://nickreynke.github.io/python-gedcom/gedcom/index.html

## Changelog

For the latest changes please have a look at the [`CHANGELOG.md`](CHANGELOG.md) file.

The current development process can be tracked in the [develop branch](https://github.com/nickreynke/python-gedcom/tree/develop).

## Common problems

* When you name your script `gedcom.py`, and import the `gedcom` module from this package, running your script won't
  work because Python will try to resolve imports like `gedcom.element.individual` from within your `gedcom.py` but
  not from within the module from this package. Rename your file in this case. ([#26](https://github.com/nickreynke/python-gedcom/issues/26))

## Local development

Local development is done using [uv](https://github.com/astral-sh/uv).

### Running tests

1. Run `uv sync` to install dependencies
1. Run tests with [pytest](https://docs.pytest.org/) (`uv run pytest` in your console)

### Generating docs

1. Run `uv sync` to install dependencies
1. Run `uv run pdoc3 --html -o docs/ gedcom --force` to generate docs into the `docs/` directory

> To develop docs run `uv run pdoc3 --http localhost:8000 gedcom`
> to watch files and instantly see changes in your browser under http://localhost:8000.

### Uploading a new package to PyPI

1. Run `uv sync` to install dependencies
1. Run `uv build` to generate distribution archives
1. Run `uv run twine upload --repository-url https://test.pypi.org/legacy/ dist/*` to upload the archives to the Test Python Package Index repository

> When the package is ready to be published to the real Python Package Index
the `repository-url` is `https://upload.pypi.org/legacy/`.
>
> `uv run twine upload --repository-url https://upload.pypi.org/legacy/ dist/*`

## History

This module was originally based on a GEDCOM parser written by 
Daniel Zappala at Brigham Young University (Copyright (C) 2005) which
was licensed under the GPL v2 and then continued by
[Mad Price Ball](https://github.com/madprime) in 2012.

The project was taken over by [Nicklas Reincke](https://github.com/nickreynke) in 2018.
Together with [Damon Brodie](https://github.com/nomadyow) a lot of changes were made and the parser was optimized.

## License

Licensed under the [GNU General Public License v2](http://www.gnu.org/licenses/gpl-2.0.html)

**Python GEDCOM Parser**
<br>Copyright (C) 2018 Damon Brodie (damon.brodie at gmail.com)
<br>Copyright (C) 2018-2019 Nicklas Reincke (contact at reynke.com)
<br>Copyright (C) 2016 Andreas Oberritter
<br>Copyright (C) 2012 Madeleine Price Ball
<br>Copyright (C) 2005 Daniel Zappala (zappala at cs.byu.edu)
<br>Copyright (C) 2005 Brigham Young University

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
