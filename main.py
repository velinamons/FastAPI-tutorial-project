from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Path parameters with types (using Python type annotations)
# with that type declaration, FastAPI gives automatic request "parsing" and data validation
# All the data validation is performed under the hood by Pydantic
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
