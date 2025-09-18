#Search for a specific guest name (e.g., "Bob") and print their message.
inp_name=input("Enter the name :")
data={}
with open('guestbook.txt','r') as f:
    
    fdata=f.readlines()  #['Name : Alice | Message : Hello Everyone \n', 'Name : Bob | Message : Excited to be here \n', 'Name : Charlie | Message : Great Event \n', 'Name: Diana | Message: Looking forward to meeting you all! ']

    for line in fdata:

        lst_data=line.strip().split("|") #['Name : Alice ', ' Message : Hello Everyone']

        name_lst=lst_data[0].split(":")
    
        name=name_lst[1].strip()

        if name==inp_name:

            print(lst_data[1])

            