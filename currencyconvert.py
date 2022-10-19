import time
import requests


class ConvertCurrency:

    currencyrates = "https://api.exchangerate.host/latest?"

    def __init__(self, gui=False):
        # if using a gui with this class, set gui to true
        self.gui = gui

    def fetch_currencies(self, *args):
        """
        Gets the current list of available currencies from http://exchangerate.host
        Input: *args: str #represents the queries to the API
        Output:
            json: dict
        """
        currencyurl = ConvertCurrency().currencyrates
        if args:
            for value in args:
                currencyurl += value
        currencyfetch = requests.get(currencyurl)
        return currencyfetch.json()

    def currencies_to_list(self):
        """
        Fetches all the known currencies from the API as a JSON and converts it into a list

        Output:
            list: list of all currencies that can be converted
        """
        currencyjson = self.fetch_currencies()
        currencylist = []
        for key in currencyjson["rates"].keys():
            currencylist.append(key)
        return currencylist

    def check_for_currency(self, currencyjson, *args):
        """
        Checks whether the given currencies exist in the given json from the api
        Input: currencyjson: dict,
               *args: str,
               currencyjson being the list of currencies from the api and args being the 3 initials of the desired currency
        Output:
            bool, Boolean represents whether the given currencies exist (returns False if any of the currencies dont exist)
        """
        args = tuple((arg.upper() for arg in args))
        for key in currencyjson["rates"].keys():
            for currency in args:
                if key == currency:
                    print(f'found exchange rate for currency "{key}"')
                    time.sleep(0.5)
                    return True

                if key == list(currencyjson["rates"])[-1] and currency != key:
                    print("couldn't find your currency on the list. exiting...")
                    return False

    def get_currency(
        self, currentcurrency=None, currentbalance=None, newcurrency=None
    ):
        """
        Fetches inputted currencies and returns the exchange rate of one currency for each given.
        Input:
            currentcurrency: str
            currentbalance: str/float
            newcurrency: str
            *all are applicable when parameter "gui" is true, otherwise not necessary
        Output:
            Balance of Original Currency: float
            Currency Name: str
            Balance of New Currency: float
            New Currency Name: str
        Errors:
            ValueError: Invalid Currency
            SyntaxError: Conversion Error with Invalid Input
        """
        # TODO create different handle for incorrect input of currency, e.g., input of USA instead of USD (fuzzy search)
        if self.gui is False:
            if currentcurrency is None:
                currentcurrency = input(
                    "what currency would you like to convert? (first three initials) "
                ).upper()  # doesnt matter whether it's uppercase or not, for convenience
            if currentbalance is None:
                convertto = input(
                    f"what currency do you want your {currentcurrency} converted to? (first three initials) "
                ).upper()
            if newcurrency is None:
                currentbalance = float(
                    input(
                        f'how much of your "{currentcurrency}" would you like to convert into "{convertto}"? (format: 000.00) '
                    )
                )

        currentcurrency = currentcurrency.upper() or currentcurrency
        convertto = newcurrency.upper() or convertto
        currencyjson = self.fetch_currencies()

        if self.check_for_currency(currencyjson, currentcurrency) is True:
            currencyjson = self.fetch_currencies(f"base={currentcurrency}")
        else:
            raise ValueError("Currency doesn't exist.")

        converted = (
            float(currentbalance) * currencyjson["rates"][f"{convertto.upper()}"]
        )
        try:
            if self.gui is False:
                print(
                    f'your ${currentbalance:.2f} in "{currentcurrency}" is ${converted:.2f} in "{convertto}".'
                )
        except ValueError:
            print(
                f"Invalid input for parameter 'currentbalance'\nReason: Type '{type(currentbalance)}' was inputted instead of '<class 'int'>'"
            )
            return None
        try:
            converted = int(str(converted))
        except ValueError:
            pass
        finally:
            return (currentbalance, currentcurrency, converted, convertto)

# instance1 = ConvertCurrency(gui=True)
# print(instance1.get_currency(currentcurrency="USD", currentbalance=20.00, newcurrency="gbp"))
