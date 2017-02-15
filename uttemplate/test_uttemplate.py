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
        
        
class TestFromFreeFunction(unittest.TestCase):
    def test_add_normal(self):
        class A:
            pass         
        def print_name(class_type):
                return class_type.__name__
                
        clses=[list, set, dict]                           
        uttemplate.tests_from_free_function(print_name, A, clses)
        
        magled=uttemplate.mangle_name("print_name")
        
        a=A()
        for cls in clses:
            fun_name=magled+cls.__name__
            self.assertTrue(magled+cls.__name__ in A.__dict__)#the fun is here
            fun =  getattr(a, fun_name, None)
            self.assertEquals(fun(), cls.__name__)#it does the right thing

    def test_add_to_existing(self):
        class A:
            def test_from_fun_for_list(self):
                return 55
            pass         
        def fun(class_type):
                return class_type.__name__
                
        clses=[list]                           
        uttemplate.tests_from_free_function(fun, A, clses)
        
        a=A()
        self.assertTrue("test_from_fun_for_list" in A.__dict__)#old
        self.assertEquals(a.test_from_fun_for_list(), 55)
        self.assertTrue("test_from_fun_for_list1" in A.__dict__)#new
        self.assertEquals(a.test_from_fun_for_list1(), "list")
        
        
        
        

