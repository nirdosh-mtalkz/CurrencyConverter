import requests
from datetime import date
from . import mongo
import json
from bson.json_util import dumps

def convert_one(url,date=str(date.today())):
    payload = {}
    headers= {
        "apikey": "xVS82OxCi3LPHFSvNKduOEGUYottHFJT"
        }
    url = f"{url}&date={date}"
    response = requests.request("GET", url, headers=headers, data = payload)
    result  = response.json()
    final_result = {"date":date,
                    "conversion":f"{result['query']['from']} to {result['query']['to']}",
                    "input":f"{result['query']['amount']} {result['query']['from']}",
                    "output":f"{result['result']} {result['query']['to']}",
                    "success":result['success']
                    }
    return final_result


def check_hist(chk):
    res = json.loads(dumps(chk))
    if 'history' in res:
        #print("histort present")
        return True
    else:
        #print("histort absent")
        return False


def create_hist(mob,hist):
    mongo.db.user.update_one({'mob':mob},{'$set':{'history':hist}})

def update_hist(mob,hist):
    mongo.db.user.update_one({'mob':mob},{'$push':{'history':hist}})
    


def sign_up(mob_no):
    mongo.db.user.insert_one({'mob':mob_no})
    
def delete_hist(mob):
    usr = json.loads(dumps(mongo.db.user.find_one({'mob':mob})))
    if check_hist(usr):
        curr_hist_len = len(usr['history'])
        print(curr_hist_len)
        if curr_hist_len >5:
            dlt = curr_hist_len - 5
            for _ in range(dlt):
                mongo.db.user.update_one({'mob':mob},{'$pop': {'history': -1}})
                print("user popped")