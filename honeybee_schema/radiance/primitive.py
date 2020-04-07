
"""Base Radiance Modifier Schema"""
from pydantic import Field, constr
from typing import List

from .._base import IDdBaseModel


class Primitive(IDdBaseModel):
    """Base class for Radiance Primitives"""

    modifier: str = Field(
        default='void',
        min_length=1,
        max_length=100,
        description='Material modifier (Default: "void").'
    )

    values: List[constr(min_length=1, max_length=100)] = Field(
        default=[[], [], []],
        description='Array of three sub-arrays for primitive data. '
                    '(Default: [[], [], []]).'
    )

    # TODO: Clarify if we want actual list of primitives here versus the string names.
    dependencies: List[constr(min_length=1, max_length=100)] = Field(
        default=[],
        description='List of strings for primitive names that this primitive depends on. '
                    'This argument is only useful for defining advanced primitives '
                    'where the primitive is defined based on other primitives '
                    '(Default: []).'
    )


if __name__ == '__main__':
    print(Primitive.schema_json(indent=2))
