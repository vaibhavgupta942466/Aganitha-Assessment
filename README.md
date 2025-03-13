# Aganitha Assessment

## Project Description

The task is to write a Python program to fetch research papers based on a user-specified query. The program must identify papers with at least one author affiliated with a pharmaceutical or biotech company and return the results as a CSV file.

## Table of Contents

- [How the Code is Organized](#how-the-code-is-organized)
- [Installation](#installation)
- [Usage](#usage)
- [Command Line Options](#command-line-options)
- [Tools and Libraries Used](#tools-and-libraries-used)
- [External Tools](#external-tools)
- [License](#license)

## How the Code is Organized

The project is organized into the following structure:

``` Markdown
.
├── .env
├── .gitignore
├── Backend takehome problem.pdf
├── poetry.lock
├── pyproject.toml
├── README.md
├── src/
│   ├── __init__.py
│   └── aganitha_assessment/
│       ├── __init__.py
│       ├── constant.py
│       ├── fetcher.py
│       ├── logger.py
│       ├── main.py
│       ├── mapper.py
│       ├── utils.py
│       └── writer.py
└── tests/
    └── __init__.py
```

### Key Files and Directories

- `src/aganitha_assessment/constant.py`: Contains constants used in the project.
- `src/aganitha_assessment/fetcher.py`: Implements the `PubMedFetcher` class to fetch PubMed data using the Entrez API from Biopython.
- `src/aganitha_assessment/logger.py`: Sets up logging configuration.
- `src/aganitha_assessment/main.py`: Implements the CLI for fetching papers from PubMed.
- `src/aganitha_assessment/mapper.py`: Maps PubMed records to a structured format.
- `src/aganitha_assessment/writer.py`: Writes PubMed paper data to a CSV file.

## Installation

1. Clone the repository:

    ```sh
    git clone <repository-url>
    cd Aganitha-Assessment
    ```

2. Install dependencies using Poetry:

    ```sh
    poetry install
    ```

3. Create a `.env` file in the root directory with the following content:

    ```env
    NCBI_API_KEY=your_ncbi_api_key
    NCBI_EMAIL=your_email@example.com
    DEFAULT_EXECUTION_LOG_FOLDER=logs
    ```

    or you can set the environment variables directly in your sysetm:

    ```sh
    NCBI_API_KEY=your_ncbi_api_key
    NCBI_EMAIL=your_email@example.com
    ```

## Usage

To fetch papers from PubMed and append results to a CSV file, run the following command:

```sh
poetry run get-papers-list --query "your search query" --max-results 10 --file output.csv --debug
```

## Command Line Options

The CLI supports the following options:

- --query or -q: PubMed search query (e.g., 'cancer treatment') (required).
- --debug or -d: Enable debug logging to the console during execution (optional).
- --file or -f: Name of the CSV file to append the data (default: output.csv) (optional).
- --max-results or -mr: Maximum number of results to fetch (default: 10) (optional).

### Tools and Libraries Used

- Biopython: Provides tools for biological computation.
- Click: A package for creating command-line interfaces.
- Python-dotenv: Reads key-value pairs from a .env file and sets them as environment variables.

### External Tools

- Poetry: Used for dependency management and packaging.
- Git: Used for version control.
- GitHub: Used for hosting the project repository.
- Gorko: Used to help in creating folder structure, Explore Poetry, Click documentation, Biopython documentation.
- Github Copilot: Used to help in writing code.

### License

This project is licensed under the MIT License.
