# TODO incorporate a fuzzy matches

class card():
    file_name: str
    name: str
    ctype: str
    arena: str
    title: str
    
    def __init__(self, args=[]):
        size = len(args)
        print("debug card: ")
        [print(x) for x in args]
        if size==0:
            return
        if size>=1:
            self.name=args[0]
            self.file_name=self.__get_file_name__()
        if size>=2:
            self.ctype=args[1]
        if size>=3:
            self.arena=args[2]
        if size>=4:
            self.stitle=args[3]
        if size>=5:
            self.title=args[4]
        

    def __get_file_name__(self):
        builder=""
        for x in self.name:
            for c in x:
                if c.isspace():
                    builder+='_'
                elif c.isprintable():
                    builder+=c

        print(f"debug card_file_name: {builder}")
        return builder
    
    def to_dict(self):
        return {"name": self.name,
                "type": self.ctype,
                "arena": self.arena,
                "title": self.title}

    def __iter__(self):
        if self.name is not None:
            yield self.name
        if self.ctype is not None:
            yield self.ctype
        if self.arena is not None:
            yield self.arena
        if self.title is not None:
            yield self.title

    def __str__(self):
        res = f'name: {self.name}'
        res += ', '
        res += f'ctype: {self.ctype}'
        res += ', '
        res += f'arena: {self.arena}'

        return res

    def __hash__(self):
        return hash((self.name, self.ctype, self.title))
    
    def __eq__(self, other):
        if not isinstance(card, other):
            return NotImplemented
        return other.__str__() == self.__str__()