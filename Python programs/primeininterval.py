lower=4
upper=30
prime=[]
for num in range(lower,upper+1):
    flag=True
    for i in range(2,num):

        if num%i==0:
            break

    else:
       prime.append(num)

print("Prime Numbers are :", prime)
# print(prime)