from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.products import db_actions
from app.pydantic_models.products import ProductModel, ProductModelResponse
from app.db.users.db_actions import decode_jwt




products_route = APIRouter(prefix="/products", tags=["Products"])

@products_route.post("/", response_model=ProductModelResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductModel,
    db: Annotated[AsyncSession, Depends(get_db)],
    username: Annotated[str, Depends(decode_jwt)]
):
    return await db_actions.create_product(product, db)

@products_route.get("/", response_model=List[ProductModelResponse])
async def get_products(
    db: Annotated[AsyncSession, Depends(get_db)],
    username: Annotated[str, Depends(decode_jwt)]
):
    return await db_actions.list_products(db)

@products_route.get("/{product_id}", response_model=ProductModelResponse)
async def get_product(
    product_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    username: Annotated[str, Depends(decode_jwt)]
):
    product = await db_actions.get_product_by_id(product_id, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@products_route.put("/{product_id}", response_model=ProductModelResponse)
async def update_product(
    product_id: str,
    product: ProductModel,
    db: Annotated[AsyncSession, Depends(get_db)],
    username: Annotated[str, Depends(decode_jwt)]
):
    updated = await db_actions.update_product(product_id, product, db)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@products_route.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    username: Annotated[str, Depends(decode_jwt)]
):
    deleted = await db_actions.delete_product(product_id, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")