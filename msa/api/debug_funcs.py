import json

method_error_message = "Request method is not POST"
GET_error_message = "Request method is not GET"
success_message = "Data received successfully."
json_error_message = "JSON decode error"
add_message = " added successfully at Key "
key_error = " key error \n"
empty_error = " empty. \n"
type_error = " type error \n"


def validateJson(data):
    try:
        json_entry = json.loads(data.decode("utf-8"))
    except:
        message = json_error_message
        return False, message
    return True, json_entry


def checkData(dict_data, key, text):
    if text == "text":
        try:
            value = dict_data[key]
            if not value:
                message = key + empty_error
            elif not isinstance(value, str):
                message = key + type_error
                return False, message
            elif value.isspace():
                message = key + empty_error
            else:
                message = key + ": " + value + " \n"
        except KeyError:
            message = key + key_error
            return False, message
        return True, message

    if text == "num":
        try:
            value = dict_data[key]
            if not (isinstance(value, int) or isinstance(value, float)):
                message = key + type_error
                return False, message
            else:
                message = key + ": " + str(value) + " \n"
        except KeyError:
            message = key + key_error
            return False, message
        return True, message

    if text == "geojson":
        try:
            value = dict_data[key]
            if not (isinstance(value, dict)):
                message = key + type_error
                return False, message
            if len(value) != 2:
                message = key + " invalid"
                return False, message
            if not (isinstance(value['coordinates'][0], float) and isinstance(value['coordinates'][1], float)):
                message = key + type_error
                return False, message
            else:
                message = key + ": " + str(value) + " \n"
        except KeyError:
            message = key + key_error
            return False, message
        return True, message
