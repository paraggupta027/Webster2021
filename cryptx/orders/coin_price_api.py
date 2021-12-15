from urllib.request import urlopen
  
import json

def get_coin_price(coin_symbol):

    url ="https://min-api.cryptocompare.com/data/price?fsym=" +  coin_symbol  +"&tsyms="+"USD"
    response = urlopen(url)

    # storing the JSON response 
    # from url in data
    data_json = json.loads(response.read())
    
    # print the json response
    print(coin_symbol +": "+str(data_json['USD']))
    return data_json['USD']
