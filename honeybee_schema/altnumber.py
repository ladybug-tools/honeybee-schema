"""Objects used as alternatives to numerical properties."""
from typing import Literal
from ._base import NoExtraBaseModel


class NoLimit(NoExtraBaseModel):

    type: Literal['NoLimit'] = 'NoLimit'


class Autocalculate(NoExtraBaseModel):

    type: Literal['Autocalculate'] = 'Autocalculate'


class Autosize(NoExtraBaseModel):

    type: Literal['Autosize'] = 'Autosize'
