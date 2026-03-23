from fastapi import FastAPI, HTTPException, status, Path
from typing import Optional 
from pydantic import BaseModel

app = FastAPI()

users = {
    1 :{
        "name":"Evin",
        "website":"www.github.com/Evin009", 
        "age": 20, 
        "role":"Developer"
    }
}

# Base Pydantic Models -- Specifing datatypes of each values of data when uploading and updatingv
class Users(BaseModel):
    name:str
    website:str
    age:int
    role:str


class UpdateUser(BaseModel):
    name: Optional[str] = None
    website: Optional[str] = None
    age: Optional[int] = None
    role: Optional[str] = None 
    
    

# endpoint(URL)
# www.myworld.com/
@app.get("/")
def root():
    return {"message":"Welcome to your fastapi intro"}

# www.myworld.com/users/1
# get users
@app.get("/users/{user_id}")
def get_user(user_id:int = Path(..., description="The ID you want to get", gt=0, lt=100)):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not Found!")
    return users[user_id]


# create a user
# www.myworld.com/users/2 adding user 2
@app.post("/users/{user_id}", status_code=status.HTTP_201_CREATED)
def create_user(user_id:int, user:Users):
    if user_id in users:
        raise HTTPException(status_code=400, detail="User already exists")
    
    users[user_id] = user.dict()
    return user


# Update a user
# www.myworld.com/users/2 updating user 2
@app.put("/users/{user_id}")
def update_user(user_id:int, user:UpdateUser):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="No such User with the id exists")
    
    current_user = users[user_id] 
    
    if user.name is not None:
        current_user["name"] = user.name   
    if user.website is not None:
        current_user["website"] = user.website   
    if user.age is not None:
        current_user["age"] = user.age   
    if user.role is not None:
        current_user["role"] = user.role   

    return current_user

# Delete a user
# www.myworld.com/users/1 deleteing user 1
@app.delete("/users/{user_id}")
def delete_user(user_id:int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not exists")
    
    deleted_user = users.pop(user_id)
    return {"message":"User has been deleted", "delete_user":deleted_user}


# search for a user
# www.myworld.com/users/search?Evin
@app.get("/users/search/")
def search_by_name(name: Optional[str] = None):
    if not name:
        return {"message":"Name pamarater is required!"}

    for user in users.values():
        if user["name"] == name:
            return user
    
    raise HTTPException(status_code=404, detail="User not found!") 