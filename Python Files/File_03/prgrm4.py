#Calculate and print the average marks of all students.
marks=[]
with open('students.txt') as f:

    fdata=f.readlines()

    for line in fdata:

        data=line.split(":")

        marks.append(int(data[1]))

print(sum(marks)/len(marks))