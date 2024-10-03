from pydantic import BaseModel
class userModel(BaseModel):
    username:str
    email:str
    password:str

class logInModel(BaseModel):
    username:str
    password:str

class fileUploader(BaseModel):
    file_name:str
    file_type:str
    user_id:int

class validationModel(BaseModel):
    file_name:str
    user_id:int