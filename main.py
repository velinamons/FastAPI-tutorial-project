from enum import Enum

from fastapi import FastAPI

from pydantic_models import Item


# By inheriting from str the API docs will know that the values must be type string
# and will be able to render correctly
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# declare its type as the model you created - Item
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# using model_dump instead of items because of pydantic v2
# Pydantic model - > request body
# singular type - > query parameter
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


# When you declare other function parameters that are not part of the path parameters
# they are automatically interpreted as "query" parameters
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Path parameters with types (using Python type annotations)
# with that type declaration, FastAPI gives automatic request "parsing" and data validation
# All the data validation is performed under the hood by Pydantic
@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


# Path operations are evaluated in order
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# path parameter with a type annotation using the enum class (ModelName)
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    # Compare enumeration members
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    # You can get the actual value using your_enum_member.value
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    # You can return enum members from your path operation
    # They will be converted to their corresponding values before returning
    return {"model_name": model_name, "message": "Have some residuals"}


# Path parameters containing paths
# :path option directly from Starlette
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
