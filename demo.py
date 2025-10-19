#!/usr/bin/env python3
"""
Demo script showing eCourts Scraper functionality with mock data
"""

import json
from datetime import datetime
from ecourts_scraper import ECourtsScraper

class MockECourtsScraper(ECourtsScraper):
    """Mock version for demonstration"""
    
    def _parse_case_response(self, response):
        """Return mock successful response"""
        return {
            'case_found': True,
            'cnr': 'DLCT01-123456-2024',
            'case_details': {
                'case_type': 'CC',
                'case_number': '123',
                'year': '2024',
                'parties': 'State vs Rahul Verma',
                'court': 'District Court Delhi'
            },
            'listing_info': self._check_listing_dates()
        }
    
    def search_case_by_cnr(self, cnr):
        """Mock CNR search"""
        print(f"[MOCK] Searching CNR: {cnr}")
        return self._parse_case_response(None)
    
    def search_case_by_details(self, case_type, case_number, year, state_code='', dist_code=''):
        """Mock case details search"""
        print(f"[MOCK] Searching case: {case_type}/{case_number}/{year}")
        return self._parse_case_response(None)

def demo():
    print("=== eCourts Scraper Demo ===\n")
    
    scraper = MockECourtsScraper()
    
    # Demo 1: CNR Search
    print("1. CNR Search Demo:")
    result = scraper.search_case_by_cnr("DLCT01-123456-2024")
    print(json.dumps(result, indent=2))
    
    # Demo 2: Case Details Search
    print("\n2. Case Details Search Demo:")
    result = scraper.search_case_by_details("CC", "123", "2024")
    print(json.dumps(result, indent=2))
    
    # Demo 3: Cause List Download
    print("\n3. Cause List Download Demo:")
    causelist = scraper.download_cause_list()
    print(json.dumps(causelist, indent=2))
    
    # Demo 4: PDF Download
    print("\n4. PDF Download Demo:")
    pdf_result = scraper.download_case_pdf("demo_case")
    print(json.dumps(pdf_result, indent=2))
    
    print("\n=== Demo Complete ===")
    print("Files generated:")
    print("- cause_list_*.json")
    print("- case_demo_case_*.pdf")

if __name__ == "__main__":
    demo()