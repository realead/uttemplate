

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
        setattr(target_cls, method_name, lambda x, inner_type=my_type: fun(inner_type))#x=self


    
