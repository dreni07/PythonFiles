import requests
new_model = {
    'username':'Dren',
    'email':'drenllaza',
    'password':'DRENBABA'
}
response = requests.post('http://127.0.0.1:8003/addUser',json=new_model)
print(response.json())
