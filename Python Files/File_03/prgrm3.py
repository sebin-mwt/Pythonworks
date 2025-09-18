# Search for a student by name entered by the user and print their marks. If not found, print "Student not found."

inp=input("Enter the name :")
flag=False

with open("students.txt",'r') as f :

    fdata=f.readlines()

    for line in fdata: 

        datas=line.split(":")

        name=datas[0].strip()

        if name==inp:

             print(int(datas[1]))

             flag=True

if flag==False:

    print(f'User with name :{inp} doesnt exists !!')