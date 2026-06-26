class Account:
    def __init__(self, account_id, name, email, address):
        self.id = account_id
        self.name = name
        self.email = email
        self.address = address
 
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address
        }
