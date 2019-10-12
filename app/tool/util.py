import json


def list2json(_list, return_str=False):
    temp = json.dumps(_list)

    if return_str is True:
        return json.loads(temp)
    return temp
