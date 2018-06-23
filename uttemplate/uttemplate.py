import inspect
import sys

PYTHON_VERSION = sys.version_info[0]# 2 or 3?


#finds a name not in dictionary:
#checks for name, name1, name2, name3 and so on
def find_unused_name(name, all_names):
   cand=name
   try_cnt=0
   while cand in all_names:
        try_cnt+=1
        cand=name+str(try_cnt)
   return cand


#"test" is a must for unittest, anything else is just for the eye
__TEST_CASE_PREFIX="test_from_"
__TEST_CASE_MIDDLE="_for_"

def mangle_name(name):
    return __TEST_CASE_PREFIX+name+__TEST_CASE_MIDDLE
    
#actually my_type don't have to be a type..    
def get_type_name(my_type):
    if hasattr(my_type, "__name__"):
        return my_type.__name__
    else:
        return str(my_type)


#if self is used in the free function it should have the following signature
#    my_fun(my_type, self)
#there is no much sense to add tests via free template function
def tests_from_free_function(fun, target_cls, types):
    for my_type in types:
        method_name=mangle_name(fun.__name__)+get_type_name(my_type)
        method_name=find_unused_name(method_name, target_cls.__dict__) 
        setattr(target_cls, method_name, lambda self, inner_type=my_type: fun(inner_type) if fun.__code__.co_argcount==1 else fun(inner_type, self))#x=self


#the member function should have signature my_fun(self, my_type)
def tests_from_member(fun, target_cls, types):
    for my_type in types:
        method_name=mangle_name(fun.__name__)+get_type_name(my_type)
        method_name=find_unused_name(method_name, target_cls.__dict__) 
        setattr(target_cls, method_name, lambda x, inner_type=my_type: fun(x, inner_type))#x=self
  
 
__TEMPLATE_PREFIX="template_"  

__MEMBER_FILTER = inspect.ismethod if PYTHON_VERSION == 2 else inspect.isfunction

def tests_from_templates(cls, types):
    for name, m in inspect.getmembers(cls, __MEMBER_FILTER):
        if name.startswith(__TEMPLATE_PREFIX):
            for_types = types if not hasattr(m, "uttemplate_types") else m.uttemplate_types
            tests_from_member(m, cls, for_types)
            
            
#decorators:
def from_nonmember(target_cls,types):
    def decorator(fun, target_cls=target_cls, types=types):
        tests_from_free_function(fun, target_cls, types)
        return fun
    return decorator

def from_templates(types=[]):
    def decorator(cls, types=types):
        tests_from_templates(cls, types)
        return cls
    return decorator

def for_types(types):
    def decorator(fun, types=types):
        fun.uttemplate_types=types
        return fun
    return decorator
    
    
#no decorator from member, because  the class can not be changed before complete    
#def from_member(target_cls, types):
#    def decorator(m, target_cls=target_cls, types=types):
#        tests_from_member(fun, target_cls, types)        
#    return decorator
           
