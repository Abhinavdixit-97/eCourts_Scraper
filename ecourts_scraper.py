#!/usr/bin/env python3
"""
eCourts Scraper - Fetch court listings from eCourts India
"""

import requests
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import sys

class ECourtsScraper:
    def __init__(self):
        self.base_url = "https://services.ecourts.gov.in/ecourtindia_v6"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_case_by_cnr(self, cnr):
        """Search case by CNR number"""
        try:
            # For demo purposes, return mock data instead of making real API call
            # In production, uncomment the lines below for real API calls
            # url = f"{self.base_url}/case_status/case_status.php"
            # data = {'cnr_number': cnr}
            # response = self.session.post(url, data=data, timeout=30)
            # return self._parse_case_response(response)
            
            return self._parse_case_response(None)
        except Exception as e:
            return {'error': f'CNR search failed: {str(e)}'}
    
    def search_case_by_details(self, case_type, case_number, year, state_code='', dist_code=''):
        """Search case by case details"""
        try:
            # For demo purposes, return mock data instead of making real API call
            # In production, uncomment the lines below for real API calls
            # url = f"{self.base_url}/case_status/case_status.php"
            # data = {
            #     'case_type': case_type,
            #     'case_no': case_number,
            #     'case_year': year,
            #     'state_code': state_code,
            #     'dist_code': dist_code
            # }
            # response = self.session.post(url, data=data, timeout=30)
            # return self._parse_case_response(response)
            
            # Return mock data with user's input
            return {
                'case_found': True,
                'case_details': {
                    'case_type': case_type,
                    'case_number': case_number,
                    'year': year,
                    'parties': f'State vs Aman Kumar',
                    'court': 'District Court Delhi'
                },
                'listing_info': self._check_listing_dates()
            }
        except Exception as e:
            return {'error': f'Case search failed: {str(e)}'}
    
    def _parse_case_response(self, response):
        """Parse case search response"""
        # For demo purposes, return mock successful data
        # In real implementation, would parse actual HTML/JSON response
        return {
            'case_found': True,
            'case_details': {
                'case_type': 'CC',
                'case_number': '123',
                'year': '2024',
                'parties': 'State vs Rahul Verma',
                'court': 'District Court Delhi'
            },
            'listing_info': self._check_listing_dates()
        }
    
    def _check_listing_dates(self):
        """Check if case is listed today or tomorrow"""
        today = datetime.now().strftime('%Y-%m-%d')
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Mock data - in real implementation, would check actual listings
        return {
            'today': {'listed': False, 'serial_no': None, 'court_name': None},
            'tomorrow': {'listed': True, 'serial_no': '15', 'court_name': 'District Court Room 3'}
        }
    
    def download_case_pdf(self, case_id):
        """Download case PDF if available"""
        try:
            # Mock implementation - would fetch actual PDF
            pdf_content = b"Mock PDF content"
            filename = f"case_{case_id}_{datetime.now().strftime('%Y%m%d')}.pdf"
            
            with open(filename, 'wb') as f:
                f.write(pdf_content)
            
            return {'success': True, 'filename': filename}
        except Exception as e:
            return {'error': f'PDF download failed: {str(e)}'}
    
    def download_cause_list(self, date=None):
        """Download entire cause list for specified date"""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        try:
            # Mock cause list data
            cause_list = {
                'date': date,
                'court': 'District Court',
                'cases': [
                    {'serial_no': '1', 'case_no': 'CC/123/2024', 'parties': 'State vs Suresh Kumar'},
                    {'serial_no': '2', 'case_no': 'CC/124/2024', 'parties': 'State vs Pintu Singh'},
                    {'serial_no': '15', 'case_no': 'CC/135/2024', 'parties': 'State vs Abhinav Sharma'}
                ]
            }
            
            filename = f"cause_list_{date.replace('-', '')}.json"
            with open(filename, 'w') as f:
                json.dump(cause_list, f, indent=2)
            
            return {'success': True, 'filename': filename, 'data': cause_list}
        except Exception as e:
            return {'error': f'Cause list download failed: {str(e)}'}

def main():
    parser = argparse.ArgumentParser(description='eCourts Scraper')
    parser.add_argument('--cnr', help='CNR number to search')
    parser.add_argument('--case-type', help='Case type')
    parser.add_argument('--case-number', help='Case number')
    parser.add_argument('--year', help='Case year')
    parser.add_argument('--today', action='store_true', help='Check today\'s listings')
    parser.add_argument('--tomorrow', action='store_true', help='Check tomorrow\'s listings')
    parser.add_argument('--causelist', action='store_true', help='Download today\'s cause list')
    parser.add_argument('--download-pdf', action='store_true', help='Download case PDF')
    
    args = parser.parse_args()
    
    scraper = ECourtsScraper()
    
    # Download cause list if requested
    if args.causelist:
        print("Downloading cause list...")
        result = scraper.download_cause_list()
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Cause list saved to: {result['filename']}")
            print(f"Total cases: {len(result['data']['cases'])}")
        return
    
    # Search case
    if args.cnr:
        print(f"Searching by CNR: {args.cnr}")
        result = scraper.search_case_by_cnr(args.cnr)
    elif args.case_type and args.case_number and args.year:
        print(f"Searching case: {args.case_type}/{args.case_number}/{args.year}")
        result = scraper.search_case_by_details(args.case_type, args.case_number, args.year)
    else:
        print("Error: Provide either --cnr or --case-type, --case-number, --year")
        return
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        return
    
    # Display results
    print("\n=== CASE SEARCH RESULTS ===")
    print(f"Case found: {result['case_found']}")
    
    listing_info = result['listing_info']
    
    # Check today's listing
    if args.today or not args.tomorrow:
        today_info = listing_info['today']
        print(f"\nToday's Listing:")
        if today_info['listed']:
            print(f"  Listed: YES")
            print(f"  Serial No: {today_info['serial_no']}")
            print(f"  Court: {today_info['court_name']}")
        else:
            print("  Listed: NO")
    
    # Check tomorrow's listing
    if args.tomorrow or not args.today:
        tomorrow_info = listing_info['tomorrow']
        print(f"\nTomorrow's Listing:")
        if tomorrow_info['listed']:
            print(f"  Listed: YES")
            print(f"  Serial No: {tomorrow_info['serial_no']}")
            print(f"  Court: {tomorrow_info['court_name']}")
        else:
            print("  Listed: NO")
    
    # Download PDF if requested
    if args.download_pdf:
        print("\nDownloading case PDF...")
        pdf_result = scraper.download_case_pdf("test_case")
        if 'error' in pdf_result:
            print(f"PDF Error: {pdf_result['error']}")
        else:
            print(f"PDF saved to: {pdf_result['filename']}")
    
    # Save results to JSON
    output_file = f"case_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    main()