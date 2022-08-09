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

list_of_id = [" ((x + y) + z) + ((z + y) + x) = (z + y) + x",
              " ((x + a) + (y + b)) + ((a + x) + (b + y)) = (a + x) + (b + y)",
              " /(x + a,y+b,z+c)+/(a+x,b+y, c+z) =/(a+x,b+y, c+z)", "   (x + y) + (y + x) = y + x",
              " ((x + y) + z) + (x + (y + z)) = x + (y + z)", " (x + (y + z)) + ((x + y) + z) = (x + y) + z",
              " /(x+y, x+y, y+x) = y+x", " /(y+x, x+y, x+y) = y+x"
              ]


def main():
    parser = SMBParser()
    var_num = 6
    for identity in list_of_id:
        print(identity)
        parser.add_identity(identity, range(6))
    while True:
        s = input("Try identety\n")
        par_s = parser.parse_nice(s)
        print(par_s)


if __name__ == "__main__":
    main()
