class InMemoryDB:
    def __init__(self):
        self.data = {}
        self.transaction_in_progress = False
        self.transaction_data = {}

    def begin_transaction(self):
        if self.transaction_in_progress:
            raise Exception("Transaction already in progress")
        self.transaction_in_progress = True
        self.transaction_data = self.data.copy()

    def put(self, key, value):
        try:
            if not self.transaction_in_progress:
                raise Exception("No transaction in progress")
            if type(key) != str or type(value) != int:
                raise Exception("Invalid key or value")
            if key not in self.transaction_data:
                self.transaction_data[key] = 0
            self.transaction_data[key] = value
        except Exception as e:
            print("Error:", e)

    def get(self, key):
        if key in self.data:
            return self.data[key]
        return self.data.get(key, None)

    def commit(self):
        try:
            if not self.transaction_in_progress:
                raise Exception("No transaction in progress")
            self.data.update(self.transaction_data)
            self.transaction_data = {}
            self.transaction_in_progress = False
        except Exception as e:
            print("Error:", e)

    def rollback(self):
        try:
            if not self.transaction_in_progress:
                raise Exception("No transaction in progress")
            self.transaction_data = {}
            self.transaction_in_progress = False
        except Exception as e:
            print("Error:", e)

# Example usage
db = InMemoryDB()

# should return null, because A doesn’t exist in the DB yet
print("Expected null, got: ", db.get("A"))

# should throw an error because a transaction is not in progress
print("Expected error, got: ", end=" ")
db.put("A", 5)

# starts a new transaction
db.begin_transaction()

# set’s value of A to 5, but its not committed yet
db.put("A", 5)

# should return null, because updates to A are not committed yet
print("Expected null, got", db.get("A"))

# update A’s value to 6 within the transaction
db.put("A", 6)

# commits the open transaction
db.commit()

# should return 6, that was the last value of A to be committed
print("Expected 6, got", db.get("A"))

# throws an error, because there is no open transaction
print("Expected error, got: ", end=" ")
db.commit()

# throws an error because there is no ongoing transaction
print("Expected error, got: ", end=" ")
db.rollback()

# should return null because B does not exist in the database
print("Expected null, got", db.get("B"))

# starts a new transaction
db.begin_transaction()

# Set key B’s value to 10 within the transaction
db.put("B", 10)

# Rollback the transaction - revert any changes made to B
db.rollback()

# Should return null because changes to B were rolled back
print("Expected null, got", db.get("B"))