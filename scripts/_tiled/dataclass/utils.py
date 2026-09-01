
def extract_propertie(data):
    if      data["type"] == "bool":     return bool(data["value"])
    elif    data["type"] ==  "int":     return int(data["value"])
    elif    data["type"] ==  "float":   return float(data["value"])
    elif    data["type"] ==  "list":    return [extract_propertie(value) for value in data["value"]]
    else:                               return str(data["value"])

def extract_properties(property_list):
	return {data["name"]: extract_propertie(data) for data in property_list}