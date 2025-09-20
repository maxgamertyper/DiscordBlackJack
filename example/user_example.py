from blackjack import DiscordBlackjack

session = DiscordBlackjack("discord_user_id")
"""
has the possibility to raise an exception if:
The user has not played the game before
It fails to get balances
Or anything else occurs, itll be broad
"""

session.get_balance() # returns 100

"""
with the remove, debit, or set_balance functions, if the value results in a negative balance, it will not be run (this is internal and not made by me)
"""

session.give(100) # just a wrapper for self.credit (user now at 200)
session.remove(10) # just a wrapper for debit (user now at 190)
session.credit(50) # gives the user money (user now at 240)
session.debit(140) # removes money from the user (user now at 100)
session.get_balance() # returns the balance of the user (returns 100)
session.set_balance(0) # sets the balance of the user (sets the user balance to 0, will return to 100 because of the short money bonus)
