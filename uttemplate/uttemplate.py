

import inspect


#finds a name not in dictionary:
#it's your problem if you try to use strange names...
def find_unused_name(name, all_names):
   cand=name
   try_cnt=0
   while cand in all_names:
        try_cnt+=1
        cand=name+str(try_cnt)
   return cand



__TEST_CASE_PREFIX="test_from_"
__TEST_CASE_MIDDLE="_for_"

def mangle_name(name):
    return __TEST_CASE_PREFIX+name+__TEST_CASE_MIDDLE

def tests_from_free_function(fun, target_cls, types):
    for my_type in types:
        method_name=mangle_name(fun.__name__)+my_type.__name__
        method_name=find_unused_name(method_name, target_cls.__dict__) 
        setattr(target_cls, method_name, lambda self, inner_type=my_type: fun(inner_type) if fun.__code__.co_argcount==1 else fun(inner_type, self))#x=self


def tests_from_member(fun, target_cls, types):
    for my_type in types:
        method_name=mangle_name(fun.__name__)+my_type.__name__
        method_name=find_unused_name(method_name, target_cls.__dict__) 
        setattr(target_cls, method_name, lambda x, inner_type=my_type: fun(x, inner_type))#x=self
  
  
  
def tests_from_templates(cls, types):
    for name, m in inspect.getmembers(cls, inspect.ismethod):
        if name.startswith("template_"):
            tests_from_member(m, cls, types)
            
            
#decorators:
def from_nonmember(target_cls,types):
    def decorator(fun, target_cls=target_cls, types=types):
        tests_from_free_function(fun, target_cls, types)
        return fun
    return decorator

def from_templates(types):
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
           
