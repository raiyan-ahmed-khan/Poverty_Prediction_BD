# src/name_mapping.py
"""
District name standardization across data sources.
Different datasets use different spellings for the same districts.
This mapping standardizes everything to the BBS HIES 2022 naming convention.
"""

# Maps common alternate spellings -> Standard name (BBS official)
DISTRICT_NAME_MAP = {
    # Chattogram Division
    "Chittagong": "Chattogram",
    "Chittangong": "Chattogram",
    "Comilla": "Cumilla",
    "Cumilla": "Cumilla",
    "Cox's Bazar": "Cox's Bazar",
    "Coxs Bazar": "Cox's Bazar",
    "Noakhali": "Noakhali",
    "Brahmanbaria": "Brahmanbaria",
    "Feni": "Feni",
    "Khagrachhari": "Khagrachhari",
    "Rangamati": "Rangamati",
    "Bandarban": "Bandarban",
    "Lakshmipur": "Lakshmipur",
    "Chandpur": "Chandpur",

    # Dhaka Division
    "Dhaka": "Dhaka",
    "Gazipur": "Gazipur",
    "Narayanganj": "Narayanganj",
    "Manikganj": "Manikganj",
    "Munshiganj": "Munshiganj",
    "Narsingdi": "Narsingdi",
    "Tangail": "Tangail",
    "Kishorganj": "Kishoreganj",
    "Kisghoreganj": "Kishoreganj",
    "Netrokona": "Netrokona",
    "Mymensingh": "Mymensingh",
    "Jamalpur": "Jamalpur",
    "Sherpur": "Sherpur",
    "Faridpur": "Faridpur",
    "Gopalganj": "Gopalganj",
    "Madaripur": "Madaripur",
    "Rajbari": "Rajbari",
    "Shariatpur": "Shariatpur",

    # Khulna Division
    "Khulna": "Khulna",
    "Jessore": "Jashore",
    "Jhenaidah": "Jhenaidah",
    "Magura": "Magura",
    "Narail": "Narail",
    "Satkhira": "Satkhira",
    "Bagerhat": "Bagerhat",
    "Meherpur": "Meherpur",
    "Chuadanga": "Chuadanga",
    "Kushtia": "Kushtia",

    # Rajshahi Division
    "Rajshahi": "Rajshahi",
    "Bogra": "Bogura",
    "Bogura": "Bogura",
    "Chapai Nawabganj": "Chapai Nawabganj",
    "Chapainawabganj": "Chapai Nawabganj",
    "Joypurhat": "Joypurhat",
    "Naogaon": "Naogaon",
    "Natore": "Natore",
    "Pabna": "Pabna",
    "Sirajganj": "Sirajganj",

    # Rangpur Division
    "Rangpur": "Rangpur",
    "Dinajpur": "Dinajpur",
    "Gaibandha": "Gaibandha",
    "Kurigram": "Kurigram",
    "Lalmonirhat": "Lalmonirhat",
    "Nilphamari": "Nilphamari",
    "Panchagarh": "Panchagarh",
    "Thakurgaon": "Thakurgaon",

    # Barishal Division
    "Barisal": "Barishal",
    "Barishal": "Barishal",
    "Barguna": "Barguna",
    "Bhola": "Bhola",
    "Jhalokati": "Jhalokati",
    "Patuakhali": "Patuakhali",
    "Pirojpur": "Pirojpur",

    # Sylhet Division
    "Sylhet": "Sylhet",
    "Habiganj": "Habiganj",
    "Moulvibazar": "Moulvibazar",
    "Sunamganj": "Sunamganj",

    # Mymensingh Division
    "Netrakona": "Netrokona",
}

# Division membership for each district
DISTRICT_TO_DIVISION = {
    "Chattogram": "Chattogram", "Cumilla": "Chattogram", "Cox's Bazar": "Chattogram",
    "Noakhali": "Chattogram", "Brahmanbaria": "Chattogram", "Feni": "Chattogram",
    "Khagrachhari": "Chattogram", "Rangamati": "Chattogram", "Bandarban": "Chattogram",
    "Lakshmipur": "Chattogram", "Chandpur": "Chattogram",

    "Dhaka": "Dhaka", "Gazipur": "Dhaka", "Narayanganj": "Dhaka",
    "Manikganj": "Dhaka", "Munshiganj": "Dhaka", "Narsingdi": "Dhaka",
    "Tangail": "Dhaka", "Kishoreganj": "Dhaka", "Faridpur": "Dhaka",
    "Gopalganj": "Dhaka", "Madaripur": "Dhaka", "Rajbari": "Dhaka",
    "Shariatpur": "Dhaka",

    "Mymensingh": "Mymensingh", "Netrokona": "Mymensingh",
    "Jamalpur": "Mymensingh", "Sherpur": "Mymensingh",

    "Khulna": "Khulna", "Jashore": "Khulna", "Jhenaidah": "Khulna",
    "Magura": "Khulna", "Narail": "Khulna", "Satkhira": "Khulna",
    "Bagerhat": "Khulna", "Meherpur": "Khulna", "Chuadanga": "Khulna",
    "Kushtia": "Khulna",

    "Rajshahi": "Rajshahi", "Bogura": "Rajshahi", "Chapai Nawabganj": "Rajshahi",
    "Joypurhat": "Rajshahi", "Naogaon": "Rajshahi", "Natore": "Rajshahi",
    "Pabna": "Rajshahi", "Sirajganj": "Rajshahi",

    "Rangpur": "Rangpur", "Dinajpur": "Rangpur", "Gaibandha": "Rangpur",
    "Kurigram": "Rangpur", "Lalmonirhat": "Rangpur", "Nilphamari": "Rangpur",
    "Panchagarh": "Rangpur", "Thakurgaon": "Rangpur",

    "Barishal": "Barishal", "Barguna": "Barishal", "Bhola": "Barishal",
    "Jhalokati": "Barishal", "Patuakhali": "Barishal", "Pirojpur": "Barishal",

    "Sylhet": "Sylhet", "Habiganj": "Sylhet", "Moulvibazar": "Sylhet",
    "Sunamganj": "Sylhet",
}


def standardize_name(name: str) -> str:
    """
    Standardize a district or division name to BBS official spelling.
    
    Args:
        name: Raw district/division name from any data source
    Returns:
        Standardized name string
    """
    if not name:
        return name
    cleaned = name.strip().title()
    return DISTRICT_NAME_MAP.get(cleaned, cleaned)


def get_division(district_name: str) -> str:
    """
    Get the division for a given district name.
    
    Args:
        district_name: Standardized district name
    Returns:
        Division name string, or 'Unknown' if not found
    """
    std = standardize_name(district_name)
    return DISTRICT_TO_DIVISION.get(std, "Unknown")


if __name__ == "__main__":
    # Quick test
    test_cases = ["Chittagong", "Jessore", "Bogra", "Barisal", "Comilla"]
    for name in test_cases:
        print(f"{name:20} -> {standardize_name(name):20} (Division: {get_division(name)})")
