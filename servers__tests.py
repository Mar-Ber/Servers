# Aleksandra Ben, 302821
# Marcin Bereznicki, 302822

import unittest
from collections import Counter
 
from servers import ListServer, Product, Client, MapServer
 
server_types = (ListServer, MapServer)
 
 
class ServerTest(unittest.TestCase):
    
    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))
    
    def test_get_entries_returns_sort(self):
        products = [Product('abc1', 12), Product('ABC12', 8), Product('A12', 3), Product('abc123', 15), Product('AbC1234', 7), Product('Abc12', 7), Product('Ac12', 7)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(3)
            self.assertEqual([products[5], products[1], products[3]], entries)
    
    def test_get_entries_returns_default(self):
        products = [Product('abc1', 12), Product('ABC12', 8), Product('A12', 3), Product('abc123', 15), Product('AbC1234', 7), Product('Abc12', 7), Product('Ac12', 7), Product('c12', 2)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries()
            self.assertEqual([products[7], products[2]], entries)
    
    def test_get_entries_returns_empty(self):
        products = [Product('abc1', 12), Product('ABC12', 8), Product('A12', 3), Product('abc123', 15), Product('AbC1234', 7), Product('Abc12', 7), Product('Ac12', 7), Product('c12', 2)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(5)
            self.assertEqual([], entries)
            
    def test_get_entries_returns_error(self):
        products = [Product('abc1', 12), Product('ABC12', 8), Product('A12', 3), Product('abc123', 15), Product('AbC1234', 7), Product('Abc12', 7), Product('Ac12', 7)]
        for server_type in server_types:
            server = server_type(products)
            server.n_max_returned_entries = 2
            with self.assertRaises(Exception):
                server.get_entries(3)

 
class ClientTest(unittest.TestCase):
    
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))
            
    def test_total_price(self):
        products = [Product('abc1', 12), Product('ABC12', 8), Product('A12', 3), Product('abc123', 15), Product('AbC1234', 7), Product('Abc12', 7), Product('Ac12', 7)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(30, client.get_total_price(3))
            
    def test_total_price_empty_list(self):
        products = [Product('abc1', 12), Product('ABC12', 8), Product('A12', 3), Product('abc123', 15), Product('AbC1234', 7), Product('Abc12', 7), Product('Ac12', 7)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(4))
    
    def test_total_price_error(self):
        products = [Product('abc1', 12), Product('ABC12', 8), Product('A12', 3), Product('abc123', 15), Product('AbC1234', 7), Product('Abc12', 7), Product('Ac12', 7)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            server.n_max_returned_entries = 2
            self.assertEqual(None, client.get_total_price(3))
            
            
if __name__ == '__main__':
    unittest.main()

