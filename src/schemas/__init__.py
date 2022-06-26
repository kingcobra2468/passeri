import os
import json


def load_schema(name):
    """Loads a given JSON schema.

    Args:
        name (str): Name of the file.

    Returns:
        dict: JSON contents of the file.
    """
    module_path = os.path.dirname(__file__)
    path = os.path.join(module_path, '{}.json'.format(name))

    with open(os.path.abspath(path), 'r') as fp:
        data = fp.read()

    return json.loads(data)
