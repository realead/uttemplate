import unittest
import uttemplate

 
 
class FindUnusedNameTester(unittest.TestCase):  
    def test_find_in_empty(self):
        self.assertEquals(uttemplate.find_unused_name("name", {}), "name")
        
    def test_find_if_not_yet_in_the_set(self):
        self.assertEquals(uttemplate.find_unused_name("name", ["name_", "name ", "nname"]), "name")
        
    def test_find_1(self):
        self.assertEquals(uttemplate.find_unused_name("name", ["name"]), "name1")
        
    def test_find_2(self):
        self.assertEquals(uttemplate.find_unused_name("name", ["name", "name1"]), "name2")
        
    def test_find_3(self):
        self.assertEquals(uttemplate.find_unused_name("name", ["name", "name1", "name2", "name33", "name4"]), "name3")

