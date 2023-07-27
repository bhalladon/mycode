import unittest
from Phonebook import Phonebook

class PhonebookTest(unittest.TestCase):
    
    def test_create_phonebook(self):
        phonebook = Phonebook()
        
    def test_lookup_entry_by_name(self):
        phonebook = Phonebook()
        phonebook.add("Bob", "12345")
        self.assertEqual("12345", phonebook.lookup("Bob"))