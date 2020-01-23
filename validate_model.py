from honeybee_schema.model import Model

import sys
import os
import json


if __name__ == '__main__':
    # check the input arguments
    assert len(sys.argv) >= 2, 'Model JSON argument not included.'
    model_json = sys.argv[1]
    assert os.path.isfile(model_json), 'No JSON file found at {}.'.format(model_json)
    
    # validate the Model JSON
    print('Validating Model JSON ...')
    Model.parse_file(model_json)
    print('Pydantic validation passed.')
    try:
        import honeybee.model as hb_model
        with open(model_json) as json_file:
            data = json.load(json_file)
        parsed_model = hb_model.Model.from_dict(data)
        print('Python re-serialization passed.')
        print('Congratulations! Yout Model JSON is valid!')
    except ImportError:
        print('Honeybee is not installed. A reserialzation test will not be run.\n'
              'Use `pip install honeybee-core` to install Honeybee.')
