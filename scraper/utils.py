import json

def make_serializable(value):
    if hasattr(value, '__dict__'):
        return value.__dict__
    return value

def save_json(file_path, obj):
    output = json.dumps(obj.__dict__, indent=4, default=make_serializable)
    with open(file_path, "w") as file_handle:
        file_handle.write(output)

