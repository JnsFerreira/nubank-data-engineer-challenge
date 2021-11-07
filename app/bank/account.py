class BankAccount:
    def __init__(
        self,
        active_card: bool,
        available_limit: int
    ):
        self.active_card = active_card
        self.available_limit = available_limit
        self.transactions = []

    @property
    def active_card(self):
        return self.__active_card

    @active_card.getter
    def active_card(self):
        return self.__active_card

    @active_card.setter
    def active_card(self, value: bool):
        if isinstance(value, bool):
            self.__active_card = value
        else:
            # Expected type 'int', got 'str' instead
            raise ValueError(f"Expected type 'boolean', but got: {type(value)}")

    @property
    def available_limit(self):
        return self.__available_limit

    @available_limit.getter
    def available_limit(self):
        return self.__available_limit

    @available_limit.setter
    def available_limit(self, value):
        if isinstance(value, int):
            self.__available_limit = value
        else:
            raise ValueError(f"Expected integer, but got: {type(value)}")

    @property
    def transactions(self):
        return self.__transactions

    @transactions.getter
    def transactions(self):
        return self.__transactions

    @transactions.setter
    def transactions(self, value: list):
        if isinstance(value, list):
            self.__transactions = value
        else:
            raise ValueError(f"Expected type 'list', but got: {type(value)}")
