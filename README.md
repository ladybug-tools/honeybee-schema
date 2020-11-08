[![Build Status](https://travis-ci.com/ladybug-tools/honeybee-schema.svg?branch=master)](https://travis-ci.com/ladybug-tools/honeybee-schema)
[![Coverage Status](https://coveralls.io/repos/github/ladybug-tools/honeybee-schema/badge.svg?branch=master)](https://coveralls.io/github/ladybug-tools/honeybee-schema)

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

# honeybee-schema

Honeybee Data-Model Objects

This code was partially developed under the [Wells Fargo Innovation Incubator grant](https://newsroom.wf.com/press-release/community/five-clean-tech-startups-added-wells-fargo-innovation-incubator) with help from the
[OpenStudio Team](https://github.com/NREL/OpenStudio) at [NREL](https://www.nrel.gov/).

## Installation

```console
pip install honeybee-schema
```

## QuickStart

```python
import honeybee_schema

```

## API Documentation

[Model Schema](https://ladybug-tools.github.io/honeybee-schema/model.html)

[Energy Simulation Parameter Schema](https://ladybug-tools.github.io/honeybee-schema/simulation-parameter.html)

## Local Development

1. Clone this repo locally

```console
git clone git@github.com:ladybug-tools/honeybee-schema

# or

git clone https://github.com/ladybug-tools/honeybee-schema
```

2. Install dependencies:

```console
cd honeybee-schema
pip install -r dev-requirements.txt
pip install -r requirements.txt
```

3. Run Tests:

```console
python -m pytest tests/
```

4. Generate Documentation:

```python
python ./docs.py
```

5. Generate Sample Files:

```python
python ./scripts/export_samples.py
```
