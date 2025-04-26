# here is the test file I am running in case any of you guys want to use it/check it out

###############################################################################################
# specification test.py is the file I needed to use for testing all of our DSL with unittest  #
# CSC 330 4/26/2025                                                                           #
# this is my own work.                                                                        #
###############################################################################################

from token import NUMBER
from lexer import *
from parser import Parser
from BankAccount import *
from Interpreter import *
import unittest
                        #********************************************
                        #*        specification tests               *
                        #********************************************

class specification_test(unittest.TestCase):
    #implement this below
    #I had to set up the tests to use them
    def setUp(self):
        #creating my own bank and interpreter
        self.bank = Bank()
        self.interpreter = Interpreter(self.bank)
        
        
    #method to print all accounts
    def print_all_accounts(self):
        for account in self.Bank.accounts:
            bank_account = self.Bank.accounts[account]
            print(f"accountId:  {bank_account.get_id()} {bank_account.get_first_name()} {bank_account.get_last_name()} {bank_account.get_balance()}")
        print("\n")



    def run_test(self, text):

        #this try/except is mostly for if they give us bad input
        try:
            #lexes, tokenizes and parses before visiting with the interpreter, print statements print out found tokens for debugging
            lexer = Lexer(text)
            tokens = lexer.tokenize()
            #print('tokens are: ')
            #print(tokens)
            parser = Parser(tokens)
            program = parser.parse()
            #print(program)
            #output is the response from the interpreter
            self.Bank = self.interpreter.visit(program)

            #I want to skip none outputs because they are visits that move to another node
            return self.Bank
        
        except Exception as error:
            print("An error occurred " + repr(error))

    def test_check_balance(self):
        #I create an account id
        account_id = "js132487"
        account = self.bank.accounts[account_id]

        #this is the balance returned by the interpreter
        expected_balance = self.run_test(f"CHECK BALANCE ACCOUNT {account_id}\n")

        print(f"""
            CHECK BALANCE test, if the balance returned by the interpreter *{expected_balance}*
            is the same as the actual balance *{account.get_balance()}* Then the test passes.
        """)

        if expected_balance == account.get_balance():
            print("CHECK BALANCE passed")
        else:
            print("CHECK BALANCE failed")
        #assertEqual is the unittest that tests my checked balance and actual balance
        self.assertEqual(expected_balance, account.get_balance())
        print("----------------------------------------------------------------------\n")

    def test_withdraw(self):
        #I store the bank account and initial balance in account
        bank_account     = self.bank.accounts['cb442244']
        initial_balance  = bank_account.get_balance()
        #here I calculate the expected balance
        expected_balance = initial_balance - 200

        #here is where I use my DSL language
        self.run_test("WITHDRAW 200 ACCOUNT cb442244")
        #here is the actual final balance from the bank account
        final_balance = bank_account.get_balance()

        print(f"""
            WITHDRAW test, the initial bank balance is for account cb442244 is: *{initial_balance}*.
            We are withdrawing *200*.
            the balance after the withdrawal is expected to be *{expected_balance}*.
            if this matches the bank's final balance the test passes. The final balance is *{final_balance}*.
        """)        
        
        #if the expected balance matches the actual balance it passes the test
        if expected_balance == final_balance:
            print("WITHDRAW passed")
        else:
            print("WITHDRAW failed")
        #python unittest to see if the expected value is the actual value after the deposit
        self.assertEqual(expected_balance, final_balance)
        print("----------------------------------------------------------------------\n")

    def test_deposit(self):
        account_id       = 'bb946532'
        deposit_amount   = 500
        #storing the bank account and initial balance
        bank_account     = self.bank.accounts[account_id]
        initial_balance  = bank_account.get_balance()
        #calculating the expected balance
        expected_balance = initial_balance + deposit_amount

        #depositing into my bank account using the DSL
        self.run_test(f"DEPOSIT {deposit_amount} ACCOUNT {account_id}")
        #getting the actual final balance
        final_balance = bank_account.get_balance()

        print(f"""
            DEPOSIT test, the initial bank balance is for account {account_id} is: *{initial_balance}*.
            We are depositing *{deposit_amount}*.
            the balance after the withdrawal is expected to be *{expected_balance}*.
            if this matches the bank's final balance the test passes. The final balance is *{final_balance}*.
        """)

        #if the expected balance matches the actual balance we pass
        if expected_balance == bank_account.get_balance():
            print("DEPOSIT passed")
        else:
            print("DEPOSIT failed")
        #assertEqual is the unittest that tests my expected balance and actual balance
        self.assertEqual(expected_balance, bank_account.get_balance())
        print("----------------------------------------------------------------------\n")
    
    def test_create_account(self):
        first_name = "Casey"
        last_name  = "Jones"
        initial_balance = 400.00
        #here I am running my DSL to test if create account works
        self.run_test(f"NEW ACCOUNT {first_name} {last_name} {initial_balance}")
        #here I have to ascertain the account's id since it is made separately
        account_id = self.bank.get_account_id(first_name, last_name)

        print(f"""
            CREATE ACCOUNT test, we are creating an account for *{first_name} {last_name}*.
            the initial balance is: *{initial_balance}*.
            if unittest finds the account id *{account_id}* to be an instance of a bank account, the test passes.
        """)


        #if my account_id is a key in my bank accounts dictionary, it exists and passes the test
        if account_id in self.bank.accounts:
            print("CREATE ACCOUNT passed")
        else:
            print("CREATE ACCOUNT failed")
        
        #here I need to see if the new bank account is an instance of a bank account, this was hard
        #I ended up using type() on an existing account
        self.assertIsInstance(self.bank.accounts[account_id], type(self.bank.accounts['cb442244']))
        print()

    
    
    #test = specification_test(Bank)

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