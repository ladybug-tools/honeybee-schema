[![Build Status](https://travis-ci.org/ladybug-tools-in2/honeybee-schema.svg?branch=master)](https://travis-ci.org/ladybug-tools-in2/honeybee-schema)
[![Coverage Status](https://coveralls.io/repos/github/ladybug-tools-in2/honeybee-schema/badge.svg?branch=master)](https://coveralls.io/github/ladybug-tools-in2/honeybee-schema)

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

# honeybee-schema

Honeybee Data-Model Objects

## Installation
```console
pip install honeybee-schema
```

## QuickStart
```python
import honeybee_schema

```

## API Documentation

[Model Schema](https://ladybug-tools-in2.github.io/honeybee-schema/model.html)

[Energy Simulation Parameter Schema](https://ladybug-tools-in2.github.io/honeybee-schema/simulation-parameter.html)

## Local Development
1. Clone this repo locally
```console
git clone git@github.com:ladybug-tools-in2/honeybee-schema

# or

git clone https://github.com/ladybug-tools-in2/honeybee-schema
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
