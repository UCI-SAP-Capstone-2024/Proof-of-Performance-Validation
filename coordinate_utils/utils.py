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

def convert_gps_to_float_lat_lon(old):
    direction = {'N': 1, 'S' : -1, 'E' : 1, 'W' : -1}    
    return (int(old["val"][0])+int(old["val"][1])/60.0+int(old["val"][2])/3600.0) * direction[old["dir"]]

def get_exif_tags_from_image(image):
    exif = {
    ExifTags.TAGS[k]: v
    for k, v in image._getexif().items()
    if k in ExifTags.TAGS
    }
    return exif

def get_lat_long_from_exif(exif_data):
    location_data = {}
    location_data["lat"] = {}
    location_data["lon"] = {}
    
    try:
        location_data["lat"]["dir"] = exif_data["GPSInfo"][1]
        location_data["lat"]["val"] = exif_data["GPSInfo"][2]
        location_data["lon"]["dir"] = exif_data["GPSInfo"][3]
        location_data["lon"]["val"] = exif_data["GPSInfo"][4]
    except KeyError as k:
        print(k)
        print("Location Data Missing")
    
    return location_data

def extract_lat_long_from_image(image):
    # # Open Image From File Path
    # try:
    #     image = Image.open(image_path)
    # except FileNotFoundError as f:
    #     print(f)
    # Extract EXIF data from Image
    exif_tags = get_exif_tags_from_image(image)
    assert(exif_tags is not None)
    if(exif_tags is None):
        return
    # Get Lat and Long Data
    location_data_gps = get_lat_long_from_exif(exif_data=exif_tags)
    assert(location_data_gps is not None)
    try:
        final_coordinates = (convert_gps_to_float_lat_lon(location_data_gps["lat"]), convert_gps_to_float_lat_lon(location_data_gps["lon"]))
    except KeyError as k:
        print("key Error", k)
    return final_coordinates

def extract_date_from_image(image):
    exif_tags = get_exif_tags_from_image(image)
    
    date = exif_tags["DateTime"]

    date = datetime.datetime.strptime(date, '%Y:%m:%d %H:%M:%S')

    return date
    

def spherical_law_of_cosines(loc_1, loc_2):
    lat1 = loc_1[0]
    lon1 = loc_1[1]
    lat2 = loc_2[0]
    lon2 = loc_2[1]

    φ1 = lat1 * math.pi / 180
    φ2 = lat2 * math.pi / 180
    Δλ = (lon2 - lon1) * math.pi / 180
    R = 6371000  # Earth's radius in meters
    
    dist = math.acos(math.sin(φ1) * math.sin(φ2) + math.cos(φ1) * math.cos(φ2) * math.cos(Δλ)) * R

    # Convert distance to freedom units
    dist_feet = dist * 3.28084
    return dist_feet

def validate_if_image_is_from_given_location(image_location, location):
    distance = spherical_law_of_cosines(image_location, location)
    # Threshold For Detection is 500 ft / ~150m
    if(distance > 500):
        return False
    return True

def get_product_promoted_from_image(image):
    return "Red Bull"

def print_HI():
    print("HI")

def serialize_coordinates(latlon):
    coordinates = latlon.split(',')
    return (float(coordinates[0]), float(coordinates[1]))

def filter_promotions_by_dates(promotion_date, promotions):
    # for each promotion
    for promotion in promotions[:]:
    # compare the date with the start and end date of the promotions in the promotions list
        start_date = promotion["start_date"]
        end_date = promotion["end_date"]
        if not (datetime.datetime.strptime(start_date, '%m-%d-%Y') <= promotion_date <= datetime.datetime.strptime(end_date, '%m-%d-%Y')):
            # remove the promotion from the list
            promotions.remove(promotion)
    # return the promotions that are active on the date of the proof
    return promotions

def filter_promotions_by_coordinates(image_location, promotions):
    # Get location data from the image

    # fro each promotion
    for promotion in promotions[:]:
        # get the store id
        store_id = promotion["customer_hierarchy_id"]

        print(store_id)
        # gget the coordinates of the store
        store = db["albertsons"].find_one({"storeId": store_id})
        store_coordinates = serialize_coordinates(store["coordinates"])
        # compare the coordinates of the store with the coordinates of the image
        if not validate_if_image_is_from_given_location(image_location, store_coordinates):
            # remove the promotion from the list
            promotions.remove(promotion)

    # return the promotions that are near the image
    return promotions, store_id
    # pass

def get_image_details(image):
    # Get Image Coordinates
    image_location = extract_lat_long_from_image(image)

    # Get Image Date
    image_date = extract_date_from_image(image)

    # Get Image Product
    image_product = get_product_promoted_from_image(image)

    return (image_location, image_date, image_product)

def filter_promotions_by_product(product_name, promotions):
    # for each promotion
    for promotion in promotions[:]:
    # get the product name
        promotion_product_name = promotion["name"]
        # compare the product name with the product name in the image
        if product_name.lower() not in promotion_product_name.lower():
            # remove the promotion from the list
            promotions.remove(promotion)
    # return the promotions that match the product name
    return promotions

def get_customer_details(matched_promotion):
    # customer_id = matched_promotion["customer_id"]
    # matched_customer = db["customers"].find_one({"customer_id": customer_id})
    # matched
    pass

def match_promotion_to_retailer(image):
    # Read the CSV file into a pandas DataFrame
    # df = pd.read_csv("promotions.csv")
    # db = connect_to_db()

    # Get the collection
    collection = db["promotions"]

    # Get all the documents in the collection
    promotions = list(collection.find())

    # Image Details
    image_location, image_date, image_product = get_image_details(image)
    
    # Filter the promotions by product
    promotions = filter_promotions_by_product(image_product, promotions)

    # Filter the promotions by date
    promotions = filter_promotions_by_dates(image_date, promotions)

    # Filter the promotions by coordinates
    promotions, store_id = filter_promotions_by_coordinates(image_location, promotions)

    # # This dictionary will store coordinates as keys and all corresponding rows as values
    # coordinate_matches = []

    # # Iterate through each row in the DataFrame
    # for index, row in df.iterrows():
    #     coord = row['retailer_coordinates']

    #     coord = serialize_coordinates(coord)


    #     if validate_if_image_is_from_given_location(image, coord) == True:
    #         # If coordinates already in the dictionary, append the current row
    #         coordinate_matches.append({"store": row["retailer_name"], "address": row["retailer_address"], "coordinates": coord, "product_name": row["product_name"]})

    store_details = db["albertsons"].find_one({"storeId": store_id})

    matched_promotion = {
        "promotion_id" : promotions[0]["id"],
        "promotion_name" : promotions[0]["name"],
        "promotion_description" : promotions[0]["campaign_description"],
        "promotion_start_date" : promotions[0]["start_date"],
        "promotion_end_date" : promotions[0]["end_date"],
        "customer_id" : promotions[0]["customer_id"],
        "store_id" : store_id,
        "address" : store_details["address"],
        "product": image_product
    }

    # matched_promotion = get_customer_details(matched_promotion)

    print(matched_promotion)

    return matched_promotion
    # return coordinate_matches