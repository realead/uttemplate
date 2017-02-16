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
    def test_as_decorator(self):
        class A:
            pass  
            
        clses=[list, set, dict]
        @uttemplate.from_nonmember(A, clses)           
        def print_name(class_type):
                return class_type.__name__
          
        #function ok?       
        self.assertEqual(print_name(list), "list")
        
        magled=uttemplate.mangle_name("print_name")    
        a=A()
        for cls in clses:
            fun_name=magled+cls.__name__
            self.assertTrue(magled+cls.__name__ in A.__dict__)#the fun is here
            fun =  getattr(a, fun_name, None)
            self.assertEquals(fun(), cls.__name__)#it does the right thing
            
            
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
                     
        def fun(class_type):
                return class_type.__name__
                
        clses=[list]                           
        uttemplate.tests_from_free_function(fun, A, clses)
        
        a=A()
        self.assertTrue("test_from_fun_for_list" in A.__dict__)#old
        self.assertEquals(a.test_from_fun_for_list(), 55)
        self.assertTrue("test_from_fun_for_list1" in A.__dict__)#new
        self.assertEquals(a.test_from_fun_for_list1(), "list")
        
       
        
class TestFromMember(unittest.TestCase):
    #not (yet) possible
    #def test_as_decorator(self):

    def test_add_normal(self):
        class A:
            def print_name(self, class_type):
                return class_type.__name__
                
        clses=[list, set, dict]                           
        uttemplate.tests_from_member(A.print_name, A, clses)
        
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
            def fun(self, class_type):
                return class_type.__name__
                
        clses=[list]                           
        uttemplate.tests_from_member(A.fun, A, clses)
        
        a=A()
        self.assertTrue("test_from_fun_for_list" in A.__dict__)#old
        self.assertEquals(a.test_from_fun_for_list(), 55)
        self.assertTrue("test_from_fun_for_list1" in A.__dict__)#new
        self.assertEquals(a.test_from_fun_for_list1(), "list")
        


class TestFromTemplates(unittest.TestCase):
    def test_as_decorator(self):
        clses=[list, set, dict]
        
        @uttemplate.from_templates(clses)
        class A:
            def template_one(self, class_type):
                return class_type.__name__

        magled=uttemplate.mangle_name("template_one")
        
        a=A()
        for cls in clses:
            fun_name=magled+cls.__name__
            self.assertTrue(magled+cls.__name__ in A.__dict__)#the fun is here
            fun =  getattr(a, fun_name, None)
            self.assertEquals(fun(), cls.__name__)#it does the right thing
            
            
    def test_add_normal(self):
        class A:
            def template_one(self, class_type):
                return class_type.__name__
                
        clses=[list, set, dict]                           
        uttemplate.tests_from_templates(A, clses)
        
        magled=uttemplate.mangle_name("template_one")
        
        a=A()
        for cls in clses:
            fun_name=magled+cls.__name__
            self.assertTrue(magled+cls.__name__ in A.__dict__)#the fun is here
            fun =  getattr(a, fun_name, None)
            self.assertEquals(fun(), cls.__name__)#it does the right thing

    def test_add_to_existing(self):
        class A:
            def test_from_template_one_for_list(self):
                return 55
            def template_one(self, class_type):
                return class_type.__name__
                
        clses=[list]                           
        uttemplate.tests_from_templates(A, clses)
        
        a=A()
        self.assertTrue("test_from_template_one_for_list" in A.__dict__)#old
        self.assertEquals(a.test_from_template_one_for_list(), 55)
        self.assertTrue("test_from_template_one_for_list1" in A.__dict__)#new
        self.assertEquals(a.test_from_template_one_for_list1(), "list")   
        
        
    def test_two_templates(self):
        class A:
            def template_one(self, class_type):
                return class_type.__name__
            def template_two(self, class_type):
                return class_type.__name__
                
        clses=[list, dict, set]                           
        uttemplate.tests_from_templates(A, clses)
        
        a=A()
        for my_type in clses:
            for i, base_name in enumerate(["test_from_template_one_for_", "test_from_template_two_for_"]):
                fun_name=base_name+my_type.__name__
                self.assertTrue(fun_name in A.__dict__, msg=fun_name+"  "+str(A.__dict__))#the fun is here
                fun = getattr(a, fun_name, None)
                if i==0: 
                   expected=my_type.__name__
                else:
                   my_type.__name__+my_type.__name__
                self.assertEquals(fun(), expected)#it does the right thing
                             

@uttemplate.from_templates([list, set])
class RunDecoratorTests(unittest.TestCase):
    def template_check_name(self, class_type):
        self.assertTrue(uttemplate.mangle_name("template_check_name")+class_type.__name__ in RunDecoratorTests.__dict__) 
        
    def test_all_functions_here(self):
       clses=[list, set, dict, RunDecoratorTests]
       for cls in clses:
          self.assertTrue(uttemplate.mangle_name("template_check_name")+cls.__name__ in RunDecoratorTests.__dict__)
       


@uttemplate.from_nonmember(RunDecoratorTests, [dict, RunDecoratorTests])
def template_check_name(class_type, self=None):
        self.assertTrue(uttemplate.mangle_name("template_check_name")+class_type.__name__ in RunDecoratorTests.__dict__) 
        
        
@uttemplate.from_templates([list])
class TestForTypesDecorator(unittest.TestCase):

    def test_types_attribute(self):
        @uttemplate.for_types([list, set, dict])
        def fun():
            pass        
        self.assertTrue("uttemplate_types" in fun.__dict__)
        
        self.assertEqual(len(fun.uttemplate_types), 3)
        for clsRec, clsExp in zip(fun.uttemplate_types, [list, set, dict]):
            self.assertTrue(clsRec==clsExp)
     
    @uttemplate.for_types([int, float])   
    def template_one(self, my_type):
         self.assertTrue(my_type!=list)
        
    def template_two(self, my_type):
         self.assertFalse(my_type in [int, float])         
         

## readme examples:

def create_test_obj(type4test):
   if(type4test==list):
        return [0]*5
   else:
        return {3:0}
        
@uttemplate.from_templates([list, set, dict])
class TestBasics(unittest.TestCase):
    def template_are_empty(self, type4test):
        self.assertEquals(len(type4test()), 0) 
        
    @uttemplate.for_types([list, dict])
    def template_getitem(self, type4test):
            obj=create_test_obj(type4test)
            self.assertEquals(obj[3], 0)     
          
    @uttemplate.for_types([0, 2, 4])
    def template_is_even(self, number):
            self.assertEquals(number % 2, 0)          
  
  
@uttemplate.from_templates()
class TestAllSpecial(unittest.TestCase):            
    @uttemplate.for_types([0, "dfadfs", 0.0])
    def template_is_even(self, obj):
            self.assertFalse(obj.__class__ is list)  
            
                 
