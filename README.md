# uttemplate

creating unit tests from a template in python2.7+ or python3.

## Introduction

`Boost.Test` offers a functionality which can create same test cases for different types/classes: `BOOST_AUTO_TEST_CASE_TEMPLATE`. 

For example

    typedef boost::mpl::vector<TypeA, TypeB> types_for_test;
    BOOST_AUTO_TEST_CASE_TEMPLATE(test_something, T, types_for_test){
        T obj;
        BOOST_CHECK_EQUAL(obj.empty(), true);
    }

would result in two different test cases, one for `TypeA` and one for `TypeA`. 

This project augments the `unittest` module with a similar functionality.

## Installation

To run it/test it you need a python2.7 (or python3) environment, the easiest way is to use the `virtualenv`:

    virtualenv -p python2.7 p27
    source p27/bin/activate
    (p27)...

To install the module using `pip` run:

    (p27) pip install https://github.com/realead/uttemplate/zipball/master

It is possible to uninstall it afterwards via
   
    (p27) pip uninstall exetest

You can also install using the `setup.py` file from the root directory of the project:

    (p27)  python setup.py install

However, there is no easy way to deinstall it afterwards (only manually) if `setup.py` was used directly.

You could also use the module without installation, by augmenting the python-path via enviroment variable

    export PYTHONPATH="${PYTHONPATH}:<path_to_uttemplate>"

or programmatically, for example with help of

    import sys
    sys.path.append(path_to_uttemplate)



## Usage

There are two ingridients: 

 1. a class method whose name starts with `"template_"` and has signature 
     
     `template_name(self, type_for_test)`
     
 2. the class-decorator `from_templates`
    
For example, we would like to assert, that newly created instances of `list`, `set`and `dict` are empty:

    import unittest
    import uttemplate
    
    @uttemplate.from_templates([list, set, dict])
    class TestBasics(unittest.TestCase):
    
        def template_is_empty(self, type4test):
            self.assertEquals(len(type4test()), 0)
            
Now, run your tests, for example via

    python -m unittest discover -s <your_test_folder>
            
The example translates roughly to

    import unittest

    class TestBasics(unittest.TestCase):
    
        def test_list_is_empty(self):
            self.assertEquals(len(list()), 0)
            
        def test_set_is_empty(self):
            self.assertEquals(len(set()), 0)
            
        def test_dict_is_empty(self):
            self.assertEquals(len(dict()), 0)
            
### Qualifying parameters method-wise

It is possible to define parameters which apply to only one template function (and override the global parameters): 

    ...
    @uttemplate.from_templates([list, set, dict])
    class TestBasics(unittest.TestCase):
        ...
        @uttemplate.for_types([list, dict])
        def template_getitem(self, type4test):
            obj=create_test_obj(type4test)
            self.assertEquals(obj[3], 0)
            
would lead to `getitem` being tested only for `list`and `dict`but not for `set`.


### Other parameter types

It is also possible to provide other type of parameters (not only types) for templates, for example integer values:

    @uttemplate.from_templates([list, set, dict])
    class TestBasics(unittest.TestCase):
        ...
        @uttemplate.for_types([0, 2, 4])
        def template_is_even(self, number):
            self.assertEquals(number % 2, 0)
            
### No default parameters for a class

There is no need to provide default parameter list for the class decorator, if there are only templates with locally provided parameters in the test class:

    @uttemplate.from_templates()
    class TestAllSpecial(unittest.TestCase):
        @uttemplate.for_types([0, "dfadfs", 0.0])
        def template_is_even(self, obj):
                self.assertFalse(obj.__class__ is list)
                


## Future:
 
   1. no '()' for '@uttemplate.from_templates()'
   2. more than one parameter list


                              
             
