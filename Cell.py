## each cell in puzzle
class Cell:
    def __init__(self,x,y,domain=['w','b'],value='_') :
        self.x=x
        self.y=y
        self.domain = domain
        self.value=value