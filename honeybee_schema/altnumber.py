"""Objects used as alternatives to numerical properties."""
from pydantic import constr
from ._base import NoExtraBaseModel


class NoLimit(NoExtraBaseModel):

    type: constr(regex='^NoLimit$') = 'NoLimit'


class Autocalculate(NoExtraBaseModel):

    type: constr(regex='^Autocalculate$') = 'Autocalculate'


class Autosize(NoExtraBaseModel):

    type: constr(regex='^Autosize$') = 'Autosize'
