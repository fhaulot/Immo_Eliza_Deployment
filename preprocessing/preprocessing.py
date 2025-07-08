def preprocess_data(data):
    # Convert input into dict for flexibility
    data = data.dict(by_alias=True)

    # Minimal preprocessing example (expand as needed)
    processed = {
        "area": data["area"],
        "rooms_number": data["rooms-number"],
        "zip_code": data["zip-code"],
        "property_type": {"APARTMENT": 0, "HOUSE": 1, "OTHERS": 2}[data["property-type"]],
        "garden": int(data["garden"]) if data["garden"] is not None else 0,
        "terrace": int(data["terrace"]) if data["terrace"] is not None else 0,
        # ... include other relevant fields with defaults
    }

    return list(processed.values())
