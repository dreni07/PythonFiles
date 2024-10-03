from fastapi import FastAPI
import models
import database

app = FastAPI()


@app.post('/addUser')
async def addUseri(user:models.userModel):
    validating = database.checking_username(user)
    if validating['success'] == 'User Not Exists':
        adding_user = database.insertData(user)
        if adding_user['success'] == 'True':
            return {"added":'With Success'}
        elif adding_user['success'] == 'False':
            return {'addedd':'Not Added Sorry'}
        else:
            return {'addedd':'Query Problem'}
    else:
        return {'added':'User With That Username Exists'}

@app.post('/logIn')
async def logIn(user:models.logInModel):
    checking = database.logIn(user)
    if checking['success'] == 'True':
        return {'Valid':'success','data':checking['data']}
    else:
        return {'Valid':'False'}

@app.post('/addFile')
async def addingFile(file:models.fileUploader):
    file_validation = database.is_file_valid(file)
    if file_validation['success'] == 'File Does Not Exist':
        adding_file = database.addingFile(file)
        if adding_file['File Added'] == 'Successfully':
            return {'success':'True'}
        else:
            return {'success':'False'}
    else:
        return {'success':'File Exists'}

@app.get('/seeFiles/{userId}')
async def seeFiles(userId:int):
    seeing_file = database.see_files(userId)
    if seeing_file['data'] != 'Failed':
        return seeing_file['data']
    else:
        return {'answer':'Went Wrong'}





