# x=0, y=1, z=2
def meet(x,y):
        if x not in {0,1,2}:
        table = [[0, 1, 4],
                [0, 1, 2],
                [4, 1, 2]]
        return table[x][y]


print(meet(0,2))
