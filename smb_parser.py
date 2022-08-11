from itertools import product
from sys import stdout

from lark import Lark, Transformer


class SMBTransformer(Transformer):
    meet_dict: dict

    def __init__(self, meet_dict):
        super().__init__()
        self.meet_dict = meet_dict

    def num(self, n):
        n = n[0].value
        return n

    def name(self, name):
        (name,) = name
        return name

    @staticmethod
    def assign_var(values):
        a, b = values
        return a, b

    def meet(self, values):
        a, b = values
        if a == b:  # idempotent
            return b
        if f"({a},{b})" in self.meet_dict.keys():
            return self.meet_dict[f"({a},{b})"]
        else:
            return a, b

    def d(self, values):
        a, b, c = values
        if a == b and b == c:  # idempotent
            return c
        # malcev
        try:
            if a == b and self.meet_dict[f"({b},{c})"] == c and  self.meet_dict[f"({c},{b})"] == b:
                return c
            if c == b and self.meet_dict[f"({b},{a})"] == a and  self.meet_dict[f"({a},{b})"] == b:
                return a
        finally:
            return a, b, c



class SMBParser:
    smb_grammar = """
                    ?start: 
                        | inf
                        | start "=" inf     -> assign_var
                    ?inf: atom
                        | inf "+" atom -> meet                              
                    ?atom: NAME         -> name 
                        | NUMBER         -> num
                        | "(" inf ")" 
                        | "/(" inf "," inf "," inf ")" -> d
            
            
                    %import common.CNAME -> NAME
                    %import common.WS
                    %import common.NUMBER
            
                    %ignore WS
                    """
    meet = {}
    transformer = SMBTransformer(meet)
    parser = Lark(smb_grammar, start="start", parser="lalr", transformer=transformer)

    def add_meet(self, str):
        try:
            left, right = self.parse(str)
            l1, l2 = left
            self.meet[f"({l1},{l2})"] = right
        except:
            try:
                left, right = str.split(",")
                self.meet[f"({left},{right})"] = right
                self.meet[f"({right},{left})"] = left
            except:
                # print(f"greska sa unosom stringa:\t{str}\n"
                #       f" parsirano:\t\t {self.parse(str)}\n"
                #       f"left:\t {left}, \t\t"
                #       f"right:\t {right}\n"
                #       f"nece biti unesen")
                # print(self.meet)
                # input()
                pass

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
            return f"/({self.nice(arr[0])},{self.nice(arr[1])},{self.nice(arr[2])})"
        elif len(arr) == 1:
            return arr[0]
        else:
            return ""

    def parse_nice(self, str):
        if "=" in str:
            return self.nice(self.parse(str), depth=0)
        else:
            return self.nice(self.parse(str), depth=1)

    def add_identity(self, id: [str], alphabet):
        id_set = set(id).difference(("+", "(", ")", "=", " ", "/", ","))
        # print(id_set)
        if id_set.intersection(set(alphabet)):
            raise Exception("not disjunct")
        id_set = list(id_set)
        pr = list(product(alphabet, repeat=len(id_set)))
        temp = id
        for p in pr:
            for i in range(len(id_set)):
                temp = temp.replace(id_set[i], str(p[i]))
                # print(temp)
            self.add_meet(temp)
            temp = id
        # print(self.meet)

    def calculate(self, id: [str], alphabet, file=stdout):
        id_set = set(id).difference(("+", "(", ")", "=", " ", "/", ","))
        if id_set.intersection(set(alphabet)):
            raise Exception("not disjunct")
        id_set = list(id_set)
        pr = list(product(alphabet, repeat=len(id_set)))
        print(id_set)
        temp = id
        for p in pr:
            for i in range(len(id_set)):
                temp = temp.replace(id_set[i], str(p[i]))
            nice_parse = self.parse_nice(temp).split(" = ")
            if not nice_parse[0] == nice_parse[1]:
                print(p, end="\t\t", file=file)
                print(self.parse_nice(temp), file=file)
            temp = id
        # print(self.meet)
        # input()


def main():
    # s = input("add rule, if not write 0 (a,b is a~b, a+b=c is usual \n\t")
    parserr = SMBParser()
    s = "x,y"
    parserr.add_meet(s)
    print(parserr.meet)
    # parserr.add_identity(s, ["1","2","3","4","5","6"])


if __name__ == "__main__":
    main()
