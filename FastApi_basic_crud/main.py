from fastapi import FastAPI,Response,status,HTTPException
from pydantic import BaseModel

app=FastAPI()

class Student(BaseModel):

    name: str

    school : str

    age : int

    is_student : bool

    id : int

my_data=[{"name":"appu","school":"hkps","age":12,"is_student":True ,"id":1}]

 # to add a student to my_data
@app.post("/user", status_code=status.HTTP_201_CREATED)  
def userData(data : Student,response:Response):   

    # print(data)
    datas=dict(data)

    my_data.append(datas)
    # response.status_code=status.HTTP_201_CREATED
    return {"message" : my_data}

# To get the names of the students
@app.get("/user")
def getuser():  

    names=[v for dic in my_data for k,v in dic.items() if k=="name"]

    return {f"availavle students are {names} "} 


# To get the details of the particular student
@app.get("/user/{id}")
def getuserbyid(id:int,response:Response):
    user_data=None
    for dic in my_data:
        if dic["id"]==int(id):
            user_data=dic
            print(user_data)

    if not user_data:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid data present")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"Message" : f"student with id :{id} is not available"}
    
    return user_data

# To get the details of the last added 
@app.get("/user/recent/student")
def latestuser():

    length=len(my_data) - 1
    return my_data[length]


@app.delete("/user/{id}/delete")
def deleteuser(id: int,response:Response):
    index=None
    for i,s in enumerate(my_data):
        if s['id']==int(id):
            index=i
            break

    if index is None :
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No element in this index")
    
    print(my_data)
    my_data.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/user/update/{id}")
def updateUser(id:int , student:Student):

    index=None
    for i,s in enumerate(my_data):
        if s['id']==int(id):
            index=i
            break

    if index is None :
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No element in this index")
    
    student_dict=dict(student)
    my_data[index]=student_dict
    print(my_data[index])
    return {"message":my_data[index]}

# {
#     "name":"John",
#     "school":"hkpss",
#     "age":29,
#     "is_student":false,
#     "id":4
# }  data to send api