from PIL import Image, ExifTags
import math
import pandas as pd
from pymongo import MongoClient
from pprint import pprint
import datetime

exif = {'ImageWidth': 4032,
 'ImageLength': 3024,
 'GPSInfo': {1: 'N',
  2: (33.0, 38.0, 43.07676),
  3: 'W',
  4: (117.0, 49.0, 48.472319)},
 'ResolutionUnit': 2,
 'ExifOffset': 238,
 'Make': 'samsung',
 'Model': 'SM-G780F',
 'Software': 'G780FXXSGFXD1',
 'Orientation': 6,
 'DateTime': '2024:05:08 14:49:21',
 'YCbCrPositioning': 1,
 'XResolution': 72.0,
 'YResolution': 72.0,
 'ExifVersion': b'0220',
 'ShutterSpeedValue': 0.01,
 'ApertureValue': 1.69,
 'DateTimeOriginal': '2024:05:08 14:49:21',
 'DateTimeDigitized': '2024:05:08 14:49:21',
 'BrightnessValue': 2.46,
 'ExposureBiasValue': 0.0,
 'MaxApertureValue': 1.69,
 'MeteringMode': 2,
 'Flash': 0,
 'FocalLength': 5.4,
 'ColorSpace': 1,
 'ExifImageWidth': 4032,
 'DigitalZoomRatio': 1.0,
 'FocalLengthIn35mmFilm': 26,
 'SceneCaptureType': 0,
 'OffsetTime': '-07:00',
 'OffsetTimeOriginal': '-07:00',
 'SubsecTime': '061',
 'SubsecTimeOriginal': '061',
 'SubsecTimeDigitized': '061',
 'ExifImageHeight': 3024,
 'ExposureTime': 0.01,
 'FNumber': 1.8,
 'ImageUniqueID': 'X12LLND01AM',
 'ExposureProgram': 2,
 'ISOSpeedRatings': 200,
 'ExposureMode': 0,
 'WhiteBalance': 0}

def connect_to_db():
    # Connect to your MongoDB Atlas cluster
    client = MongoClient("mongodb+srv://sapsuser:3dUEbY0ijMlL81vF@sap-pv.bdcccxg.mongodb.net/?retryWrites=true&w=majority&appName=SAP-PV")
    db = client["SAPPV"]
    # st.session_state.db = db
    return db

db = connect_to_db()

def get_product_promoted_from_image(image):
    return "Red Bull"

def get_exif_tags_from_image(image):
    exif = {
    ExifTags.TAGS[k]: v
    for k, v in image._getexif().items()
    if k in ExifTags.TAGS
    }
    return exif

def filter_promotions_by_product(image, promotions):
    # Get the product name from the image
    product_name = get_product_promoted_from_image(image)
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

def filter_promotions_by_dates(image, promotions):
    # Get Date of Proof from exif image
    # exif_tags = get_exif_tags_from_image(image)

    date = exif["DateTime"]

    date = datetime.datetime.strptime(date, '%Y:%m:%d %H:%M:%S')

    # for each promotion
    for promotion in promotions[:]:
    # compare the date with the start and end date of the promotions in the promotions list
        start_date = promotion["start_date"]
        end_date = promotion["end_date"]
        if not (datetime.datetime.strptime(start_date, '%m-%d-%Y') <= date <= datetime.datetime.strptime(end_date, '%m-%d-%Y')):
            # remove the promotion from the list
            promotions.remove(promotion)
    # return the promotions that are active on the date of the proof
    return promotions

def trial_filter():
    # Get the collection
    collection = db["promotions"]

    # Get all the documents in the collection
    promotions = list(collection.find())
    
    print("All Promotions")
    pprint(promotions)

    # Filter the promotions by product
    promotions = filter_promotions_by_product("Image", promotions)

    print("Promotions after filtering by product")
    pprint(promotions)

    filter_promotions_by_dates("Image", promotions)

    print("Promotions after filtering by date")
    pprint(promotions)

trial_filter()
# store = db["albertsons"].find_one({"storeId": '1003'})
# print(store["coordinates"])
