from pydantic import BaseModel



class ProductModel(BaseModel):
    name: str
    description: str
    price: float


class ProductModelResponse(BaseModel):
    id: str
    name: str
    description: str
    price: float
    available: bool