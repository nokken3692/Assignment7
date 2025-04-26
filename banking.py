###############################################
# Session 7 assignment - description          #
# date, name, revision                        #
# I certify that this is all my and my group's#
# work.                                       #
###############################################

# Imports the BankAccount class from its file
from BankAccount import BankAccount # type: ignore

####################################################################
# Account dictionary created and initialized with example accounts #
####################################################################
exampleAccOne = BankAccount("cb442244", "Carter", "Boatman", 5000)
exampleAccTwo = BankAccount("df394750", "Dennis", "Feldbruegge", 15000)
exampleAccThree = BankAccount("mr395760", "Mary", "Reinke", 10000)
exampleAccFour = BankAccount("bb946532", "Billy", "Bob", 1)
exampleAccFive = BankAccount("js132487", "Jane", "Schmidt", 5000)

accountsDict = {
     "cb442244" : exampleAccOne,
     "df394750" : exampleAccTwo,
     "mr395760" : exampleAccThree,
     "bb946532" : exampleAccFour,
     "js132487" : exampleAccFive,
}

############################################################################################################
# The get choice function gets input from the user, prints a question, clears the screen and returns input #
############################################################################################################
def getChoice(question):
    print(question)
    choice = input("Your choice: > ")
    print("\033c") # Clears output
    return choice

##########################################################################
# The Main function for executing most of the input and displaying menus #
##########################################################################
def main():

    running = True
    loggedIn = False
    choice = ""
    
    # This is the main program loop
    while running:
        
        choice = getChoice("""Would you like to:
            (1) Check (existing) account?
            (2) Create a new account?
            (3) exit.
        """)        
        
        match choice:
            case "1": # Choose existing Account
                accountFound = False
                while accountFound == False:
                        # Print list of example IDs
                        print("[Example Account IDs]:")
                        i = 0 # for numbering the list
                        for key in accountsDict:
                            i += 1
                            print("(" + str(i) + "): " + key)

                        # Looks for account based off of inputed Id
                        myId = input("Please enter your ID number: ")
                        try:            
                            currentAccount = accountsDict.get(myId) # Finds account in dictionary using it's Id
                            if currentAccount == None:
                                raise Exception
                            accountFound = True
                            loggedIn = True
                        except:
                            print("ERROR: ID " + myId + " is not accociated with any existing account")
                        break 
                            
            case "2": # Create new Account
                firstName = input("Please enter your first name: ")
                lastName  = input("Please enter your last name: ")    
                userId = BankAccount.generate_account_id(firstName, lastName) # Uses random number generation to create an Id
                print("user id is: " + userId)
                initBalance = input("Please enter the initial balance of the account (in dollars): ")
                currentAccount = BankAccount(userId, firstName, lastName, initBalance) # Account object created
                accountsDict[userId] = currentAccount # New account added to dictionary
                loggedIn = True    
            case "3": # Exit program
                running = False
                print("Exiting program... Goodbye!")
                exit()
            case _:
                print("Invalid input: ")        

        # This is the inner while-loop that executes while a user is logged in:
        while loggedIn:
            choice = getChoice(f"""
               {currentAccount.getFirstName()} {currentAccount.getLastName()}, would you like to:
                   (1) Make a deposit:
                   (2) Make a withdrawal:
                   (3) Check your current balance:
                   (4) Run Specification Tests:
                   (5) Run Demo:
                   (6) Log out of account:
            """)
            
            match choice:
                case "1":
                    print("You have chosen to make a deposit ")
                    depAmount = input("Enter the amount you would like to deposit (in dollars): ")
                    currentAccount.deposit(depAmount)
                case "2":
                    print("You have chosen to make a withdrawal ")
                    wthAmount = input("Enter the amount you would like to withdraw (in dollars): ")
                    currentAccount.withdraw(wthAmount)
                case "3":
                    print("You have chosen to check your balance ")
                    print("Current balance: $" + str(currentAccount.get_balance()))
                case "4":
                    print("You have chosen to run the specification tests ")
                    #Insert test call here
                    pass
                case "5":
                    print("You have chosen to run the demo")
                    # Insert demo call here
                    pass
                case "6":
                    print("You have chosen to log out")
                    print("Logging out...")
                    currentAccount = ""
                    loggedIn = False
                    choice = ""
                case _:
                    print("Invalid input, please try again: ")
            # this ends the log in loop:
                   
if __name__ == "__main__":
    main()