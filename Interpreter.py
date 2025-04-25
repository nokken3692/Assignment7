from typing import ValuesView
from BankAccount import *
##################################################################
# Interpreter.py is the interpreter class file for using our DSL #
# Written: 04/23/2025 by group 8                                 #
# Revised: 4/24/25 debugged, 4/25/2025 changed return stmts      #
##################################################################

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
    accounts = {}
    #I needed a constructor, so when an instance of interpreter is created, a dictionary is created or received from main
    def __init__(self, accounts):
        self.accounts = accounts

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
        #print("Check balance visited")
        #self.accounts is the account dictionary, node.accound_id is the account id extracted from the node and check_balance is the check balance method in BankAccount
        #every instance of calling self.accounts[] is indexing an account by the account_id
        current_account = self.accounts[node.account_id]
        if current_account == None:
            return None
        #f-string is returned with information about the account's balance
        return f"Balance is: ${current_account.check_balance()}"
        
    ##################################################
    # this method is for traversing account creation #
    ##################################################
    def visit_CreateAccountNode(self, node): 
        #print(f"Creating account for {node.first_name} {node.last_name} ")
        #here is where we determine the account ID based on the user inputted first and last name, and 6 random numbers
        account_id = BankAccount.generate_account_id(node.first_name, node.last_name)
        if account_id in self.accounts:
            print("Account already exists")
            return None
        #here we create the instance of bank account and store it in the accounts dictionary
        self.accounts[account_id] = BankAccount(account_id, node.first_name, node.last_name, node.initial_balance)
        #f-string is returned that says that the account was created
        return f"Account created for {node.first_name} {node.last_name} "
        
    ##############################################
    # this method is for visiting a deposit node #
    ##############################################
    def visit_DepositNode(self, node):
        current_account = self.accounts[node.account_id]
        if current_account == None:
            print("Account not found")
            return None
        #I index the account and call deposit with the node's specified amount
        self.accounts[node.account_id].deposit(node.amount)
        #returns f-string with information about deposit
        return f"{current_account.first_name} {current_account.last_name} deposited {node.amount}"
            
    ##################################################################
    # this method is called if visit finds a program node in the AST #
    ##################################################################
    def visit_ProgramNode(self, node):
        output_list = [] #I found out I need a list to collect output from visited nodes
        #if its a create statement then visit create bank account
        # stmt is determined by the keyword of what the transaction is, ie DEPOSIT, WITHDRAW CHECK BALANCE
            
        #if it is a transaction then visit the transaction node
        #a for loop to handle multiple transactions
        for stmt in node.statements:
            output = self.visit(stmt)
            if output is not None:
                output_list.append(output)
        return output_list
            
    ###########################################
    # this method visits the transaction node #
    ###########################################
    def visit_TransactionNode(self, node):
        #if a transaction node is found, the transaction visits the specific transaction
        print(f"Transaction on {node.date}")
        #transaction goes to action
        self.visit(node.action)
        
    ###############################################
    # this method is for visiting a withdraw node #
    ###############################################
    def visit_WithdrawNode(self, node):
        current_account = self.accounts[node.account_id]
        if current_account == None:
            print("Account not found")
            return None
        #performs withdraw on the specified account
        current_account.withdraw(node.amount)
        #f-string returned with a display of how much they withdrew
        return f"""{current_account.first_name} {current_account.last_name} withdrew {node.amount}
               they have a remaining balance of {current_account.balance} """
        
        


#https://www.geeksforgeeks.org/how-to-create-an-empty-class-in-python/
#https://beginnersbook.com/2018/03/python-constructors-default-and-parameterized/
#https://www.geeksforgeeks.org/constructors-in-python/
#https://www.youtube.com/watch?v=YYvBy0vqcSw&t=937s