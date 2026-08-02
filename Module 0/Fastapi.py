from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="FastAPI CRUD Without Database")


products = []

class Product(BaseModel):
    id: int
    name: str
    price: float


@app.get("/")
def home():
    return {"message": "FastAPI CRUD"}


# Create Product


@app.post("/products")
def create_product(product: Product):

    for p in products:
        if p["id"] == product.id:
            raise HTTPException(status_code=400, detail="Product ID already exists")

    products.append(product.model_dump())

    return {
        "message": "Product Added Successfully",
        "product": product
    }

# Get All Products


@app.get("/products")
def get_products():
    return products

# -----------------------
# Get Product By ID
# -----------------------

@app.get("/products/{id}")
def get_product(id: int):

    for product in products:
        if product["id"] == id:
            return product

    raise HTTPException(status_code=404, detail="Product Not Found")


# Update Product

@app.put("/products/{id}")
def update_product(id: int, updated_product: Product):

    for index, product in enumerate(products):

        if product["id"] == id:
            products[index] = updated_product.model_dump()
            return {
                "message": "Product Updated",
                "product": updated_product
            }

    raise HTTPException(status_code=404, detail="Product Not Found")


# Delete Product

@app.delete("/products/{id}")
def delete_product(id: int):

    for index, product in enumerate(products):

        if product["id"] == id:
            products.pop(index)
            return {"message": "Product Deleted Successfully"}

    raise HTTPException(status_code=404, detail="Product Not Found")