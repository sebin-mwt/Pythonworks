num=int(input("Enter the number :"))
flag=True
if num==(1,2):
    print("prime")
elif num >2 :
    for i in range(2,num):

        if (num % i)==0:

            flag=False
            break
else: 
    flag=False
    print("Enter positive number", end=" ")

if flag==True:

    print(f"{num} is prime")

else :

    print(f"{num} is not prime")