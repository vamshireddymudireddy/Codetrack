# CodeTrack

CodeTrack is a Flask-based web application designed to track and monitor students' CodeChef problem-solving progress. It allows teachers to manage multiple classes and automatically tracks students' progress by scraping their CodeChef profiles.

## Features

- **Multiple Class Management**: Support for multiple classes (CSE_A, CSE_B, CSE_C, etc.)
- **Automated Progress Tracking**: Automatically scrapes and updates students' problem-solving counts from CodeChef
- **Progress Comparison**: Shows previous and recent week statistics for each student
- **Student Performance Metrics**: 
  - Previous week's solved problems
  - Recent week's solved problems
  - Progress count (difference between weeks)
- **Responsive Web Interface**: Clean and user-friendly interface to view and manage student data

## Technical Stack

- **Backend**: Python Flask
- **Database**: SQLite3
- **Web Scraping**: BeautifulSoup4, Requests
- **Data Processing**: Pandas
- **Frontend**: HTML with Bootstrap styling
- **Template Engine**: Jinja2

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/codetrack.git
cd codetrack
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. The application uses SQLite database which will be automatically initialized when you run the application for the first time.
2. Modify the `classes` list in `app.py` to add or remove classes as needed:
```python
classes = ['CSE_A', 'CSE_B', 'CSE_C']
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Access the application through your web browser at `http://localhost:5000`

3. From the homepage, you can:
   - Select a class to view
   - Update scores for a class
   - View detailed scores for each class

## Project Structure

```
codetrack/
├── app.py              # Main Flask application
├── scraper.py         # CodeChef scraping functionality
├── students.db        # SQLite database
├── templates/
│   ├── index.html    # Homepage template
│   └── scores.html   # Score display template
└── requirements.txt   # Project dependencies
```

## Features in Detail

### Web Scraping
- Implements robust scraping with retry mechanisms
- Respects rate limiting with random delays
- Handles various error cases gracefully
- Uses session management for efficient connections

### Database Structure
Each class table contains:
- Student serial number (Primary Key)
- CodeChef username
- Roll number
- Previous week's problem count
- Recent week's problem count
- Progress count

### Error Handling
- Comprehensive error handling for database operations
- Graceful handling of web scraping failures
- User-friendly error messages in the UI

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- CodeChef for providing the platform and user profiles
- Flask community for the excellent web framework
- BeautifulSoup developers for the web scraping capabilities

## Note

This application is designed for educational purposes and includes measures to respect CodeChef's servers through rate limiting and appropriate delays between requests. Please use responsibly.
