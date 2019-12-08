"""generate openapi docs."""
from honeybee_model_schema.openapi import get_openapi
import json

print('Generating documentation...')
openapi = get_openapi()
with open('./docs/openapi.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)
