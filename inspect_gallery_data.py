# inspect_gallery_data.py
import json

output_file = "gallery-data.json"

with open(output_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

if isinstance(data, dict):
    print("Data is a dictionary. Keys:")
    for k in data.keys():
        val = data[k]
        if isinstance(val, list):
            print(f"  {k}: list of length {len(val)}")
        else:
            print(f"  {k}: {type(val)}")
    
    # Check if there is a 'posts' or similar key
    for k in data.keys():
        if isinstance(data[k], list) and len(data[k]) > 0:
            print(f"Sample from '{k}':")
            sample = data[k][0]
            if isinstance(sample, dict):
                for sk, sv in sample.items():
                    val_str = str(sv)
                    if len(val_str) > 120:
                        val_str = val_str[:120] + "..."
                    print(f"    {sk}: {val_str}")
elif isinstance(data, list):
    print(f"Data is a list of length {len(data)}")
else:
    print(f"Data has type {type(data)}")
