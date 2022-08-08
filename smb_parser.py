from lark import Lark, Transformer
from itertools import product

class SMBTransformer(Transformer):
    meet_dict: dict

    def __init__(self, meet_dict):
        super().__init__()
        self.meet_dict = meet_dict

    def num(self, n):
        (n,) = n
        return n

    def name(self, name):
        (name,) = name
        return name

    def assign_var(self, value):
        return value

    def meet(self, values):
        a, b = values
        if f"({a},{b})" in self.meet_dict.keys():
            return self.meet_dict[f"({a},{b})"]
        else:
            return a, b

    def d(self, values):
        a, b, c = values
        if a == b and b == c:
            return c
        return a, b, c


class SMBParser:
    smb_grammar = """
                    ?start: inf
                        | start "=" inf     -> assign_var
                        | "d(" inf "," inf "," inf ")"      -> d
                    ?inf: atom
                        | inf "+" atom      -> meet
                    ?atom: NAME         -> name 
                        | DIGIT         -> num
                        | "(" inf ")" 
            
            
                    %import common.CNAME -> NAME
                    %import common.WS
                    %import common.DIGIT
            
                    %ignore WS
                    """
    meet = {}
    transformer = SMBTransformer(meet)
    parser = Lark(smb_grammar, start="start", parser="lalr", transformer=transformer)

    def add_meet(self, str):
        if "," in str:
            left, right = str.split(",")
            self.meet[f"({left},{right})"] = right
            self.meet[f"({right},{left})"] = left
        else:
            left, right = str.split("=")
            l1, l2 = left.split("+")
            self.meet[f"({l1},{l2})"] = right

    def parse(self, str):
        tree = self.parser.parse(str)
        return tree

    def nice(self, arr, depth=2):
        """If depth = 0 then there is "=", if there is not "=" depth = 1"""
        if depth == 0:
            return f"{self.nice(arr[0], depth=1)} = {self.nice(arr[1], depth=1)}"
        if len(arr) == 2:
            if depth == 1:
                return f"{self.nice(arr[0])}+{self.nice(arr[1])}"
            return f"({self.nice(arr[0])}+{self.nice(arr[1])})"
        elif len(arr) == 3:
            return f"d({self.nice(arr[0])},{self.nice(arr[1])},{self.nice(arr[2])})"
        elif len(arr) == 1:
            return arr[0]
        else:
            return ""

    def parse_nice(self, str):
        if "=" in str:
            return self.nice(self.parse(str), depth=0)
        else:
            return self.nice(self.parse(str), depth=1)


    def add_identity(self, id: [str], alphebet):
        id_set = list(set(id).difference(("+", "(", ")", "=", " ")))
        pr = list(product(alphebet, repeat=len(id_set)))
        temp = id
        print(pr)
        for p in pr:
            for i in range(len(id_set)):
                temp = temp.replace(id_set[i], p[i])
                print(temp)
            self.add_meet(temp)
            temp = id
        print(self.meet)


def main():
    s = input("add rule, if not write 0 (a,b is a~b, a+b=c is usual \n\t")
    parserr = SMBParser()
    parserr.add_identity("1+2=3", ["x","y","z"])


if __name__ == "__main__":
    main()
