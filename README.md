# eCourts Scraper

A Python script to fetch court listings from [eCourts India](https://services.ecourts.gov.in/ecourtindia_v6/).

## Features

- Search cases by CNR number or case details (type/number/year)
- Check if case is listed today or tomorrow
- Display serial number and court name for listed cases
- Download case PDFs (when available)
- Download entire cause list for today
- Save results as JSON files
- Command-line interface with multiple options

## Setup

1. Install Python 3.7+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Demo

Run the demo with mock data to see functionality:
```bash
python demo.py
```

## Web Interface (Bonus)

1. Install web dependencies:
   ```bash
   pip install -r requirements_web.txt
   ```
2. Start web server:
   ```bash
   python web_interface.py
   ```
3. Open http://localhost:5001 in browser

## Usage

### Search by CNR
```bash
python ecourts_scraper.py --cnr "DLCT01-123456-2024"
```

### Search by Case Details
```bash
python ecourts_scraper.py --case-type "CC" --case-number "123" --year "2024"
```

### Check Specific Days
```bash
# Check only today's listings
python ecourts_scraper.py --cnr "DLCT01-123456-2024" --today

# Check only tomorrow's listings
python ecourts_scraper.py --cnr "DLCT01-123456-2024" --tomorrow
```

### Download Options
```bash
# Download case PDF
python ecourts_scraper.py --cnr "DLCT01-123456-2024" --download-pdf

# Download today's cause list
python ecourts_scraper.py --causelist
```

## Output

- Console display of case information and listing status
- JSON files with detailed results
- PDF files for cases (when available)
- Cause list JSON files

## Files Generated

- `case_result_YYYYMMDD_HHMMSS.json` - Case search results
- `cause_list_YYYYMMDD.json` - Daily cause list
- `case_CASEID_YYYYMMDD.pdf` - Case PDF documents

## Error Handling

The script handles:
- Network timeouts and connection errors
- Invalid case numbers or CNR formats
- Missing case information
- PDF download failures
- API response parsing errors

## Note

This is a basic implementation. The actual eCourts website may require:
- Session management and cookies
- CAPTCHA solving
- State/district code selection
- HTML parsing for real data extraction

For production use, additional features needed:
- Proper HTML/JSON response parsing
- Session persistence
- Rate limiting
- Retry mechanisms
- Better error handling