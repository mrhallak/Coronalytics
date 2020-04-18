# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Released]
##  [[2.0.1]](https://github.com/mrhallak/Coronalytics/releases/tag/v2.0.1) - 2020-04-18
### Added
- Google style documentation
- [Black code formatting](https://github.com/psf/black)
- Add tests using pytest and pytest-cov
- Used [codecov.io](http://www.codecov.io/) to showcase the testcase coverage
- Bug fixes
- Code refactoring and improvements
### Removed
- docBlockr docstring format

## [[2.0.0]](https://github.com/mrhallak/Coronalytics/releases/tag/v2.0.0) - 2020-03-29
### Added
- ElasticSearch as a NoSQL database
- Kibana for visualization
### Changed
- Fetching data from the JHU API instead of CSVs from the Github repository
### Removed
- Grafana
- Postgres

## [[1.0.0]](https://github.com/mrhallak/Coronalytics/releases/tag/v1.0.0) - 2020-03-24
### Added
- Docker-compose setup
- Pull data from the [JHU CSSE COVID-19 repository](https://github.com/CSSEGISandData/COVID-19)
- Load data in PostgreSQL
- Visualize using Grafana