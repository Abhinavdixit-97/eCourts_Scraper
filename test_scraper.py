#!/usr/bin/env python3
"""
Test script for eCourts Scraper
"""

from ecourts_scraper import ECourtsScraper
import json

def test_scraper():
    print("Testing eCourts Scraper...")
    
    scraper = ECourtsScraper()
    
    # Test CNR search
    print("\n1. Testing CNR search...")
    result = scraper.search_case_by_cnr("DLCT01-123456-2024")
    print(f"CNR Search Result: {json.dumps(result, indent=2)}")
    
    # Test case details search
    print("\n2. Testing case details search...")
    result = scraper.search_case_by_details("CC", "123", "2024")
    print(f"Details Search Result: {json.dumps(result, indent=2)}")
    
    # Test PDF download
    print("\n3. Testing PDF download...")
    pdf_result = scraper.download_case_pdf("test_case")
    print(f"PDF Download Result: {json.dumps(pdf_result, indent=2)}")
    
    # Test cause list download
    print("\n4. Testing cause list download...")
    causelist_result = scraper.download_cause_list()
    print(f"Cause List Result: {json.dumps(causelist_result, indent=2)}")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_scraper()