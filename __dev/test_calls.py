def print():
    return "111"

def print2():

    return "2222"



class Demo():
    def __init(self):
        self.data = 2324
        self.put = 232
        self.p = print

    def __str__(self):
        return self.p() + str(self.data )

class Demo1():
    def __init(self):
        self.data = 12324
        self.put = 1232
        self.p = print

    def __str__(self):
        return self.p() + str(self.data )

if __name__ == '__main__':
    import copy

    Dmo2 = copy.copy(Demo)
    # Dmo2.__class__ = Demo1
    Dmo2().data = 1111
    Dmo2().p = print2

    print (Dmo2() )
