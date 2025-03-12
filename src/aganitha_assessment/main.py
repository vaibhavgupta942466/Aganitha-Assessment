import click
from aganitha_assessment.logger import setup_logging
from aganitha_assessment.writer import CSVWriter
from aganitha_assessment.fetcher import PubMedFetcher
from aganitha_assessment.mapper import PaperMapper


class CLI:
    """Command Line Interface for fetching papers from PubMed.

    This class encapsulates the setup and execution of a Click-based CLI
    to fetch and process PubMed papers based on user input.
    """

    def __init__(self):
        """Initialize the CLI with a Click CommandCollection."""
        self.cli = click.CommandCollection(sources=[cli])

    def run(self):
        """Execute the CLI command."""
        self.cli()


@click.command()
@click.option(
    "--query",
    "-q",
    required=True,
    help="PubMed search query (e.g., 'cancer treatment')",
)
@click.option(
    "--debug",
    "-d",
    is_flag=True,
    help="Enable debug logging to the console during execution",
)
@click.option(
    "--file",
    "-f",
    default="output.csv",
    help="Name of the CSV file to append the data (default: output.csv)",
)
@click.option(
    "--max-results",
    "-mr",
    default=10,
    type=int,
    help="Maximum number of results to fetch",
)
def cli(query: str, max_results: int, file: str, debug: bool) -> None:
    """Fetch papers from PubMed and append results to a CSV file.

    This command searches PubMed using the provided query, retrieves up to
    the specified number of results, maps them to a structured format, and
    appends them to a CSV file. Logging is configured based on the debug flag.

    Args:
        query (str): The search query for PubMed (e.g., 'cancer treatment').
        max_results (int): The maximum number of results to fetch.
        file (str): The name of the CSV file to append the data to.
        debug (bool): Whether to enable debug-level logging.

    Raises:
        Exception: If an error occurs during fetching, mapping, or writing.
    """
    # Set up logging
    logger = setup_logging(debug, query)
    logger.info(f"Starting PubMed fetch for query: {query}")

    try:
        # Initialize fetcher and mapper
        fetcher = PubMedFetcher(logger)
        mapper = PaperMapper(logger)

        # Search for PubMed IDs (PMIDs)
        logger.info("Searching PubMed...")
        pmids = fetcher.search(query, max_results)
        if not pmids:
            logger.warning("No papers found for the given query.")
            return

        # Fetch detailed records for the PMIDs
        logger.info(f"Fetching details for {len(pmids)} papers...")
        records = fetcher.fetch_details(pmids)
        if not records:
            logger.warning("No details fetched for the given PMIDs.")
            return

        # Map records to the desired format
        logger.info("Mapping fetched records...")
        papers = mapper.map_records(records)

        # Write the mapped papers to the CSV file
        logger.info(f"Writing {len(papers)} papers to {file}")
        CSVWriter(file, logger).write_papers(papers)
        logger.info("Process completed successfully.")

    except Exception as e:
        logger.error(f"Error in CLI execution: {str(e)}")
        raise  # Propagate the exception for debugging or higher-level handling


if __name__ == "__main__":
    # For direct execution, use the CLI class
    CLI().run()
