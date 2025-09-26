# FinPulse - Financial Sentiment Analyzer

FinPulse is a comprehensive financial sentiment analysis system that aggregates and analyzes sentiment from financial news articles and Reddit posts, providing actionable insights into market sentiment trends.

## 🚀 Features

- **Data Collection**: Automated scraping of 100,000+ financial news articles and Reddit posts
- **Sentiment Analysis**: Advanced NLP models for quantifying sentiment signals
- **REST API**: FastAPI-powered endpoints for data access
- **GraphQL**: Flexible query interface for complex data retrieval
- **Interactive Dashboards**: Power BI visualizations of sentiment trends vs market movements
- **Data Validation**: Pydantic models for robust data handling

## 🛠 Technology Stack

- **Backend**: Python, FastAPI, SQLAlchemy
- **Database**: PostgreSQL/SQLite
- **Data Processing**: Pandas, NumPy
- **Web Scraping**: BeautifulSoup, Requests
- **NLP**: VADER, TextBlob, Transformers
- **Data Validation**: Pydantic
- **API**: REST (FastAPI) + GraphQL
- **Visualization**: Power BI
- **Version Control**: Git

## 📁 Project Structure

```
finpulse/
├── finpulse/
│   ├── api/          # FastAPI REST and GraphQL endpoints
│   ├── data/         # Data processing and cleaning utilities
│   ├── models/       # SQLAlchemy database models
│   ├── scrapers/     # Web scraping modules
│   ├── sentiment/    # NLP and sentiment analysis
│   └── utils/        # Utility functions
├── tests/            # Unit and integration tests
├── docs/             # Documentation
├── config/           # Configuration files
└── requirements.txt  # Python dependencies
```

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/aadheeshn26/finpulse.git
cd finpulse
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

Coming soon...

## 📊 Dashboard Access

Detailed instructions for accessing Power BI dashboards externally will be provided in the setup guide.

## 🤝 Contributing

This project is part of a technical demonstration. For questions or suggestions, please open an issue.

## 📝 License

This project is licensed under the MIT License.