        # Find and print the name(s) of the student(s) with the highest marks.

marks=[]
with open('students.txt') as f:

        fdata=f.readlines()

        for line in fdata:

            data=line.split(":")

            marks.append(int(data[1]))

            
        max_mrk=max(marks)

        for line in fdata:

            data=line.split(":")

            if int(data[1])==max_mrk:

                print(data[0])
