from pydantic import BaseModel


# Create data model using pydantic BaseModel
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
