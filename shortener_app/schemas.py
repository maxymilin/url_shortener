from pydantic import BaseModel


class URLBase(BaseModel):
    """URL base class what has target_url.
    Contains 'long' urls form users.
    """

    target_url: str


class URL(URLBase):
    """URL with chortered url and user ip."""

    url: str

    class Config:
        """Tell pydantic to work with a database model"""

        orm_mode = True
