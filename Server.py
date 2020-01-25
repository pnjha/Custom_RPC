from Interface import Interface as Interface
debug = False

class Server(Interface):

    def __init__(self):
        self.products = {}
        self.products["laptop"] = 2
        self.products["mouse"] = 10
    
    def get_items_list(self):
        print(self.products)
        return self.products

    def buy(self,args):
        if args not in self.products:
            return 0
        print("args: ",args)
        print(self.products)
        if self.products[args] > 0:
            self.products[args] -= 1
            print(self.products)
            return 1
        print(self.products)
        return 0