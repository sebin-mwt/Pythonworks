from fastapi import FastAPI,Response,status,HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app=FastAPI()

class Student(BaseModel):

    name: str

    age : int

    is_student : bool =True


try:
    # Connect to your postgres DB
    conn = psycopg2.connect(host="localhost",database="fastapi",user="postgres",password="Password@123", cursor_factory=RealDictCursor)
    
    # Open a cursor to perform database operations
    cur = conn.cursor()

    print("Database connection successfull !!!")

except Exception as e:
    print("Error Database connection Failed...", e)



my_data=[{"name":"appu","school":"hkps","age":12,"is_student":True ,"id":1}]


 # To add a student to student table
@app.post("/user", status_code=status.HTTP_201_CREATED)  
def userData(data : Student):   

    cur.execute("""INSERT INTO student (name,age,is_student) VALUES (%s , %s,%s) RETURNING * """,
                (data.name, data.age,data.is_student))

    new_student=cur.fetchone()
    conn.commit()

    return {"Data added Successfully" : new_student}
   

# To get the names of the students details from student table
@app.get("/user")
def getuser():  

    cur.execute(""" SELECT * FROM student """)
    students=cur.fetchall()
    # print(students)
    return  students


# To get the details of the particular student
@app.get("/user/{id}")
def getuserbyid(id :int,response:Response):
    
    cur.execute(""" SELECT * from student WHERE id= (%s)  """,(str(id)))
    user_data=cur.fetchone()

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
    
    cur.execute(""" DELETE from student where id=(%s) RETURNING * """,(str(id)))
    deleted_user=cur.fetchone()
    
    if not deleted_user :

        response.status_code=status.HTTP_404_NOT_FOUND
        return {"message" : f"post with id : {id} is not present"}
    
    conn.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/user/update/{id}")
def updateUser(id:int , student:Student):

    cur.execute(""" UPDATE student set name=%s , age =%s, is_student=%s where id=%s returning * """,(student.name,student.age,student.is_student,str(id)))
    updated_user=cur.fetchone()

    if not updated_user:

        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    conn.commit()

    return updated_user 
# {
#     "name":"John",
#     "school":"hkpss",
#     "age":29,
#     "is_student":false,
#     "id":4
# }  data to send api