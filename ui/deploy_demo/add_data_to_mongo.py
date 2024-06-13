from PIL import Image, ExifTags
import math
import pandas as pd
from pymongo import MongoClient
import datetime


def connect_to_db():
    # Connect to your MongoDB Atlas cluster
    client = MongoClient("mongodb+srv://sapsuser:3dUEbY0ijMlL81vF@sap-pv.bdcccxg.mongodb.net/?retryWrites=true&w=majority&appName=SAP-PV")
    db = client["SAPPV"]
    # st.session_state.db = db
    return db

db = connect_to_db()

def insert_documents_to_mongodb(collection_name, documents):
    collection = db[collection_name]

    # Insert documents
    result = collection.insert_many(documents)
    print(f"{len(result.inserted_ids)} documents inserted.")
    return result.inserted_ids

def add_stores():
    stores_list2 = [
        {
            "store_id": "s001",
            "store_retailer": "Albertsons",
            "store_name": "Albertsons Store 1",
            "store_address": "18579 Brookhurst St, Fountain Valley, CA 92708",
            "store_location": "33.698886438603004, -117.95484811537004"
        },
        {
            "store_id": "s002",
            "store_retailer": "Albertsons",
            "store_name": "Albertsons Store 2",
            "store_address": "6601 Quail Hill Pkwy, Irvine, CA 92603",
            "store_location": "33.66317496095124, -117.7811268011586"
        },
        {
            "store_id": "s003",
            "store_retailer": "Albertsons",
            "store_name": "Albertsons Store 3",
            "store_address": "4541 Campus Dr, Irvine, CA 92612",
            "store_location": "33.65488777858205, -117.83022195646848"
        },
        {
            "store_id": "s004",
            "store_retailer": "Albertsons",
            "store_name": "Albertsons Store 4",
            "store_address": "14201 Jeffrey Rd, Irvine, CA 92620",
            "store_location": "33.70060021589989, -117.76533395399599"
        },
        {
            "store_id": "s005",
            "store_retailer": "Albertsons",
            "store_name": "Albertsons Store 5",
            "store_address": "24251 Muirlands Blvd, Lake Forest, CA 92630",
            "store_location": "33.63802518542407, -117.70868569786921"
        },
        {
            "store_id": "s006",
            "store_retailer": "Ralphs",
            "store_name": "Ralphs Store 1",
            "store_address": "2555 Eastbluff Dr, Newport Beach, CA 92660",
            "store_location": "33.645620727745595, -117.87511670432097"
        },
        {
            "store_id": "s007",
            "store_retailer": "Ralphs",
            "store_name": "Ralphs Store 2",
            "store_address": "14440 Culver Dr, Irvine, CA 92604",
            "store_location": "33.707440997331894, -117.78722264500874"
        },
        {
            "store_id": "s008",
            "store_retailer": "Costco",
            "store_name": "Costco Store 1",
            "store_address": "2700 Park Ave, Tustin, CA 92782",
            "store_location": "33.70849564777357, -117.82395633725993"
        },
        {
            "store_id": "s009",
            "store_retailer": "Target",
            "store_name": "Target Store 1",
            "store_address": "289 E 17th St, Costa Mesa, CA 92627",
            "store_location": "33.63730197445153, -117.91667107953324"
        },
        {
            "store_id": "s010",
            "store_retailer": "Target",
            "store_name": "Target Store 2",
            "store_address": "26932 La Paz Rd, Aliso Viejo, CA 92656",
            "store_location": "33.57644895243048, -117.70434372855664"
        }
    ]
    stores_list = [
        {
            "store_id": "s011",
            "store_retailer": "UCI",
            "store_name": "ISEB",
            "store_address": "419 Physical Sciences Quad, Irvine, CA 92697",
            "store_location": "33.64313763754278, -117.8439102401954"
        }
    ]
    insert_documents_to_mongodb("stores", stores_list)

def add_products():
    products_list = [
        {
            "product_id": "p001",
            "product_name": "Coca Cola",
            "product_category": "Beverages"
        },
        {
            "product_id": "p002",
            "product_name": "Red Bull",
            "product_category": "Beverages",
        }
    ]    
    # insert_documents_to_mongodb("products", products_list)  

def add_promotions():
    promotions_list2 = [
    {
        "promotion_id":"1001",
        "name":"RED BULL BRAND RB MINI-FRIDGE",
        "type":"FRIDGE",
        "campaign_type":"STORE DISPLAY",
        "campaign_description":"Albertsons - Exclusive Trade Promotion Display Promo",
        "status":[
            "inProcess",
            "released"
        ],
        "period_type":"SELL_IN",
        "start_date":"01-01-2023",
        "end_date":"31-01-2023",
        "tactic_type":"mini fridge with red bull cans",
        "tactic_location":"center of store",
        "tactic_location_type":2,
        "store_id":[
            "s001"
        ],
        "customer_hierarchy_id":"1001",
        "customer_hierarchy_type":"H1",
        "product_types":[
            "cans"
        ],
        "product":"p002"
    },
    {
        "promotion_id":"1002",
        "name":"RED BULL BRAND RB COOLER",
        "type":"FRIDGE",
        "campaign_type":"STORE DISPLAY",
        "campaign_description":"Albertsons - Exclusive Trade Promotion Display Promo",
        "status":[
            "inProcess",
            "released"
        ],
        "period_type":"SELL_IN",
        "start_date":"01-02-2023",
        "end_date":"28-01-2023",
        "tactic_type":"ac style cooler with red bull cans",
        "tactic_location":"center of store",
        "tactic_location_type":2,
        "store_id":[
            "s002"
        ],
        "customer_hierarchy_id":"1001",
        "customer_hierarchy_type":"H1",
        "product_types":[
            "cans"
        ],
        "product":"p002"
    },
    {
        "promotion_id":"1003",
        "name":"RED BULL BRAND RB MINI-FRIDGE",
        "type":"FRIDGE",
        "campaign_type":"STORE DISPLAY",
        "campaign_description":"Costco - Exclusive Trade Promotion Display Promo",
        "status":[
            "inProcess",
            "released"
        ],
        "period_type":"SELL_IN",
        "start_date":"01-03-2023",
        "end_date":"31-01-2023",
        "tactic_type":"mini fridge with red bull cans",
        "tactic_location":"center of store",
        "tactic_location_type":2,
        "store_id":[
            "s008"
        ],
        "customer_hierarchy_id":"1001",
        "customer_hierarchy_type":"H1",
        "product_types":[
            "cans"
        ],
        "product":"p002"
    },
    {
        "promotion_id":"1004",
        "name":"RED BULL BRAND RB CENTER SHELF",
        "type":"SHELF",
        "campaign_type":"STORE DISPLAY",
        "campaign_description":"Albertsons - Exclusive Trade Promotion Display Promo",
        "status":[
            "inProcess",
            "released"
        ],
        "period_type":"SELL_IN",
        "start_date":"01-04-2023",
        "end_date":"30-04-2023",
        "tactic_type":"red bull cans on center shelf",
        "tactic_location":"center of store",
        "tactic_location_type":2,
        "store_id":[
            "s003"
        ],
        "customer_hierarchy_id":"1001",
        "customer_hierarchy_type":"H1",
        "product_types":[
            "cans"
        ],
        "product":"p002"
    },
    {
        "promotion_id":"1004",
        "name":"RED BULL BRAND RB CENTER SHELF",
        "type":"SHELF",
        "campaign_type":"STORE DISPLAY",
        "campaign_description":"Albertsons - Exclusive Trade Promotion Display Promo",
        "status":[
            "inProcess",
            "released"
        ],
        "period_type":"SELL_IN",
        "start_date":"01-05-2023",
        "end_date":"31-05-2023",
        "tactic_type":"red bull cans on center shelf",
        "tactic_location":"center of store",
        "tactic_location_type":2,
        "store_id":[
            "s004"
        ],
        "customer_hierarchy_id":"1001",
        "customer_hierarchy_type":"H1",
        "product_types":[
            "cans"
        ],
        "product":"p002"
    },
    {
        "promotion_id":"1006",
        "name":"RED BULL BRAND RB FRIDGE GAS PUMP",
        "type":"FRIDGE",
        "campaign_type":"STORE DISPLAY",
        "campaign_description":"Ralphs - Exclusive Trade Promotion Display Promo",
        "status":[
            "inProcess",
            "released"
        ],
        "period_type":"SELL_IN",
        "start_date":"01-06-2023",
        "end_date":"30-06-2023",
        "tactic_type":"gas pump mini fridge with red bull cans",
        "tactic_location":"center of store",
        "tactic_location_type":2,
        "store_id":[
            "s006",
            "s007"
        ],
        "customer_hierarchy_id":"1001",
        "customer_hierarchy_type":"H1",
        "product_types":[
            "cans"
        ],
        "product":"p002"
    },
    {
        "promotion_id":"1007",
        "name":"RED BULL BRAND RB TALL-FRIDGE",
        "type":"FRIDGE",
        "campaign_type":"STORE DISPLAY",
        "campaign_description":"Target - Exclusive Trade Promotion Display Promo",
        "status":[
            "inProcess",
            "released"
        ],
        "period_type":"SELL_IN",
        "start_date":"01-07-2023",
        "end_date":"31-07-2023",
        "tactic_type":"tall fridge with red bull cans",
        "tactic_location":"center of store",
        "tactic_location_type":2,
         "store_id":[
            "s009"
        ],
        "customer_hierarchy_id":"1001",
        "customer_hierarchy_type":"H1",
        "product_types":[
            "cans"
        ],
        "product":"p002"
    },
    {
        "promotion_id":"1008",
        "name":"RED BULL BRAND RB MINI-FRIDGE",
        "type":"FRIDGE",
        "campaign_type":"STORE DISPLAY",
        "campaign_description":"Ralphs - Exclusive Trade Promotion Display Promo",
        "status":[
            "inProcess",
            "released"
        ],
        "period_type":"SELL_IN",
        "start_date":"01-08-2023",
        "end_date":"31-08-2023",
        "tactic_type":"mini fridge with red bull cans",
        "tactic_location":"center of store",
        "tactic_location_type":2,
         "store_id":[
            "s007"
        ],
        "customer_hierarchy_id":"1001",
        "customer_hierarchy_type":"H1",
        "product_types":[
            "cans"
        ],
        "product":"p002"
    },
    {
        "promotion_id":"1009",
        "name":"RED BULL BRAND RB MINI-FRIDGE",
        "type":"FRIDGE",
        "campaign_type":"STORE DISPLAY",
        "campaign_description":"Target - Exclusive Trade Promotion Display Promo",
        "status":[
            "inProcess",
            "released"
        ],
        "period_type":"SELL_IN",
        "start_date":"01-09-2023",
        "end_date":"30-09-2023",
        "tactic_type":"mini fridge with red bull cans",
        "tactic_location":"center of store",
        "tactic_location_type":2,
        "store_id":[
            "s010"
        ],  
        "customer_hierarchy_id":"1001",
        "customer_hierarchy_type":"H1",
        "product_types":[
            "cans"
        ],
        "product":"p002"
    },
    {   
        "promotion_id":"1010",
        "name":"COCA COLA BRAND RB MINI-FRIDGE",
        "type":"FRIDGE",
        "campaign_type":"STORE DISPLAY",
        "campaign_description":"Albertsons - Exclusive Trade Promotion Display Promo",
        "status":[
            "inProcess",
            "released"
        ],
        "period_type":"SELL_IN",
        "start_date":"01-10-2023",
        "end_date":"31-10-2023",
        "tactic_type":"mini fridge with coca cola bottles",
        "tactic_location":"center of store",
        "tactic_location_type":2,
        "store_id":[
            "s005"
        ],
        "customer_hierarchy_id":"1001",
        "customer_hierarchy_type":"H1",
        "product_types":[
            "cans"
        ],
        "product":"p001"
    },
    {
        "promotion_id":"1011",
        "name":"COCA COLA BRAND RB CENTER SHELF",
        "type":"SHELF",
        "campaign_type":"STORE DISPLAY",
        "campaign_description":"Target - Exclusive Trade Promotion Display Promo",
        "status":[
            "inProcess",
            "released"
        ],
        "period_type":"SELL_IN",
        "start_date":"01-11-2023",
        "end_date":"30-11-2023",
        "tactic_type":"center shelf with coca cola bottles",
        "tactic_location":"center of store",
        "tactic_location_type":2,
        "store_id":[
            "s010"
        ],
        "customer_hierarchy_id":"1001",
        "customer_hierarchy_type":"H1",
        "product_types":[
            "cans"
        ],
        "product":"p001"
    }
    ]
    promotions_list = [
        {
        "promotion_id":"1013",
        "name":"RED BULL BRAND RB STACK",
        "type":"STACK",
        "campaign_type":"SHOWCASE DISPLAY",
        "campaign_description":"ISEB - UCI Capstone Showcase Display Promo",
        "status":[
            "inProcess",
            "released"
        ],
        "period_type":"SELL_IN",
        "start_date":"27-05-2024",
        "end_date":"31-05-2023",
        "tactic_type":"stack of red bull cans",
        "tactic_location":"on table",
        "tactic_location_type":2,
        "store_id":[
            "s011"
        ],
        "customer_hierarchy_id":"1001",
        "customer_hierarchy_type":"H1",
        "product_types":[
            "cans"
        ],
        "product":"p002"
        },
        {
        "promotion_id":"1013",
        "name":"COCA COLA BRAND CC STACK",
        "type":"STACK",
        "campaign_type":"SHOWCASE DISPLAY",
        "campaign_description":"ISEB - UCI Capstone Showcase Display Promo",
        "status":[
            "inProcess",
            "released"
        ],
        "period_type":"SELL_IN",
        "start_date":"27-05-2024",
        "end_date":"31-05-2023",
        "tactic_type":"stack of coca cola bottles",
        "tactic_location":"on table",
        "tactic_location_type":2,
        "store_id":[
            "s011"
        ],
        "customer_hierarchy_id":"1001",
        "customer_hierarchy_type":"H1",
        "product_types":[
            "cans"
        ],
        "product":"p001"
        }
    ]
    insert_documents_to_mongodb("promotions", promotions_list)

# add_promotions()
# add_products()
add_stores()