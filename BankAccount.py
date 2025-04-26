from decimal import Decimal
from datetime import datetime
import random
from typing import Union, Any

# Simple error for when there's not enough money
class InsufficientFundsError(Exception):
    pass

class BankAccount:
    def __init__(self, account_id, first_name, last_name, initial_balance: Union[int, float, str, Decimal] = 0) -> None:
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.balance = Decimal(str(initial_balance))
        self.created_at = datetime.now()

    @property
    # Returns full name of the account holder.
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    # Generate an account ID with the format: first_initial + last_initial + 6 digits
    def generate_account_id(cls, first_name, last_name):
    
        if not first_name or not last_name:
            raise ValueError("First name and last name are required")
        
        # Get the first letter of first and last name
        first_initial = first_name[0].lower()
        last_initial = last_name[0].lower()
        
        # Generate 6 random digits
        digits = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Combine to create the account ID
        return f"{first_initial}{last_initial}{digits}"

    def deposit(self, amount):
        try:

            if not isinstance(amount, Decimal): # Converts amount to Decimal if it isn't already
                amount = Decimal(str(amount))
            if amount <= 0: #or amount.isnumeric() == False
                raise ValueError("Deposit amount must be a positive number greater than zero")
            
            self.balance += amount
            print("$" + str(amount) + " successfully deposited into your account\nCurrent balance: $" + str(self.get_balance()))
        except:
            print("ERROR: The deposit amount must be a positive number and greater than zero")
        return self

    def withdraw(self, amount):
        try:

            if not isinstance(amount, Decimal): # Converts amount to Decimal if it isn't already
                amount = Decimal(str(amount))
            if amount <= 0:
                raise ValueError("ERROR: The withdraw amount must be a positive number and more than zero.")
            if amount > self.balance:
                raise InsufficientFundsError(f"Not enough funds to withdraw ${amount}. Your current balance is ${self.balance}")
            
            self.balance -= amount
            print("$" + str(amount) + " successfully withdrawn from your account\nCurrent balance: $" + str(self.get_balance()))
        
        except (ValueError, TypeError):
            print("ERROR: The deposit amount must be a positive number and more than zero.")
        except InsufficientFundsError:
            print(f"Not enough funds to withdraw ${amount}, your current balance is ${self.balance}")
        return self

    def get_balance(self):
        return self.balance
    
    #######################
    # Getters and Setters #
    #######################

    '''
    TO DO:
    - Finish all setters and getters (assignment requirement)
    '''
    
    # Returns userID
    def get_id(self):
        return self.account_id
    
    # Returns firstName
    def get_first_name(self):
        return self.first_name
    
    # Returns lastName
    def get_last_name(self):
        return self.last_name