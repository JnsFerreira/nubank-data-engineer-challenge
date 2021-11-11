class BankAccount:
    """Represents an bank account"""
    def __init__(
        self,
        active_card: bool,
        available_limit: int
    ):
        """
        Constructor method for BankAccount

        Args:
            active_card (bool): Indicates if card whether is active or not
            available_limit (int): Current available limit at account
        """
        self.active_card = active_card
        self.available_limit = available_limit
        self.transactions = []

    @property
    def active_card(self) -> bool:
        """Property for active_card attribute"""
        return self.__active_card

    @active_card.getter
    def active_card(self) -> bool:
        """Getter for active_card attribute"""
        return self.__active_card

    @active_card.setter
    def active_card(self, value: bool) -> None:
        """
        Setter for active_card attribute

        Args:
            value (bool): Value to be set to active_card. Must be a boolean.

        Returns:
            active_card (bool): Indicates if card whether is active or not
        """
        if isinstance(value, bool):
            self.__active_card = value
        else:
            raise TypeError(f"Expected type 'boolean', got: {type(value)} instead")

    @property
    def available_limit(self) -> int:
        """Property for available_limit attribute"""
        return self.__available_limit

    @available_limit.getter
    def available_limit(self) -> int:
        """Getter for available_limit attribute"""
        return self.__available_limit

    @available_limit.setter
    def available_limit(self, value: int) -> None:
        """
        Setter for available_limit attribute

        Args:
            value (int): Value to be set to available_limit. Must be a integer.

        Returns:
            None
        """
        if isinstance(value, int):
            self.__available_limit = value
        else:
            raise TypeError(f"Expected integer, but got: {type(value)}")

    @property
    def transactions(self) -> list:
        """Property for transactions attribute"""
        return self.__transactions

    @transactions.getter
    def transactions(self) -> list:
        """Getter for transactions attribute"""
        return self.__transactions

    @transactions.setter
    def transactions(self, value: list) -> None:
        """
        Setter for transactions attribute
        Args:
            value (list): Value to be set to transactions. Must be a list.

        Returns:
            None
        """
        if isinstance(value, list):
            self.__transactions = value
        else:
            raise TypeError(f"Expected type 'list', got: {type(value)} instead")

    def to_dict(self):
        return {
            "account": {
                "active-card": self.active_card,
                "available-limit": self.available_limit,
            }
        }
