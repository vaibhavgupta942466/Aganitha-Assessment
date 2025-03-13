OUTPUT_FOLDER_NAME = 'output'
OUTPUT_LOG_FOLDER_NAME = 'logs'
OUTPUT_FILE_NAME = 'output.csv'

# pubmed_fetcher/constants.py
CSV_HEADERS = [
    "PubMed ID", "Title", "Publication Date",
    "Non-academic Authors", "Company Affiliations", "Corresponding Author Email"
]

COMPANY_KEYWORDS = [
    "inc", "incorporated", "pharma", "pharmaceutical", "biotech",
    "ltd", "limited", "corp", "corporation", "company", "co"
]

ACADEMIC_KEYWORDS = [
    "university", "college", "institute", "school", "academic",
    "research center", "laboratory", "department"
]