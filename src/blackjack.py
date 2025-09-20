import requests, json

class DiscordBlackjack():
    def __init__(self, user_id):
        self.user_id = user_id
        self.session = requests.Session()
        self.WALLET_ID = None
        self.SESSION_ID = None
        self.CURRENCY_ID = None
        self.CASH = 0
        self.BALANCES=[]

        if self.new_session() == False:
            raise Exception("Failed to create new session")

    
    def new_session(self):
        url = "https://1300612940486934591.discordsays.com/.proxy/lootlocker/game/v2/session/guest"
        payload={"game_key":"dev_cf978e35dde6458386a0fa9f5ad44d27","platform":"guest","player_identifier":f"DCD-{self.user_id}","game_version":"1.0.0.0"}
        response = self.session.post(url, data=json.dumps(payload))

        r = response.json()

        if r.get("success") != True:
            return False
        
        self.SESSION_ID = response.json().get("session_token")
        self.WALLET_ID = response.json().get("wallet_id")

        attempt_balance = self.get_balances()

        if attempt_balance is not True:
            raise Exception(attempt_balance["Error"])

        return True
    
    def get_balances(self):
        url = f"https://1300612940486934591.discordsays.com/.proxy/lootlocker/game/balances/wallet/{self.WALLET_ID}"
        headers={"X-Session-Token": self.SESSION_ID}
        response = self.session.get(url, headers=headers)
        r = response.json()


        self.BALANCES = r.get("balances")

        if response.status_code != 200:
            return {"Error":"Failed to get Balances"}
        
        if r=={'balances': []}:
            return {"Error":"User has not played before or is invalid"}
        

        return True

    def get_balance(self, currency_id="01JS3QZ72ZBAZF8XW923M3TH9H"):
        self.get_balances()
        this_balance = [b for b in self.BALANCES if b.get("currency",{}).get("id") == currency_id][0]
        return int(this_balance.get("amount"))
    
    def credit(self, amount, currency_id="01JS3QZ72ZBAZF8XW923M3TH9H"):
        url = "https://1300612940486934591.discordsays.com/.proxy/lootlocker/game/balances/credit"
        headers={"X-Session-Token": self.SESSION_ID}
        payload={"amount":str(amount),"currency_id":currency_id,"wallet_id":self.WALLET_ID}
        response = self.session.post(url, headers=headers, json=payload)
        return response.json()
    
    def give(self,amount, currency_id="01JS3QZ72ZBAZF8XW923M3TH9H"):
        return self.credit(amount, currency_id)
    
    def debit(self, amount, currency_id="01JS3QZ72ZBAZF8XW923M3TH9H"):
        url = "https://1300612940486934591.discordsays.com/.proxy/lootlocker/game/balances/debit"
        headers={"X-Session-Token": self.SESSION_ID}
        payload={"amount":str(amount),"currency_id":currency_id,"wallet_id":self.WALLET_ID}
        response = self.session.post(url, headers=headers, json=payload)
        return response.json()
    
    def remove(self,amount, currency_id="01JS3QZ72ZBAZF8XW923M3TH9H"):
        return self.debit(amount, currency_id)
    
    def set_balance(self, amount, currency_id="01JS3QZ72ZBAZF8XW923M3TH9H"):
        self.get_balances()
        this_balance = [b for b in self.BALANCES if b.get("currency",{}).get("id") == currency_id][0]

        if not this_balance:
            return False
        
        balance = int(this_balance.get("amount"))

        difference = balance - amount

        if difference > 0:
            self.remove(difference, currency_id)
            return True
        elif difference < 0:
            self.give(abs(difference), currency_id)
            return True
        else:
            return True
