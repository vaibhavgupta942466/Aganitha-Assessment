# aganitha_assessment/mapper.py
import re
from typing import Dict, List, Optional
import logging
from .constants import ACADEMIC_KEYWORDS, COMPANY_KEYWORDS, CSV_HEADERS

class PaperMapper:
    """Maps PubMed records to a structured format, focusing on non-academic authors and affiliations."""

    def __init__(self, logger: logging.Logger):
        """Initialize the PaperMapper with logging and patterns for company detection and email extraction."""
        self.logger = logger
        
        # Keywords to identify potential company affiliations (case-insensitive)
        self.company_keywords = COMPANY_KEYWORDS
        
        # Regex pattern to find email addresses
        self.email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

    def _extract_email(self, record: Dict) -> Optional[str]:
        """Extract the first email address from affiliation or other fields in the record.

        Args:
            record (Dict): A PubMed record.

        Returns:
            Optional[str]: The first email found, or None if no email is present.
        """
        # Fields to check for email addresses, in order of preference
        fields_to_check = ["AD", "OT", "AB"]
        for field in fields_to_check:
            if field in record:
                # Combine list fields into a single string
                text = " ".join(record[field]) if isinstance(record[field], list) else record[field]
                match = self.email_pattern.search(text)
                if match:
                    return match.group(0)
        return None

    def _is_company_affiliation(self, affiliation: str) -> bool:
        """Determine if an affiliation likely belongs to a company based on keywords.

        Args:
            affiliation (str): The affiliation text to check.

        Returns:
            bool: True if the affiliation contains company-related keywords, False otherwise.
        """
        affiliation_lower = affiliation.lower()
        # Check for academic keywords first
        is_academic = any(keyword in affiliation_lower for keyword in ACADEMIC_KEYWORDS)
        is_company = any(keyword in affiliation_lower for keyword in self.company_keywords)
        # Consider it a company affiliation only if it has company keywords and no academic ones
        return is_company and not is_academic

    def _extract_non_academic_authors(self, record: Dict) -> List[Dict[str, str]]:
        """Extract authors affiliated with non-academic institutions and their affiliations.

        Args:
            record (Dict): A PubMed record.

        Returns:
            List[Dict[str, str]]: A list of dictionaries with 'author' and 'affiliation' for non-academic authors.
        """
        authors = record.get("AU", [])
        affiliations = record.get("AD", [])
        non_academic_authors = []

        # If affiliations are missing or don't match authors, log a warning and return empty list
        if not affiliations or len(affiliations) < len(authors):
            self.logger.warning(f"Insufficient affiliations for authors in record {record.get('PMID', 'Unknown')}")
            return non_academic_authors
        
        # Log all affiliations for debugging
        self.logger.info(f"Affiliations for PMID {record.get('PMID', 'Unknown')}: {affiliations}")

        # Map authors to their affiliations (assuming one affiliation per author)
        for author, affiliation in zip(authors, affiliations):
            if self._is_company_affiliation(affiliation):
                non_academic_authors.append({
                    "author": author,
                    "affiliation": affiliation
                })

        return non_academic_authors

    def map_records(self, records: List[Dict]) -> List[Dict]:
        """Map a list of PubMed records to a structured format.

        Args:
            records (List[Dict]): List of PubMed records.

        Returns:
            List[Dict]: List of mapped records with selected fields and non-academic author information.
        """
        mapped_papers = []
        for record in records:
            try:
                # Extract non-academic authors and their affiliations
                non_academic_info = self._extract_non_academic_authors(record)
                non_academic_authors = [info["author"] for info in non_academic_info]
                company_affiliations = [info["affiliation"] for info in non_academic_info]

                # Default to "N/A" if no non-academic authors are found
                if not non_academic_authors:
                    non_academic_authors = ["N/A"]
                    company_affiliations = ["N/A"]

                # Extract email, defaulting to "N/A" if not found
                email = self._extract_email(record) or "N/A"

                paper = {
                    "pmid": record.get("PMID", "N/A"),
                    "title": record.get("TI", "No Title"),
                    "publication_date": record.get("DP", "Unknown Date"),
                    "non_academic_authors": non_academic_authors,
                    "company_affiliations": company_affiliations,
                    "corresponding_author_email": email
                }
                mapped_papers.append(paper)
            except Exception as e:
                self.logger.error(f"Error mapping record {record.get('PMID', 'Unknown')}: {str(e)}")
                continue
        return mapped_papers