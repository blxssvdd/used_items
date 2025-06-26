from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.products.models import Product
from app.pydantic_models.products import ProductModel

async def create_product(product: ProductModel, db: AsyncSession) -> Product:
    db_product = Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def list_products(db: AsyncSession) -> List[Product]:
    result = await db.execute(select(Product))
    return result.scalars().all()

async def get_product_by_id(product_id: str, db: AsyncSession) -> Optional[Product]:
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalar_one_or_none()

async def update_product(product_id: str, product: ProductModel, db: AsyncSession) -> Optional[Product]:
    db_product = await get_product_by_id(product_id, db)
    if not db_product:
        return None
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def delete_product(product_id: str, db: AsyncSession) -> bool:
    db_product = await get_product_by_id(product_id, db)
    if not db_product:
        return False
    await db.delete(db_product)
    await db.commit()
    return True