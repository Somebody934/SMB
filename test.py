from lark import Lark, Transformer


class SMBTransformer(Transformer):
    meet_dict: dict

    def __init__(self, meet_dict):
        super().__init__()
        self.meet_dict = meet_dict

    def meet(self, values):
        a, b = values
        if a == b:  # reflexivity
            return b

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
                    ?atom: NAME
                        | INT       -> num
                        | "(" inf ")" 
            
            
                    %import common.CNAME -> NAME
                    %import common.WS
                    %import common.INT
            
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


parserr = SMBParser()


def nice(arr, depth=1):
    if depth == 0:
        return f"{nice(arr[0])}={nice(arr[1])}"
    if len(arr) == 2:
        return f"({nice(arr[0])}+{nice(arr[1])})"
    elif len(arr) == 3:
        return f"d({nice(arr[0])},{nice(arr[1])},{nice(arr[2])})"
    elif len(arr) == 1:
        return arr[0]
    else:
        return ""


def main():
    s = input("add rule, if not write 0 (a,b is a~b, a+b=c is usual \n\t")
    while s != "0":
        parserr.add_meet(s)
        s = input("add rule, if not write 0 (a,b is a~b, a+b=c is usual \n\t")
    print(parserr.meet)
    try:
        s = input('> ')
    except EOFError:
        return -1
    k = parserr.parse(s)
    print(nice(k.children, depth=0))


main()
