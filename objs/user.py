import Item

class User:
    def __init__(self, user_id: int, starting_credit: int = 1000, starting_crocoins: int = 0):
        self.user_id: int = user_id
        self.social_credit: int = starting_credit
        self.crocoins: int = starting_crocoins 
        self.items: dict = {}
        self.pockmons: dict = {}
        return

    def get_social_credit(self) -> int:
        return self.social_credit
    def set_social_credit(self, amount: int):
        self.social_credit = amount
        return
    
    def get_crocoins(self) -> int:
        return self.crocoins
    def set_crocoins(self, amount):
        self.crocoins = amount
        return
    
    def get_items(self) -> dict:
        return self.items

    def add_item(self, item: Item):
        if item not in self.items:
            self.items[item.name] = [item, 0]
        self.items[item.name][1] += 1
        return

    async def use_item(self, item: Item) -> int:
        if item not in self.items:
            return -1
        await item.Use()

        return 0

    
    def get_pockmons(self) -> dict:
        return self.pockmons

    pass

    

