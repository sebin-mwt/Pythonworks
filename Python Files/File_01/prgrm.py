# f=open("data.txt")

# print(f.read())

# f.close()




# with open("data.txt") as f:

#     # print(f.readline())
#     # print(f.readline())
#     # print(f.readline())

#     print(f.read())



f=open("data.txt","r")

# for line in f:

#     print(line)

# f.close()

names=f.readlines()

for n in names:

    print(n.strip())

