# TODO incorporate a fuzzy matches

class card():
    file_name: str
    name: str
    number: int
    play_set: str
    is_foil: bool
    
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
            self.play_set=args[1]
        if size>=3:
            if '/' in args[2]:
                self.is_foil=False
                self.number=args[2].split('/')[0]
            else:
                self.is_foil=True
                self.number=args[2]
        

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
    
    def __str__(self):
        return f'{self.name}, {self.play_set}, {self.number}'

    def __hash__(self):
        # TODO hash on name and ctype
        #return hash((self.name, self.play_set, self.number))
        return hash((self.play_set, self.number))
    
    def __eq__(self, other):
        if not isinstance(other, card):
            return NotImplemented
        return other.__str__() == self.__str__()