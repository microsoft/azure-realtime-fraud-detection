def get_benford_items(type):    
    items = []

    if type == 'first-digit':
        for id in range(10):
            item = {
                    "id": f"{id}",
                    "digit_count": 0,
                    "digit_percent": 0.0
                }
            items.append(item)
    else:
        for id in range(1, 10):
            item = {
                    "id": f"{id}",
                    "digit_count": 0,
                    "digit_percent": 0.0
                }
            items.append(item)
    return items

def get_customer_items():
    import json
    import os

    root_dir = os.path.dirname(os.path.abspath(__file__))

    with open(root_dir + '/customers.json', 'rb') as f:
        data_bytes = f.read()
    
    content = json.loads(data_bytes)
    return content['data']