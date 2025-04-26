# here is the test file I am running in case any of you guys want to use it/check it out

from lexer import *
from parser import Parser
from BankAccount import *
from Interpreter import *

#please god just kill me

#implement this below
Bank = Bank()


#thinking about making a global interpreter instance so I don't have to pass it as a parameter every time, this can be changed
interpreter = Interpreter(Bank)

def run_test(text):

    #this try/except is mostly for if they give us bad input
    try:
        #lexes, tokenizes and parses before visiting with the interpreter, print statements print out found tokens for debugging
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        #print('tokens are: ')
        #print(tokens)
        parser = Parser(tokens)
        program = parser.parse()
        print(program)
        #output is the response from the interpreter
        Bank = interpreter.visit(program)

        #I want to skip none outputs because they are visits that move to another node
        
    except Exception as error:
        print("An error occurred " + repr(error))

if __name__ == "__main__":
    
    
    

    run_test("WITHDRAW 200 ACCOUNT cb442244")
    run_test("DEPOSIT 200 ACCOUNT cb442244")
    run_test("CHECK BALANCE ACCOUNT cb442244")
    run_test("NEW ACCOUNT Giorno Giovanna 500.00")
    run_test("CHECK BALANCE ACCOUNT cd234234",)
    run_test("NEW ACCOUNT Carl Pibb 400.00",)
    for account_id, account in Bank.accounts.items():
        print(f"accountId: {account.getId()} {account.getFirstName()} {account.getLastName()} {account.get_balance()}")


# name test.py or demo.py unittest
# unit test
# prints out intermediary outputs

#test.py gets run it shows a menu with three choices
# output without intermediaries canned input and output - noninteractive demo lexer/parser process
# unit test
        