# Aleksandra Ben, 302821
# Marcin Bereznicki, 302822

from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar
import re


class Product:
    def __init__(self, name: str, price: float, *args, **kwargs) -> None:
        self.name = name
        self.price = price

    def __hash__(self):
        return hash((self.name, self.price))
 
    def __eq__(self, other):
        return self.name == other.name and self.price == other.price


class ServerError(Exception):
    def __init__(self, msg="An error occurred with server", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class TooManyProductsFoundError(ServerError):
    def __init__(self, *args, **kwargs):
        super().__init__(msg="Too many products are available", *args, **kwargs)


class Server(ABC):
    n_max_returned_entries = 3

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
    @abstractmethod
    def get_products_as_list(self) -> List[Product]:
        raise NotImplementedError

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        list_of_products = []
        pattern = re.compile('^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters))
        list_from_server = self.get_products_as_list()
        for elem in list_from_server:
            if pattern.match(elem.name) is not None:
                list_of_products.append(elem)
        if len(list_of_products) > self.n_max_returned_entries:
            raise TooManyProductsFoundError
        else:
            return sorted(list_of_products, key=lambda product: product.price)


class ListServer(Server):

    def __init__(self, products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.products = products
        
    def get_products_as_list(self) -> List[Product]:
        return self.products


class MapServer(Server):

    def __init__(self, products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.products = {}
        for elem in products:
            self.products[elem.name] = elem
            
    def get_products_as_list(self) -> List[Product]:
        list_of_products = []
        for elem in self.products:
            list_of_products.append(self.products[elem])
        return list_of_products


ServerType = TypeVar('ServerType', bound=Server)


class Client:

    def __init__(self, server: ServerType, *args, **kwargs) -> None:
        self.server = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            list_of_products = self.server.get_entries(n_letters)
        except TooManyProductsFoundError:
            return None
        sum_of_prices = 0
        if len(list_of_products) < 1:
            return None
        else:
            for elem in list_of_products:
                sum_of_prices += elem.price
            return sum_of_prices
