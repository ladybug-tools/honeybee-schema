[![Build Status](https://travis-ci.org/ladybug-tools-in2/honeybee-model-schema.svg?branch=master)](https://travis-ci.org/ladybug-tools-in2/honeybee-model-schema)
[![Coverage Status](https://coveralls.io/repos/github/ladybug-tools-in2/honeybee-model-schema/badge.svg?branch=master)](https://coveralls.io/github/ladybug-tools-in2/honeybee-model-schema)

[![Python 2.7](https://img.shields.io/badge/python-2.7-green.svg)](https://www.python.org/downloads/release/python-270/) [![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

# honeybee-model-schema

Honeybee Data-Model Objects

## Installation
```console
pip install honeybee-model-schema
```

## QuickStart
```python
import honeybee_model_schema

```

## API Documentation
[Model Schema](https://ladybug-tools-in2.github.io/honeybee-model-schema/model.html)
[Energy Simulation Parameter Schema](https://ladybug-tools-in2.github.io/honeybee-model-schema/simulation-parameter.html)

## Local Development
1. Clone this repo locally
```console
git clone git@github.com:ladybug-tools-in2/honeybee-model-schema

# or

git clone https://github.com/ladybug-tools-in2/honeybee-model-schema
```
2. Install dependencies:
```console
cd honeybee-model-schema
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
