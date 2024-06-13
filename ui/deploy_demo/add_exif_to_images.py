from PIL import Image
from exif import Image as ExifImage

def add_exif_to_image(input_path, output_path, exif_data):
    # Open the image using Pillow
    with open(input_path, 'rb') as img_file:
        img = ExifImage(img_file)

    # Add or modify EXIF data
    img.make = exif_data.get("Make", "Unknown")
    img.model = exif_data.get("Model", "Unknown")
    img.software = exif_data.get("Software", "Unknown")
    img.orientation = exif_data.get("Orientation", 1)
    img.datetime = exif_data.get("DateTime", "2023:05:15 14:49:21")
    img.ycbcr_positioning = exif_data.get("YCbCrPositioning", 1)
    # img.x_resolution = exif_data.get("XResolution", 72.0)
    # img.y_resolution = exif_data.get("YResolution", 72.0)
    # img.exif_version = exif_data.get("ExifVersion", b'0220')
    # img.shutter_speed_value = exif_data.get("ShutterSpeedValue", 0.01)
    # img.aperture_value = exif_data.get("ApertureValue", 1.69)
    img.datetime_original = exif_data.get("DateTimeOriginal", "2023:05:15 14:49:21")
    img.datetime_digitized = exif_data.get("DateTimeDigitized", "2023:05:15 14:49:21")
    img.brightness_value = exif_data.get("BrightnessValue", 2.46)
    img.exposure_bias_value = exif_data.get("ExposureBiasValue", 0.0)
    img.max_aperture_value = exif_data.get("MaxApertureValue", 1.69)
    img.metering_mode = exif_data.get("MeteringMode", 2)
    img.flash = exif_data.get("Flash", 0)
    img.focal_length = exif_data.get("FocalLength", 5.4)
    img.color_space = exif_data.get("ColorSpace", 1)
    img.pixel_x_dimension = exif_data.get("ExifImageWidth", 4032)
    img.pixel_y_dimension = exif_data.get("ExifImageHeight", 3024)
    img.digital_zoom_ratio = exif_data.get("DigitalZoomRatio", 1.0)
    img.focal_length_in_35mm_film = exif_data.get("FocalLengthIn35mmFilm", 26)
    img.scene_capture_type = exif_data.get("SceneCaptureType", 0)
    # img.offset_time = exif_data.get("OffsetTime", "-07:00")
    # img.offset_time_original = exif_data.get("OffsetTimeOriginal", "-07:00")
    # img.subsec_time = exif_data.get("SubsecTime", "061")
    # img.subsec_time_original = exif_data.get("SubsecTimeOriginal", "061")
    # img.subsec_time_digitized = exif_data.get("SubsecTimeDigitized", "061")
    img.exposure_time = exif_data.get("ExposureTime", 0.01)
    img.f_number = exif_data.get("FNumber", 1.8)
    img.image_unique_id = exif_data.get("ImageUniqueID", "X12LLND01AM")
    img.exposure_program = exif_data.get("ExposureProgram", 2)
    img.iso_speed_ratings = exif_data.get("ISOSpeedRatings", 200)
    img.exposure_mode = exif_data.get("ExposureMode", 0)
    img.white_balance = exif_data.get("WhiteBalance", 0)

    # GPS Info
    gps_info = exif_data.get("GPSInfo", {})
    if gps_info:
        img.gps_latitude_ref = gps_info.get(1, 'N')
        img.gps_latitude = gps_info.get(2, (0.0, 0.0, 0.0))
        img.gps_longitude_ref = gps_info.get(3, 'W')
        img.gps_longitude = gps_info.get(4, (0.0, 0.0, 0.0))

    # Save the image with new EXIF data
    with open(output_path, 'wb') as new_img_file:
        new_img_file.write(img.get_file())

    return new_img_file

def has_exif_data(image_path):
    try:
        with open(image_path, 'rb') as img_file:
            img = ExifImage(img_file)
            return img.has_exif, img
    except Exception as e:
        print(f"Error: {e}")
        return False, None

# Example usage
if __name__ == "__main__":
    # input_image_path = "C:/Users/Om Naik/Downloads/20240526_173352.jpg"
    # 
    input_image_path = "C:/Users/Om Naik/Downloads/images_to_use/rb05.jpg"
    output_image_path = "C:/Users/Om Naik/Downloads/mages_to2/rb99.jpg"
    
    # Example EXIF data to add/modify
    exif_data = {
        'ImageWidth': 4032,
        'ImageLength': 3024,
        'GPSInfo': {
            1: 'N',
            2: (33.0, 38.0, 35.5446),
            3: 'W',
            4: (117.0, 50.0, 39.6204)
        },
        'ResolutionUnit': 2,
        'ExifOffset': 238,
        'Make': 'samsung',
        'Model': 'SM-G780F',
        'Software': 'G780FXXSGFXD1',
        'Orientation': 1,
        'DateTime': '2023:05:15 14:49:21',
        'YCbCrPositioning': 1,
        'XResolution': 72.0,
        'YResolution': 72.0,
        'ExifVersion': b'0220',
        'ShutterSpeedValue': 0.01,
        'ApertureValue': 1.69,
        'DateTimeOriginal': '2023:05:15 14:49:21',
        'DateTimeDigitized': '2023:05:15 14:49:21',
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
        'WhiteBalance': 0
    }
    
    new = add_exif_to_image(input_image_path, output_image_path, exif_data)
    print(f"Image saved with EXIF data at: {output_image_path}")

    # print(new.has_exif)
    has_exif, exif_img = has_exif_data(output_image_path)
    
    if has_exif:
        print("Image has EXIF data.")
        print(exif_img.list_all())
        for tag in exif_img.list_all():
            print(f"{tag}: {getattr(exif_img, tag)}")
    else:
        print("Image does not have EXIF data.")


