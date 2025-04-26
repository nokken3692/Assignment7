# parser.py
# Parser for my banking language

from lexer import Token

# Base class
class AST:
    # Parent for all AST nodes
    pass

# Different node types for each command:
class AmountNode(AST):
    # for Amount

    def __init__(self, amount):
        self.amount = amount
    def __repr__(self):
        return f"Amount(amount={self.amount})"
class CreateAccountNode(AST):
    # For NEW ACCOUNT commands
    
    def __init__(self, first_name, last_name, initial_balance):
        self.first_name = first_name
        self.last_name  = last_name
        self.initial_balance = initial_balance
    ###############################################################################################################################################
    def __repr__(self):
        return f"CreateAccount(first_name={self.first_name}, last_name={self.last_name}, balance={self.initial_balance})"


class DepositNode(AST):
    # For DEPOSIT commands
    
    def __init__(self, amount, account_id):
        self.amount = amount
        self.account_id = account_id
    
    def __repr__(self):
        return f"Deposit(amount={self.amount}, account={self.account_id})"


class WithdrawNode(AST):
    # For WITHDRAW commands
    
    def __init__(self, amount, account_id):
        self.amount = amount
        self.account_id = account_id
    
    def __repr__(self):
        return f"Withdraw(amount={self.amount}, account={self.account_id})"


class CheckBalanceNode(AST):
    # For CHECK BALANCE commands
    
    def __init__(self, account_id):
        self.account_id = account_id
    
    def __repr__(self):
        return f"CheckBalance(account={self.account_id})"


class ProgramNode(AST):
    # The root node - contains all commands
    
    def __init__(self, statements):
        self.statements = statements
    
    def __repr__(self):
        return f"Program({self.statements})"


class Parser:
    # Takes tokens and builds a syntax tree
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_idx = 0
        
        # Make sure we have tokens to parse
        if not tokens:
            raise ValueError("Hey! No tokens to parse!")
            
        self.current_token = self.tokens[0]  # Start with first token
    
    def error(self, expected=None):
        # Show syntax errors
        if expected:
            message = f"Syntax error: Expected {expected}, but got {self.current_token}"
        else:
            message = f"Syntax error at token: {self.current_token}"
            
        raise SyntaxError(message)
    
    def match(self, token_type):
        # Check if current token matches what we want
        # This was kind of tricky to figure out!
        
        if not self.current_token:
            return False
            
        match = self.current_token.type == token_type
        if match:
            self.advance()  # Move to next token
            
        return match
        
    def consume(self, token_type, error_message=None):
        # Either consume token or show error
        # Uses match() to do the actual checking
        
        if self.match(token_type):
            return True
            
        # Error, wrong token
        if not error_message:
            error_message = f"Expected {token_type}"
        
        self.error(error_message)
        
    def advance(self):
        # Go to next token
        self.current_token_idx += 1
        
        if self.current_token_idx < len(self.tokens):
            self.current_token = self.tokens[self.current_token_idx]
        else:
            # No more tokens
            self.current_token = None
            
        return self.current_token
    
    def parse_create_account(self):
        # NEW ACCOUNT "First" "Last" 1000.00
        
        # Need the keywords first
        self.consume(Token.NEW, "NEW")
        self.consume(Token.ACCOUNT, "ACCOUNT")
        
        # Get first name
        ##changing this, sorry dennis.
        #if self.current_token and self.current_token.type == Token.STRING:
        if self.current_token and self.current_token.type in [Token.STRING, Token.IDENTIFIER]:
            first_name = self.current_token.value
            self.advance()
        else:
            self.error("first name")
            return None
            
        # Get last name
        if self.current_token and self.current_token.type in [Token.STRING, Token.IDENTIFIER]:
            last_name = self.current_token.value
            self.advance()
        else:
            self.error("last name")
            return None
        

        # Initial money
        if self.current_token and self.current_token.type == Token.NUMBER:
            initial_balance = self.current_token.value
            self.advance()
        else:
            self.error("initial balance")
            return None
            
        # Make the node
        #print(f"first name: {first_name} last name: {last_name} amount: {initial_balance}")
        return CreateAccountNode(first_name, last_name, initial_balance)
    
    def parse_deposit(self):
        # Handle: DEPOSIT 50.00 ACCOUNT "JD123456"
        
        # Get DEPOSIT keyword
        self.consume(Token.DEPOSIT, "DEPOSIT")
        
        # Get amount (number)
        if self.current_token and self.current_token.type == Token.NUMBER:
            amount = self.current_token.value
            self.advance()
        else:
            self.error("amount")
            return None
        
        # Need ACCOUNT keyword
        self.consume(Token.ACCOUNT, "ACCOUNT")
        
        # Get account ID - can be string or ID 
        # (I had to add this special case to handle both)
        if self.current_token and self.current_token.type in (Token.STRING, Token.IDENTIFIER):
            account_id = self.current_token.value
            self.advance()
        else:
            # Show helpful error
            self.error("account ID")
            return None
            
        # Done! Return node
        return DepositNode(amount, account_id)
    
    def parse_withdraw(self):
        # WITHDRAW 25.00 ACCOUNT "JD123456"
        
        # Start with keyword
        self.consume(Token.WITHDRAW, "WITHDRAW")
        
        # How much to take out
        if self.current_token and self.current_token.type == Token.NUMBER:
            amount = self.current_token.value
            self.advance()
        else:
            self.error("amount")
            return None
        
        # Need ACCOUNT keyword
        self.consume(Token.ACCOUNT, "ACCOUNT")
        
        # Which account
        if self.current_token and self.current_token.type in (Token.STRING, Token.IDENTIFIER):
            account_id = self.current_token.value
            self.advance()
        else:
            self.error("account ID")
            return None
            
        # Make the node
        return WithdrawNode(amount, account_id)
    
    def parse_check_balance(self):
        # CHECK BALANCE ACCOUNT "JD123456"
        
        # Get the CHECK and BALANCE parts
        self.consume(Token.CHECK, "CHECK")
        self.consume(Token.BALANCE, "BALANCE")
        
        # Get ACCOUNT part
        self.consume(Token.ACCOUNT, "ACCOUNT")
        
        # Finally the account ID
        if self.current_token and self.current_token.type in (Token.STRING, Token.IDENTIFIER):
            account_id = self.current_token.value
            self.advance()
        else:
            self.error("account ID")
            return None
            

        # Make the node
        return CheckBalanceNode(account_id)
    
    def parse_statement(self):
        # Figure out which command we're dealing with
        
        # Check for tokens left
        if not self.current_token:
            self.error("banking command")
            return None
        
        # Big if-else to route to the right parser
        # Could use a dictionary/function map but this works fine
        if self.current_token.type == Token.NEW:
            return self.parse_create_account()
        elif self.current_token.type == Token.DEPOSIT:
            return self.parse_deposit()
        elif self.current_token.type == Token.WITHDRAW:
            return self.parse_withdraw()
        elif self.current_token.type == Token.CHECK:
            return self.parse_check_balance()
        else:
            # Unknown command found
            token_val = self.current_token.value if hasattr(self.current_token, 'value') else self.current_token.type
            self.error(f"valid command instead of '{token_val}'")
            return None
    
    def parse(self):
        # Main parsing function - entry point
        
        statements = []  # will hold all the command nodes
        
        # Keep going until EOF
        while self.current_token and self.current_token.type != Token.EOF:
            stmt = self.parse_statement()
            if stmt:  # only add if valid
                statements.append(stmt)
        
        # Make the root node
        return ProgramNode(statements)