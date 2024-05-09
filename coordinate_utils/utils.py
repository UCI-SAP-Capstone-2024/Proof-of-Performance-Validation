from PIL import Image, ExifTags
import math
import pandas as pd

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

def validate_if_image_is_from_given_location(image, location):
    image_location = extract_lat_long_from_image(image)
    distance = spherical_law_of_cosines(image_location, location)
    # Threshold For Detection is 500 ft / ~150m
    if(distance > 500):
        return False
    return True

def print_HI():
    print("HI")

def serialize_coordinates(latlon):
    coordinates = latlon.split(',')
    return (float(coordinates[0]), float(coordinates[1]))

def match_promotion_to_retailer(image):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv("promotions.csv")

    # This dictionary will store coordinates as keys and all corresponding rows as values
    coordinate_matches = []

    # Iterate through each row in the DataFr    ame
    for index, row in df.iterrows():
        coord = row['retailer_coordinates']

        coord = serialize_coordinates(coord)


        if validate_if_image_is_from_given_location(image, coord) == True:
            # If coordinates already in the dictionary, append the current row
            coordinate_matches.append({"store": row["retailer_name"], "address": row["retailer_address"], "coordinates": coord, "product_name": row["product_name"]})

    return coordinate_matches