
# lexer.py
# My tokenizer for the banking DSL project

import re

class Token:
    # Token types for our language
    NEW = 'NEW'
    ACCOUNT = 'ACCOUNT'
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'
    CHECK = 'CHECK'
    BALANCE = 'BALANCE'
    
    # Value types
    IDENTIFIER = 'IDENTIFIER'  # account IDs etc
    NUMBER = 'NUMBER'  # money amounts
    STRING = 'STRING'  # names in quotes
    
    # End of file/input marker
    EOF = 'EOF'
    
    def __init__(self, token_type, value=None, pos_start=None, pos_end=None):
        self.type = token_type
        self.value = value
        self.pos_start = pos_start
        self.pos_end   = pos_end
    
    def __repr__(self):
        # String for printing
        if self.value:
            return f"Token({self.type}, {self.value})"
        return f"Token({self.type})"


class Lexer:
    # This breaks input text into tokens
    
    def __init__(self, text):
        self.text = text
        self.pos = 0
        # Start with first character
        self.current_char = self.text[self.pos] if self.text else None

    def error(self):
        # Got an error - show what character caused it
        bad_char = repr(self.current_char) if self.current_char else 'EOF'
        raise Exception(f"Weird character at pos {self.pos}: {bad_char}")

    def advance(self):
        # Go to next character
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None  # at the end
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        # Skip white spaces
        while self.current_char and self.current_char.isspace():
            self.advance()

    def make_number(self):
        # This handles numbers like 100 or 50.75
        result = ''
        got_decimal = False
        
        while self.current_char and (self.current_char.isdigit() or 
                                    (self.current_char == '.' and not got_decimal)):
            if self.current_char == '.':
                got_decimal = True
            result += self.current_char
            self.advance()

        try:
            # Convert to float
            return Token(Token.NUMBER, float(result))
        except ValueError:
            # Should never happen but just in case
            raise Exception(f"Bad number: {result}")

    def make_string(self):
        # Get stuff in quotes like "John"
        self.advance()  # skip "
        result = ''
        
        # Keep going until closing quote
        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()

        # Closing quote is missing
        if not self.current_char:
            raise Exception("Missing closing quote! Fix your input.")

        self.advance()  # skip closing "
        return Token(Token.STRING, result)

    def make_identifier(self):
        # Get words like NEW, ACCOUNT, or account IDs
        result = ''
        
        # Get all letters/numbers/underscores
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        # Our keywords 
        keywords = {
            'NEW': Token.NEW,
            'ACCOUNT': Token.ACCOUNT,
            'DEPOSIT': Token.DEPOSIT,
            'WITHDRAW': Token.WITHDRAW,
            'CHECK': Token.CHECK,
            'BALANCE': Token.BALANCE
        }

        # Check if it's a keyword or just an ID
        token_type = keywords.get(result.upper(), Token.IDENTIFIER)
        return Token(token_type, result)

    def make_tokens(self):
        tokens = []
        
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
                
            # Numbers start with digits
            if self.current_char.isdigit():
                tokens.append(self.make_number())
                continue
                
            # Strings start with "
            if self.current_char == '"':
                tokens.append(self.make_string())
                continue
                
            # Words/IDs start with letters
            if self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.make_identifier())
                continue
                
            # unexpected character
            self.error()
            
        # Add EOF token so parser knows when to stop
        tokens.append(Token(Token.EOF))
        return tokens
    
    def tokenize(self):
        # Main entry point - Makes entire string into tokens.
        return self.make_tokens()