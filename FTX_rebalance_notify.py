from ccxt.ftx import ftx
from songline import Sendline
import ccxt
import pandas as pd
import json
import time
token = 'put your line token'
messenger = Sendline(token)

############################ Setting #############################################

API_Key = 'put your api key' 
API_secret = 'put your api secret'
Subaccount = 'put your subaccount name'
Pair = "SRM/USD" 
Token_name = "SRM"
Rebalance_value = 1000  ## put your rebalance value ##


############################### เรียกใช้งาน API #############################################
FTX = ccxt.ftx({
    'apiKey' : API_Key ,
    'secret' : API_secret , 
    'headers': {'FTX-SUBACCOUNT': 'put your subaccount name'}, 
    'enableRateLimit': True
})

print(messenger.sendtext('Exchange = ' + str(FTX)))      ## Network checking / Line notify ##

################################# Price of SRM #############################################

SRM_value = json.dumps(FTX.fetch_ticker('SRM/USD'))         ## pair 'SRM/USD'/ u can change to pair what u want ##
Price_SRM = json.loads(SRM_value)
print(messenger.sendtext('SRM = ' + str(Price_SRM['last'])))     ## Line notify ##

############################### Balance #######################################

while True:
    balance = FTX.fetch_balance()

    A = balance['total']['SRM'] * Price_SRM['last']  ## SRM value * Price = net balance ##

######### i set this bot to checking price for rebalance every 30 min ##############

    if A < Rebalance_value:
        amount = Rebalance_value - A
            print(messenger.sendtext('Buy ' + str(amount)))      
            time.sleep(1800)                                    ## 1800 sec./u can change to what u want ## 

    elif A > Rebalance_value:
        amount = A - Rebalance_value
            print(messenger.sendtext('Sell ' + str(amount)))
            time.sleep(1800)
        
else:
        print(messenger.sendtext('Do notihng'))
        time.sleep(1800)
