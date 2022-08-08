from smb_parser import SMBParser

id = "((y+x)+(u+z))+((x+y)+(z+u))=(x+y)+(z+u)"
print("\t" + id)
parser = SMBParser()

parser.add_meet("0+1,1+0")
parser.add_meet("1+2,2+1")
parser.add_meet("0+2,2+0")

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


for i in range(3):
    for j in range(3):
        for k in range(3):
            for l in range(3):
                new = id.replace("x", f"{i}")
                new = new.replace("y", f"{j}")
                new = new.replace("u", f"{k}")
                new = new.replace("z", f"{l}")
                # print(f"(x,y,z,u)->({i},{j},{k},{l})")
                print("> " + parser.parse_nice(new) + " <")
