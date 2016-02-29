H = 3
W = 5
l = [[] for _ in range(H)]
for j in range(H):
    for i in range(W):
        l[j].append(i+1 + W * j)

l[-1][-1]=" "
print(l)





# l = [i + 1 for i in range(4)]
# print(l)

# test = [[i + 1 for i in range(6)] for j in range(3)]
# print(test)
