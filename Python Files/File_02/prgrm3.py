# Read the file and print only the messages (ignore names).
msg=[]
with open('guestbook.txt','r') as f:

    fdata=f.readlines()

    for line in fdata:

        data=line.strip().split("|")

        # print(data[1])
        
        msg.append(data[1])

print(msg)

