year=int(input("Enter the number :"))

if (year % 400 ==0 ) and (year % 100==0):

    print(f" {year} is leap year")

elif (year % 4==0) and (year % 100 !=0):

    print(f'{year} is a leapp year')

else  :

    print(f"{year} is not a leap year")