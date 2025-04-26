from BankAccount import BankAccount # type: ignore

class Bank:
    
    #Provides functionality for account creation, deposits, withdrawals,
    # balance inquiries, and account searching.
    
    # Create new bank object (constructor)
    def __init__(self, name="My Bank"):
        self.name = name
        self.accounts = {}  # Maps account_ids to BankAccount objects
        
    # Create some example accounts
        exampleAccOne = BankAccount("cb442244", "Carter", "Boatman", 5000)
        exampleAccTwo = BankAccount("df394750", "Dennis", "Feldbruegge", 15000)
        exampleAccThree = BankAccount("mr395760", "Mary", "Reinke", 10000)
        exampleAccFour = BankAccount("bb946532", "Billy", "Bob", 1)
        exampleAccFive = BankAccount("js132487", "Jane", "Schmidt", 5000)
        
        # Add them to our accounts dictionary
        self.accounts = {
            "cb442244": exampleAccOne,
            "df394750": exampleAccTwo,
            "mr395760": exampleAccThree,
            "bb946532": exampleAccFour,
            "js132487": exampleAccFive,
        }
    
    def create_account(self):
        firstName = input("Please enter your first name: ")
        lastName  = input("Please enter your last name: ")    
        userId = BankAccount.generate_account_id(firstName, lastName) # Uses random number generation to create an Id
        
        print("user id is: " + userId) #DO WE STILL NEED TO PRINT THIS HERE?
        
        initBalance = input("Please enter the initial balance of the account (in dollars): ")
        newAccount = BankAccount(userId, firstName, lastName, initBalance) # Account object created 
        return newAccount
    
    #Search for account by account ID. Returns that BankAccount object
    def get_account(self, account_id):
     
        if account_id not in self.accounts:
            raise Exception(f"Account with ID {account_id} not found")
        
        return self.accounts[account_id]


    # Function to deposit. 
    # Command is given to our Bank object, 
    # which then calls the apporpriate command on the specified BankAccount object.
    def deposit_in_account(self, account_id, amount):

        account = self.get_account(account_id)
        account.deposit(amount) #actual deposit handled by deposit function in BankAccount
        return account
    
    #Same logic as deposit. Just using withdraw.
    def withdraw_from_account(self, account_id, amount):

        account = self.get_account(account_id)
        account.withdraw(amount)
        return account
    
    def add_account(self, new_account_id, new_account):
        if new_account_id not in self.accounts:
            self.accounts[new_account_id] = new_account
        else:
            raise Exception("Account already exists")
        return new_account

    def account_balance(self, account_id):

        account = self.get_account(account_id)
        return account.balance
    
    #This returns a list of our accounts. Not formatted at all.
    def list_accounts(self):
  
        return list(self.accounts.values())

    ###############################################################################
    # this method returns an account_id that corresponds to a first and last name #
    ###############################################################################
    def get_account_id(self, first_name, last_name):
        if len(self.accounts) < 0:
            raise Exception("No accounts")
        else:
            for account in self.accounts:
                if self.accounts[account].get_first_name() == first_name and self.accounts[account].get_last_name() == last_name:
                    return self.accounts[account].get_id()
    

def main():
    pass
    #RUN ALL OF CARTERS MENU OPTIONS

if __name__ == "__main__":
    main()
