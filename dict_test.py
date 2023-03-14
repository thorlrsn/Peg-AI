dictall = {}

dictall[0] = { "Move" : [0,2,0,3,0,4]}

dictall[1]= {"Move" : [[0,2,0,3,0,4],[0,3,0,2,0,0]]}
# print(dictall)


# print(len(dictall[3]["Move"]))
# print(len(dictall[3]["Move"]))

# dictall[3]["Move"][]

# for i in range(len(dictall[3]["Move"])):
#     print(dictall[3]["Move"][i])
#     print(i)
temp = {"Move" : [[0,2,0,3,0,4],[0,3,0,2,0,0]]}
# print(dictall[1]["Move"])
# for i in range(len(dictall)):
#     print(dictall[0]["Move"][:])
#     print(temp == dictall[1]["Move"])

print(dictall.values())
print(temp in dictall.values())