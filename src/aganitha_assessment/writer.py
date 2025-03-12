# aganitha_assessment/writer.py
import csv
import os
import logging
from typing import List, Dict

class CSVWriter:
    """Writes PubMed paper data to a CSV file with predefined headers."""

    def __init__(self, file: str, logger: logging.Logger):
        """Initialize the CSVWriter with the target file.

        Args:
            file (str): The path to the CSV file to write to.
        """
        self.logger = logger
        self.file = file
        # Define CSV headers
        self.headers = [
            "PubMed ID", "Title", "Publication Date",
            "Non-academic Authors", "Company Affiliations", "Corresponding Author Email"
        ]
        # Check if file exists to determine whether to write headers
        self.file_exists = os.path.isfile(file)

    def write_papers(self, papers: List[Dict]) -> None:
        """Write a list of paper data to the CSV file.

        Args:
            papers (List[Dict]): A list of dictionaries, each containing paper data.
        """
        try:
            with open(self.file, mode='a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.headers)

                # Write headers if the file is new
                if not self.file_exists:
                    self.logger.info(f"Created new file '{self.file}' and writing headers.")
                    writer.writeheader()
                    self.file_exists = True  # Update flag after writing headers

                # Write each paper's data to the CSV
                for paper in papers:
                    writer.writerow({
                        "PubMed ID": paper.get("pmid", "N/A"),
                        "Title": paper.get("title", "No Title"),
                        "Publication Date": paper.get("publication_date", "Unknown Date"),
                        "Non-academic Authors": ", ".join(paper.get("non_academic_authors", ["N/A"])),
                        "Company Affiliations": ", ".join(paper.get("company_affiliations", ["N/A"])),
                        "Corresponding Author Email": paper.get("corresponding_author_email", "N/A")
                    })
        except Exception as e:
            self.logger.error(f"Failed to write to CSV file '{self.file}': {str(e)}")
            raise RuntimeError(f"CSV writing failed: {str(e)}")