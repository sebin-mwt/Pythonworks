# Create a file called guestbook.txt and write three initial guest entries. Each entry should be in this format:

# Name: Alice | Message: Hello everyone!
# Name: Bob | Message: Excited to be here!
# Name: Charlie | Message: Great event!

f=open("guestbook.txt","w")

f.write("Name : Alice | Message : Hello Everyone \n")
f.write("Name : Bob | Message : Excited to be here \n")
f.write("Name : Charlie | Message : Great Event \n")

f.close()


fr=open("guestbook.txt",'r')
data=fr.read()
print(data)

fr.close()

