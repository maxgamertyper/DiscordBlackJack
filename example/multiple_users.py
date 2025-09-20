from blackjack import DiscordBlackjack

# im not sure if this works, on the spot making

file="userids.txt"

with open(file,"r") as f:
    content=f.read()
    f.close()
users=content.splitlines()

for user in users:
  session = DiscordBlackjack(user)
  session.set_balance(1000)
