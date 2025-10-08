from fastapi import FastAPI
from fastapi.params import Body
app=FastAPI()

@app.get("/")
def hello():

    return {"message":"hello world welcome to FastAPI"}

@app.get("/user/")
def user_name():

    return {"message": "hei this is sebin"}

@app.post('/username')
def username(data: dict = Body(...)):   

    print(data)
    if not data:
        return {"message" : "data not received"}
    
    return {"message" : "successfully received data"}