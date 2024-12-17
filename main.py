from enum import Enum

from fastapi import FastAPI


# By inheriting from str the API docs will know that the values must be type string
# and will be able to render correctly
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


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
