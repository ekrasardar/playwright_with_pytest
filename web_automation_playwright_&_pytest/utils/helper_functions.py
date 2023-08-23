import re, json, os


def write_data_to_json(fieldname, value):
    filename = "tests/test_data.json"
    # try to open the JSON file and load the contents into a dictionary
    try:
        with open(filename, "r") as f:
            invoice_dict = json.load(f)
    except FileNotFoundError:
        # if the file doesn't exist, create a new dictionary
        invoice_dict = {}
    except json.JSONDecodeError:
        # if the file exists but is not a valid JSON, raise an error
        raise ValueError("Invalid JSON file: {}".format(filename))

    # add or update the field in the dictionary
    invoice_dict[fieldname] = value

    # save the dictionary to the JSON file
    with open(filename, "w") as f:
        json.dump(invoice_dict, f)

    # print a success message
    print(f"Saved {fieldname}: {value} to file {filename}")


def get_data_from_json_file(fieldname):
    try:
        # open the JSON file and load the contents into a dictionary
        with open("test_parameter.json", "r") as f:
            invoice_dict = json.load(f)
        # extract the invoice ID from the dictionary
        retrieved_invoice_id = invoice_dict.get(fieldname)
        if retrieved_invoice_id:
            print("Retrieved data {} from file".format(retrieved_invoice_id))
            return retrieved_invoice_id
        else:
            print("Data not found in file: {}".format(fieldname))
            return None
    except FileNotFoundError:
        print("File not found")
        return None
    except json.JSONDecodeError:
        print("Invalid JSON file")
        return None


def get_file_path(directory, filename, folder_name):
    """
    Retrieve a file path given a directory, a filename, and the name of the folder where the file is available.

    Args:
        directory (str): The root directory to search for the folder and file.
        filename (str): The name of the file to retrieve.
        folder_name (str): The name of the folder where the file is available.

    Returns:
        str: The full file path of the file, or None if the file is not found.
    """
    folder_path = os.path.join(directory, folder_name)
    if not os.path.exists(folder_path):
        return None
    for root, dirs, files in os.walk(folder_path):
        if filename in files:
            return os.path.join(root, filename)
    return None
