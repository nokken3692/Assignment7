from typing import ValuesView
from BankAccount import *
from Bank import *
##################################################################
# Interpreter.py is the interpreter class file for using our DSL #
# Written: 04/23/2025 by group 8                                 #
# Revised: 4/24/25 debugged, 4/25/2025 changed return stmts      #
##################################################################


######################################################################################################################
#                                         interpreter                                                                #
######################################################################################################################

###################################################################################
# created a class for the action (deposit, withdraw)  with node position tracking #
###################################################################################
class Action:
    #initializes action with a value and calls set position
    def __init__(self, value):
        self.value = value
        self.set_pos()
    #here is where it sets position start and end, with a default of none
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end   = pos_end
        return self
    def __repr__(self):
        return str(self.value)

#################################################
# created a class for amount with node tracking #
#################################################
class Amount:
    #initializes it with a value and calls set position
    def __init__(self, value):
        self.value = value
        self.set_pos()
    #creates a position with a default parameter of None
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end   = pos_end
        return self
    def __repr__(self):
        return str(self.value)


class Interpreter:
    #this is the constructor where I initialize an empty account dict if I don't receive any from the main

    #I needed a constructor, so when an instance of interpreter is created, a dictionary is created or received from main
    def __init__(self, bank_instance):
        self.bank = bank_instance

    ###################################################################################
    # the visit method visits each node of the AST and returns the method of the node #
    ###################################################################################
    def visit(self, node):
        #method_name variable is an f-string that concatenates visit_ with the type of node and name.
        method_name = f"visit_{type(node).__name__}"
        #the method is a get attribute of the self, method name
        method = getattr(self, method_name, self.no_visit_method) #provides default instructions if method is not found
        return method(node) #it returns a method function's result of the node.
    
    ########################################################################################################################
    # the no_visit_method takes in itself and the node, it the default method if no method is found to operate on the node #
    ########################################################################################################################
    def no_visit_method(self, node):
        #this raises an exception if we can't find the method to work on the node.
        raise Exception(f"No visit_{type(node).__name__} method defined")
    
    # From my EBNF I can determine that I need nodes for:
        #program
        #transaction (date + action)
        #actions (create_account, check_balance, withdraw, deposit)
        #exit command
        #and literals (amount, account, string, float)
    
    
    ###################################################################
    # this method is called if visit finds an action token in the AST #
    ###################################################################
    def visit_ActionNode(self, node):
        #print("found action node!")
        #this determines what the action is, and visits it based on what type of action it is
        self.visit(node.action).set_pos(node.pos_start, node.pos_end) #set pos sets the position of this specific node in the tree
        
    ##################################################################
    # this method is called if visit finds a number token in the AST #
    ##################################################################
    def visit_AmountNode(self, node):
        #print("found amount node!")
        #if an amount is found, the value is returned and the position of the node is set
        node.value.set_pos(node.pos_start, node.pos_end)
        
    ###############################################
    # this method is for visiting a check_balance #
    ###############################################
    def visit_CheckBalanceNode(self, node):
        #determine the account id
        current_account = node.account_id
        if current_account == None:
            raise Exception("Can't find the node's account id for CheckBalance")
        
        ############################################################################################################
        #uncomment the below if you want to return a bank object, this just didn't make sense to me to do.
        #new_bank = print(self.bank.account_balance(current_account))
        #return new_bank

        #this just returns the actual account balance.
        return self.bank.account_balance(current_account)
        
    ##################################################
    # this method is for traversing account creation #
    ##################################################
    def visit_CreateAccountNode(self, node): 
        #print(f"Creating account for {node.first_name} {node.last_name} ")
        #here is where we determine the account ID based on the user inputted first and last name, and 6 random numbers
        account_id = BankAccount.generate_account_id(node.first_name, node.last_name)
        #here we create the instance of bank account and store it in the accounts dictionary
        new_bank = self.bank.add_account(account_id, BankAccount(account_id, node.first_name, node.last_name, node.initial_balance))
        #returns new bank instance
        return new_bank
        
    ##############################################
    # this method is for visiting a deposit node #
    ##############################################
    def visit_DepositNode(self, node):
        current_account = node.account_id
        if current_account == None:
            raise Exception("Can't find the node's account id")
        #I index the account and call deposit with the node's specified amount

        new_bank = self.bank.deposit_in_account(current_account, node.amount)
        #returns f-string with information about deposit
        return new_bank
            
    ##################################################################
    # this method is called if visit finds a program node in the AST #
    ##################################################################
    def visit_ProgramNode(self, node):
        
        #if its a create statement then visit create bank account
        # stmt is determined by the keyword of what the transaction is, ie DEPOSIT, WITHDRAW CHECK BALANCE
            
        #if it is a transaction then visit the transaction node
        #a for loop to handle multiple transactions
        for stmt in node.statements:
            new_bank = self.visit(stmt)
        return new_bank
            
    ###########################################
    # this method visits the transaction node #
    ###########################################
    def visit_TransactionNode(self, node):
        #if a transaction node is found, the transaction visits the specific transaction
        #print(f"Transaction on {node}")
        #transaction goes to action
        self.visit(node.action)
        
    ###############################################
    # this method is for visiting a withdraw node #
    ###############################################
    def visit_WithdrawNode(self, node):
        #determining the current account through the node's account id
        current_account = node.account_id
        #raises error if the current account id doesn't have value
        if current_account == None:
            raise Exception("Can't find the node's account id")
        #performs withdraw from account method if no exception is raised
        self.bank.withdraw_from_account(node.account_id, node.amount)
        return self.bank
        
        


#https://www.geeksforgeeks.org/how-to-create-an-empty-class-in-python/
#https://beginnersbook.com/2018/03/python-constructors-default-and-parameterized/
#https://www.geeksforgeeks.org/constructors-in-python/
#https://www.youtube.com/watch?v=YYvBy0vqcSw&t=937s