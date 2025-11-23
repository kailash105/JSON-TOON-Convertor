import json

def json_to_toon(data):
    """
    Convert JSON data into a simplified TOON format.
    """
    if isinstance(data, list) and all(isinstance(i, dict) for i in data):
        keys = data[0].keys()
        toon = f"[{len(data)}]{{{','.join(keys)}}}:\n"
        for item in data:
            values = [str(item.get(k, '')) for k in keys]
            toon += "  " + ",".join(values) + "\n"
        return toon
    elif isinstance(data, dict):
        lines = []
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                sub = json_to_toon(v).replace("\n", "\n  ")
                lines.append(f"{k}:\n  {sub}")
            else:
                lines.append(f"{k}: {v}")
        return "\n".join(lines)
    else:
        return str(data)
