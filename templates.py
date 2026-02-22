TEMPLATES = {
    "10th Marksheet": {
        "keywords": ["SSLC", "SECONDARY", "MARKS"],
        "patterns": {
            "year": r"\b20\d{2}\b",
            "percentage": r"\b\d{2}\.\d{2}%\b|\b\d{2}%\b"
        }
    },

    "12th Marksheet": {
        "keywords": ["PUC", "HIGHER SECONDARY", "MARKS"],
        "patterns": {
            "year": r"\b20\d{2}\b",
            "percentage": r"\b\d{2}\.\d{2}%\b|\b\d{2}%\b"
        }
    },

    "CET Score Card": {
        "keywords": ["CET", "SCORE"],
        "patterns": {
            "rank": r"\bRANK\s*\d+\b|\b\d{1,6}\b"
        }
    },

    "Photo ID (Aadhaar)": {
        "keywords": ["GOVERNMENT OF INDIA"],
        "patterns": {
            "aadhaar_number": r"\b\d{4}\s\d{4}\s\d{4}\b"
        }
    },

    "UG Degree Certificate": {
        "keywords": ["DEGREE", "CERTIFICATE", "GRADUATION"],
        "patterns": {
            "year": r"\b20\d{2}\b",
            "degree_name": r"(BACHELOR OF TECHNOLOGY|B\.TECH|BCA)"
        }
    },

    "PGCET Score Card": {
        "keywords": ["PGCET", "SCORE", "RANK"],
        "patterns": {
            "rank": r"\bRANK\s*\d+\b|\b\d{1,6}\b",
            "score": r"\b\d{2,3}\b"
        }
    }
}