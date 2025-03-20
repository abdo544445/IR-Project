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

- **IR System**
  - Document indexing using Apache Lucene
  - Multiple analyzer options (Standard, Whitespace, English)
  - Different similarity models (VSM, BM25)
  - Query processing and result evaluation
  - Performance metrics calculation (Precision, Recall, MAP)

## 🛠️ Technology Stack

### Java Application
- Java 8 or higher
- Apache Lucene for indexing and searching
- Maven for dependency management
- JUnit for testing

### Python Web Crawler
- Python 3.6 or higher
- BeautifulSoup4 for HTML parsing
- Requests for HTTP requests
- Concurrent processing for efficient crawling

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Java JDK 8 or higher
- Python 3.6 or higher
- Maven 3.8 or higher
- Git (for cloning the repository)

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

### Running with Java Integration

Run crawler and Java application together:
```bash
python run_crawler.py --urls https://arxiv.org/list/cs.IR/recent --max-pages 50 --run-java
```

### Running Java Application Manually

```bash
mvn clean compile exec:java -Dexec.mainClass=IR.App
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

## 📊 Performance Metrics

The system evaluates search results using:
- Precision@25
- Recall
- Mean Average Precision (MAP)

## 🔄 Recent Updates

### Java Application Updates
- Added automatic creation of results directory
- Improved error handling
- Enhanced evaluation metrics

## 🐛 Troubleshooting

### Common Issues
1. **Missing Files**
   - Check output directory for crawler results
   - Verify file permissions

2. **Java Application Errors**
   - Ensure Maven dependencies are installed
   - Check Java version compatibility

3. **Crawler Issues**
   - Review crawler.log for detailed error messages
   - Check network connectivity
   - Verify URL accessibility

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Apache Lucene team for the excellent IR framework
- BeautifulSoup4 and Requests libraries for web scraping capabilities
- The academic community for providing open access to research papers 