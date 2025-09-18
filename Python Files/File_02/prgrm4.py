#Count the total number of guests in the guestbook.
counts=0
with open('guestbook.txt','r') as f:

    fdata=f.readlines()
    
    for data in fdata :

        data=data.strip()

        if data:

            counts+=1


print(counts)