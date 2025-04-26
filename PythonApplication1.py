# here is the test file I am running in case any of you guys want to use it/check it out

from token import NUMBER
from lexer import *
from parser import Parser
from BankAccount import *
from Interpreter import *
import specification_tests
from specification_tests import *
import unittest



Bank = Bank()

#this was the only way I could get unittest to work
if __name__ == "__main__":
    unittest.main(module=specification_tests, exit=False)
# name test.py or demo.py unittest
# unit test
# prints out intermediary outputs

#test.py gets run it shows a menu with three choices
# output without intermediaries canned input and output - noninteractive demo lexer/parser process
# unit test
        

#https://www.geeksforgeeks.org/creating-instance-objects-in-python/
#https://stackoverflow.com/questions/2052390/manually-raising-throwing-an-exception-in-python
#https://docs.python.org/3/library/unittest.html
#https://www.w3schools.com/python/ref_func_type.asp