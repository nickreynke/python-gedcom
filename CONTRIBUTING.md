# Python Gedcom Parser: Contribution Guideline

1. Clone the repo
1. Make your changes
1. (Write appropriate tests within `tests/`)
1. Commit using [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
1. [Open a pull request](https://github.com/madprime/python-gedcom/compare)
1. When checks for the PR fail consider making changes so that the checks pass

## About Conventional Commits

Git committing is done using [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) with NPM.

Consider installing node packages with [NVM](https://github.com/nvm-sh/nvm) and start committing with `npm run commit`.
Git hooks installed via [Husky](https://github.com/typicode/husky) will do the rest.

How to install:

1. Use Node version `12.16.1` (or use [NVM](https://github.com/nvm-sh/nvm) and run `nvm use`)
1. Run `npm install` and then `npm run commit` to commit your changes
