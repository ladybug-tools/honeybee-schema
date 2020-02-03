"""Objects used as alternatives to numerical properties."""
from pydantic import BaseModel, constr


class NoLimit(BaseModel):

    type: constr(regex='^NoLimit$') = 'NoLimit'


class Autocalculate(BaseModel):

    type: constr(regex='^Autocalculate$') = 'Autocalculate'


class Autosize(BaseModel):

    type: constr(regex='^Autosize$') = 'Autosize'
