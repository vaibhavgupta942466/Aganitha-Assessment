# aganitha_assessment/fetcher.py
from Bio import Entrez
from Bio import Medline
import logging
from typing import List, Dict
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class PubMedFetcher:
    """A class to fetch PubMed data using the Entrez API from Biopython."""
    
    def __init__(self, logger: logging.Logger):
        """Initialize the PubMedFetcher with NCBI credentials from environment variables."""
        self.email = os.getenv("NCBI_EMAIL")
        self.api_key = os.getenv("NCBI_API_KEY")
        self.logger = logger

        if not self.email:
            raise ValueError("NCBI_EMAIL environment variable is required.")

        Entrez.email = self.email
        if self.api_key:
            Entrez.api_key = self.api_key
        else:
            self.logger.warning("NCBI_API_KEY not set. Rate limits may apply.")

    def search(self, query: str, max_results: int = 10) -> List[str]:
        """Search PubMed with a query and return a list of PMIDs.

        Args:
            query (str): The search query for PubMed.
            max_results (int): Maximum number of PMIDs to return (default: 10).

        Returns:
            List[str]: A list of PubMed IDs (PMIDs).

        Raises:
            RuntimeError: If the search fails due to an API error.
        """
        try:
            self.logger.info(f"Searching PubMed with query: '{query}', max_results: {max_results}")
            with Entrez.esearch(db="pubmed", term=query, retmax=max_results, usehistory="y") as handle:
                record = Entrez.read(handle)
            pmids = record.get("IdList", [])
            if not pmids:
                self.logger.warning(f"No results found for query: '{query}'")
            return pmids
        except Exception as e:
            self.logger.error(f"Failed to search PubMed: {str(e)}")
            raise RuntimeError(f"PubMed search failed: {str(e)}")

    def _fetch_batch(self, pmids: List[str]) -> List[Dict]:
        """Fetch details for a batch of PMIDs (internal method).

        Args:
            pmids (List[str]): List of PMIDs to fetch details for.

        Returns:
            List[Dict]: List of dictionaries containing PubMed record details.

        Raises:
            RuntimeError: If fetching details fails.
        """
        try:
            self.logger.info(f"Fetching details for {len(pmids)} PMIDs")
            self.logger.info(f"PMIDs being fetched: {pmids}")
            with Entrez.efetch(db="pubmed", id=",".join(pmids), rettype="medline", retmode="text") as handle:
                records = list(Medline.parse(handle))
            if not records:
                self.logger.warning(f"No details retrieved for {len(pmids)} PMIDs")
            return records
        except Exception as e:
            self.logger.error(f"Failed to fetch details for PMIDs: {str(e)}")
            raise RuntimeError(f"Failed to fetch PubMed details: {str(e)}")

    def fetch_details(self, pmids: List[str], batch_size: int = 200) -> List[Dict]:
        """Fetch detailed records for a list of PMIDs, handling batching if necessary.

        Args:
            pmids (List[str]): List of PMIDs to fetch details for.
            batch_size (int): Number of PMIDs to fetch per batch (default: 200).

        Returns:
            List[Dict]: List of dictionaries containing PubMed record details.
        """
        if not pmids:
            return []

        records = []
        if len(pmids) > batch_size:
            self.logger.info(f"Fetching {len(pmids)} PMIDs in batches of {batch_size}")
            for i in range(0, len(pmids), batch_size):
                batch_pmids = pmids[i:i + batch_size]
                records.extend(self._fetch_batch(batch_pmids))
        else:
            records = self._fetch_batch(pmids)
        return records