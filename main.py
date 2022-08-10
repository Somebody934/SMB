from smb_parser import SMBParser

# x + x = x
#   d(x, x, x) = x
# ((x + y) + z) + ((z + y) + x) = (z + y) + x
# ((x + a) + (y + b)) + ((a + x) + (b + y)) = (a + x) + (b + y)
# d(x + a,y+b,z+c)+d(a+x,b+y, c+z) =d(a+x,b+y, c+z)
#   (x + y) + (y + x) = y + x
# ((x + y) + z) + (x + (y + z)) = x + (y + z)
# (x + (y + z)) + ((x + y) + z) = (x + y) + z
# d(x+y, x+y, y+x) = y+x
# d(y+x, x+y, x+y) = y+x

list_of_id = ["((x + y) + z) + ((z + y) + x) = (z + y) + x",
              "((x + a) + (y + b)) + ((a + x) + (b + y)) = (a + x) + (b + y)",
              "/(x + a,y+b,z+c)+/(a+x,b+y, c+z) =/(a+x,b+y, c+z)",
              "((x + y) + z) + (x + (y + z)) = x + (y + z)",
              "(x + (y + z)) + ((x + y) + z) = (x + y) + z",
              "/(x+y, x+y, y+x) = y+x",
              "/(y+x, x+y, x+y) = y+x"
              ]


def main():
    parser = SMBParser()
    var_num = 4
    #       0  1  2  3
    mat = [[0, 1, 2, 3],  # 0
           [0, 1, 3, 3],  # 1
           [3, 2, 2, 3],  # 2
           [2, 3, 2, 3]]  # 3
    for i in range(4):
        for j in range(4):
            parser.add_meet(f"{i}+{j}={mat[i][j]}")
    with open("not_id.txt", "w") as file:
        for identity in list_of_id:
            print(identity, file=file)
            print(identity)
            parser.calculate(identity, range(var_num), file)


if __name__ == "__main__":
    main()
