import re

# ================= NORMAL RANGES =================

NORMAL_RANGES = {
    "hemoglobin": (12, 17),
    "wbc": (4000, 11000),
    "platelets": (150000, 450000),
    "glucose": (70, 140)
}

# ================= CLEAN NUMBER =================

def clean_number(value):

    value = value.replace(",", "")

    try:
        return float(value)

    except:
        return None

# ================= EXTRACTION =================

def extract_medical_values(text):

    text = text.lower()

    results = {}

    patterns = {

        "hemoglobin": [
            r"hemoglobin.*?(\\d+\\.?\\d*)",
            r"hb.*?(\\d+\\.?\\d*)"
        ],

        "wbc": [
            r"wbc.*?(\\d+[\\,\\d]*)",
            r"white blood cell.*?(\\d+[\\,\\d]*)"
        ],

        "platelets": [
            r"platelets.*?(\\d+[\\,\\d]*)"
        ],

        "glucose": [
            r"glucose.*?(\\d+\\.?\\d*)",
            r"blood sugar.*?(\\d+\\.?\\d*)"
        ]
    }

    for key, regex_list in patterns.items():

        for pattern in regex_list:

            matches = re.findall(
                pattern,
                text,
                re.IGNORECASE
            )

            if matches:

                value = clean_number(
                    matches[0]
                )

                if value is not None:

                    results[key] = value

                    break

    return results

# ================= ANALYSIS =================

def analyze_medical_values(values):

    analysis = []

    for key, value in values.items():

        low, high = NORMAL_RANGES[key]

        if value < low:

            analysis.append(
                f"{key.capitalize()} is LOW ({value})"
            )

        elif value > high:

            analysis.append(
                f"{key.capitalize()} is HIGH ({value})"
            )

        else:

            analysis.append(
                f"{key.capitalize()} is NORMAL ({value})"
            )

    return analysis