# IR Project with Web Crawler Integration

[![Java](https://img.shields.io/badge/Java-8-red.svg)](https://www.oracle.com/java/)
[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![Maven](https://img.shields.io/badge/Maven-3.8+-green.svg)](https://maven.apache.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This project implements an Information Retrieval (IR) system with a web crawler integration. It combines a Java-based IR application using Apache Lucene with a Python web crawler to collect and index academic papers from the internet.

## 🌟 Features

- **Web Crawler**
  - Fetches academic papers from specified URLs
  - Extracts title, author, and content
  - Formats documents in Cranfield format
  - Generates sample queries and relevance judgments
  - Concurrent processing for efficient crawling
  - Configurable crawling parameters
  - Automatic error handling and retry mechanisms

- **IR System**
  - Document indexing using Apache Lucene
  - Multiple analyzer options (Standard, Whitespace, English)
  - Different similarity models (VSM, BM25)
  - Query processing and result evaluation
  - Performance metrics calculation (Precision, Recall, MAP)
  - Support for custom query formats
  - Configurable search parameters

## 🏗️ Architecture Overview

### System Components
1. **Web Crawler (Python)**
   - URL Manager: Handles URL queue and visited URLs
   - Content Extractor: Parses HTML and extracts relevant information
   - Document Formatter: Converts content to Cranfield format
   - Query Generator: Creates sample queries from documents

2. **IR System (Java)**
   - Document Indexer: Creates and manages Lucene index
   - Query Processor: Handles query parsing and execution
   - Result Evaluator: Calculates performance metrics
   - Report Generator: Creates detailed evaluation reports

### Data Flow
1. Crawler fetches documents from web
2. Documents are formatted in Cranfield format
3. Formatted documents are indexed by Lucene
4. Queries are processed against the index
5. Results are evaluated and reported

## 🛠️ Technology Stack

### Java Application
- Java 8 or higher
- Apache Lucene for indexing and searching
- Maven for dependency management
- JUnit for testing
- Log4j for logging
- Apache Commons for utility functions

### Python Web Crawler
- Python 3.6 or higher
- BeautifulSoup4 for HTML parsing
- Requests for HTTP requests
- Concurrent processing for efficient crawling
- Logging module for detailed tracking
- JSON for data storage

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Java JDK 8 or higher
- Python 3.6 or higher
- Maven 3.8 or higher
- Git (for cloning the repository)
- At least 2GB of free disk space
- Internet connection for web crawling

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/abdo544445/IR-Project.git
   cd IR-Project
   ```

2. Set up Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   .\venv\Scripts\activate  # On Windows
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Java dependencies:
   ```bash
   mvn clean install
   ```

## 💻 Usage

### Running the Web Crawler

Run the crawler independently:
```bash
python web_crawler.py --urls https://arxiv.org/list/cs.IR/recent --max-pages 50
```

#### Crawler Options
- `--urls`: Starting URLs (space-separated)
- `--output`: Output directory (default: src/main/resources/crawled)
- `--max-pages`: Maximum pages to crawl (default: 100)
- `--delay`: Request delay in seconds (default: 1.0)
- `--workers`: Concurrent workers (default: 5)
- `--timeout`: Request timeout in seconds (default: 10)
- `--retries`: Number of retry attempts (default: 3)

### Running with Java Integration

Run crawler and Java application together:
```bash
python run_crawler.py --urls https://arxiv.org/list/cs.IR/recent --max-pages 50 --run-java
```

### Running Java Application Manually

```bash
mvn clean compile exec:java -Dexec.mainClass=IR.App
```

### Example Usage

1. **Basic Crawling**
   ```bash
   python web_crawler.py --urls https://arxiv.org/list/cs.IR/recent --max-pages 10
   ```

2. **Advanced Crawling with Custom Settings**
   ```bash
   python web_crawler.py --urls https://arxiv.org/list/cs.IR/recent https://arxiv.org/list/cs.LG/recent --max-pages 20 --delay 2.0 --workers 3
   ```

3. **Full Integration Run**
   ```bash
   python run_crawler.py --urls https://arxiv.org/list/cs.IR/recent --max-pages 50 --run-java
   ```

## 📁 Project Structure

```
IR-Project/
├── src/
│   └── main/
│       ├── java/
│       │   └── IR/
│       │       ├── App.java                 # Main application entry point
│       │       ├── CranQuery.java           # Query parsing and handling
│       │       ├── CreateIndex.java         # Document indexing
│       │       ├── Evaluation.java          # Search result evaluation
│       │       ├── EvaluationMetrics.java   # Evaluation metrics calculation
│       │       ├── QueryIndex.java          # Query processing and results
│       │       └── SearchResult.java        # Search result representation
│       └── resources/
│           ├── cran/                        # Standard Cranfield dataset
│           ├── crawled/                     # Web crawler output
│           └── results/                     # Search results
├── web_crawler.py                          # Main crawler implementation
├── run_crawler.py                          # Integration script
├── requirements.txt                        # Python dependencies
└── pom.xml                                # Maven configuration
```

## 🔧 Configuration

### Java Application
- Analyzer options:
  1. Standard Analyzer
  2. Whitespace Analyzer
  3. English Analyzer

- Similarity methods:
  1. Vector Space Model (VSM)
  2. BM25 Similarity

### Web Crawler
- Customize crawling behavior in `web_crawler.py`
- Adjust output formats in `run_crawler.py`
- Configure logging in `crawler.log`

## 📊 Performance Metrics

The system evaluates search results using:
- Precision@25
- Recall
- Mean Average Precision (MAP)
- NDCG (Normalized Discounted Cumulative Gain)
- F1 Score

### Example Results
```
Evaluation Results:
Precision@25: 0.0400
Recall: 0.2870
Mean Average Precision (MAP): 0.1649
NDCG: 0.2156
F1 Score: 0.0702
```

## 🔄 Recent Updates

### Java Application Updates
- Added automatic creation of results directory
- Improved error handling
- Enhanced evaluation metrics
- Added support for custom analyzers
- Optimized index creation process

### Web Crawler Updates
- Added concurrent processing
- Improved error handling
- Enhanced content extraction
- Added support for multiple URLs
- Optimized memory usage

## 🐛 Troubleshooting

### Common Issues
1. **Missing Files**
   - Check output directory for crawler results
   - Verify file permissions
   - Ensure sufficient disk space

2. **Java Application Errors**
   - Ensure Maven dependencies are installed
   - Check Java version compatibility
   - Verify memory allocation
   - Check index directory permissions

3. **Crawler Issues**
   - Review crawler.log for detailed error messages
   - Check network connectivity
   - Verify URL accessibility
   - Monitor memory usage
   - Check rate limiting

### Debug Mode
Enable debug logging by setting the environment variable:
```bash
export DEBUG=1
python web_crawler.py --urls https://arxiv.org/list/cs.IR/recent
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide for Python code
- Use Google Java Style Guide for Java code
- Write unit tests for new features
- Update documentation for significant changes
- Include example usage in commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Apache Lucene team for the excellent IR framework
- BeautifulSoup4 and Requests libraries for web scraping capabilities
- The academic community for providing open access to research papers
- Contributors and maintainers of all used libraries
- The open-source community for their valuable tools and resources

## 📚 Additional Resources

- [Apache Lucene Documentation](https://lucene.apache.org/core/documentation.html)
- [BeautifulSoup4 Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Python Requests Documentation](https://requests.readthedocs.io/)
- [Maven Documentation](https://maven.apache.org/guides/index.html)
- [Information Retrieval Concepts](https://nlp.stanford.edu/IR-book/) 