

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

def tests_from_template_fun(fun, target_cls, types):
    pass
    
