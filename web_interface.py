#!/usr/bin/env python3
"""
Simple web interface for eCourts Scraper (Bonus feature)
"""

from flask import Flask, request, jsonify, render_template_string
from ecourts_scraper import ECourtsScraper
import json

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>eCourts Scraper - India Court Listings</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(45deg, #1e3c72, #2a5298);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 1.1em; }
        .content { padding: 40px; }
        .form-group { margin: 25px 0; }
        .form-group label { 
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        input, select {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        .checkbox-group {
            display: flex;
            align-items: center;
            margin: 15px 0;
        }
        .checkbox-group input[type="checkbox"] {
            width: auto;
            margin-right: 10px;
        }
        .button-group {
            display: flex;
            gap: 15px;
            margin-top: 30px;
        }
        button {
            flex: 1;
            padding: 15px 25px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-primary {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
        }
        .btn-secondary {
            background: linear-gradient(45deg, #f093fb, #f5576c);
            color: white;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        .result {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            padding: 30px;
            margin: 30px 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            min-height: 400px;
            max-height: 600px;
            overflow-y: auto;
        }
        .error {
            background: #fee;
            border-color: #fcc;
            color: #c33;
        }
        .success {
            background: #efe;
            border-color: #cfc;
            color: #363;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .feature-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 2px solid transparent;
            transition: all 0.3s;
        }
        .feature-card:hover {
            border-color: #667eea;
            transform: translateY(-5px);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚖️ eCourts Scraper</h1>
            <p>Search Indian Court Cases & Download Cause Lists</p>
        </div>
        
        <div class="content">
            <div class="feature-grid">
                <div class="feature-card">
                    <h3>🔍 Case Search</h3>
                    <p>Search by CNR or case details</p>
                </div>
                <div class="feature-card">
                    <h3>📅 Listing Check</h3>
                    <p>Check today/tomorrow listings</p>
                </div>
                <div class="feature-card">
                    <h3>📄 PDF Download</h3>
                    <p>Download case documents</p>
                </div>
                <div class="feature-card">
                    <h3>📋 Cause Lists</h3>
                    <p>Download daily cause lists</p>
                </div>
            </div>
            
            <form id="searchForm">
                <div class="form-group">
                    <label>🔍 Search Method:</label>
                    <select id="searchMethod" onchange="toggleFields()">
                        <option value="cnr">CNR Number</option>
                        <option value="details">Case Details</option>
                    </select>
                </div>
                
                <div class="form-group" id="cnrField">
                    <label>📋 CNR Number:</label>
                    <input type="text" id="cnr" placeholder="e.g., DLCT01-123456-2024">
                </div>
                
                <div id="detailsFields" style="display:none;">
                    <div class="form-group">
                        <label>⚖️ Case Type:</label>
                        <input type="text" id="caseType" placeholder="e.g., CC, CRL, CIV">
                    </div>
                    <div class="form-group">
                        <label>🔢 Case Number:</label>
                        <input type="text" id="caseNumber" placeholder="e.g., 123">
                    </div>
                    <div class="form-group">
                        <label>📅 Year:</label>
                        <input type="text" id="year" placeholder="e.g., 2024">
                    </div>
                </div>
                
                <div class="checkbox-group">
                    <input type="checkbox" id="downloadPdf">
                    <label>📄 Download PDF (if available)</label>
                </div>
                
                <div class="button-group">
                    <button type="button" class="btn-primary" onclick="searchCase()">🔍 Search Case</button>
                    <button type="button" class="btn-secondary" onclick="downloadCauseList()">📋 Download Cause List</button>
                </div>
            </form>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Processing your request...</p>
            </div>
    
            <div id="result"></div>
        </div>
    </div>
    
    <script>
        function toggleFields() {
            const method = document.getElementById('searchMethod').value;
            document.getElementById('cnrField').style.display = method === 'cnr' ? 'block' : 'none';
            document.getElementById('detailsFields').style.display = method === 'details' ? 'block' : 'none';
        }
        
        async function searchCase() {
            const method = document.getElementById('searchMethod').value;
            const data = { method };
            
            if (method === 'cnr') {
                const cnr = document.getElementById('cnr').value.trim();
                if (!cnr) {
                    displayResult({ error: 'Please enter a CNR number' });
                    return;
                }
                data.cnr = cnr;
            } else {
                const caseType = document.getElementById('caseType').value.trim();
                const caseNumber = document.getElementById('caseNumber').value.trim();
                const year = document.getElementById('year').value.trim();
                
                if (!caseType || !caseNumber || !year) {
                    displayResult({ error: 'Please fill all case details' });
                    return;
                }
                
                data.case_type = caseType;
                data.case_number = caseNumber;
                data.year = year;
            }
            
            data.download_pdf = document.getElementById('downloadPdf').checked;
            
            showLoading(true);
            
            try {
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                displayResult(result);
            } catch (error) {
                displayResult({ error: 'Request failed: ' + error.message });
            } finally {
                showLoading(false);
            }
        }
        
        async function downloadCauseList() {
            showLoading(true);
            
            try {
                const response = await fetch('/api/causelist', { method: 'POST' });
                const result = await response.json();
                displayResult(result);
            } catch (error) {
                displayResult({ error: 'Request failed: ' + error.message });
            } finally {
                showLoading(false);
            }
        }
        
        function showLoading(show) {
            document.getElementById('loading').style.display = show ? 'block' : 'none';
            document.getElementById('result').style.display = show ? 'none' : 'block';
        }
        
        function displayResult(result) {
            const resultDiv = document.getElementById('result');
            
            if (result.error) {
                resultDiv.innerHTML = `
                    <div class="result error">
                        <h2 style="color: #d32f2f; margin-bottom: 20px;">❌ Error Occurred</h2>
                        <div style="background: white; padding: 20px; border-radius: 8px; border-left: 4px solid #d32f2f;">
                            <p style="font-size: 18px; margin: 0;">${result.error}</p>
                        </div>
                    </div>`;
                return;
            }
            
            let html = '<div class="result success">';
            
            if (result.case_found) {
                html += '<h2 style="color: #2e7d32; margin-bottom: 25px; font-size: 24px;">✅ Case Search Results</h2>';
                
                if (result.case_details) {
                    html += `
                        <div style="background: white; padding: 25px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                            <h3 style="color: #1976d2; margin-bottom: 15px; font-size: 20px;">📋 Case Information</h3>
                            <div style="display: grid; gap: 12px;">
                                <div style="display: flex; padding: 10px; background: #f5f5f5; border-radius: 6px;">
                                    <span style="font-weight: bold; width: 120px; color: #555;">Case Number:</span>
                                    <span style="font-size: 18px; color: #1976d2;">${result.case_details.case_type}/${result.case_details.case_number}/${result.case_details.year}</span>
                                </div>
                                <div style="display: flex; padding: 10px; background: #f5f5f5; border-radius: 6px;">
                                    <span style="font-weight: bold; width: 120px; color: #555;">Parties:</span>
                                    <span style="font-size: 18px;">${result.case_details.parties}</span>
                                </div>
                                <div style="display: flex; padding: 10px; background: #f5f5f5; border-radius: 6px;">
                                    <span style="font-weight: bold; width: 120px; color: #555;">Court:</span>
                                    <span style="font-size: 18px;">${result.case_details.court}</span>
                                </div>
                            </div>
                        </div>`;
                }
                
                if (result.listing_info) {
                    const today = result.listing_info.today;
                    const tomorrow = result.listing_info.tomorrow;
                    
                    html += `
                        <div style="background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                            <h3 style="color: #1976d2; margin-bottom: 20px; font-size: 20px;">📅 Court Listing Status</h3>
                            <div style="display: grid; gap: 15px;">
                                <div style="padding: 15px; border-radius: 8px; ${today.listed ? 'background: #e8f5e8; border-left: 4px solid #4caf50;' : 'background: #fff3e0; border-left: 4px solid #ff9800;'}">
                                    <h4 style="margin: 0 0 10px 0; font-size: 18px;">📅 Today's Listing</h4>
                                    ${today.listed ? 
                                        `<p style="margin: 5px 0; font-size: 16px;"><strong>Status:</strong> <span style="color: #4caf50;">✅ Listed</span></p>
                                         <p style="margin: 5px 0; font-size: 16px;"><strong>Serial Number:</strong> ${today.serial_no}</p>
                                         <p style="margin: 5px 0; font-size: 16px;"><strong>Court Room:</strong> ${today.court_name}</p>` : 
                                        `<p style="margin: 5px 0; font-size: 16px;"><strong>Status:</strong> <span style="color: #ff9800;">❌ Not Listed</span></p>`
                                    }
                                </div>
                                <div style="padding: 15px; border-radius: 8px; ${tomorrow.listed ? 'background: #e8f5e8; border-left: 4px solid #4caf50;' : 'background: #fff3e0; border-left: 4px solid #ff9800;'}">
                                    <h4 style="margin: 0 0 10px 0; font-size: 18px;">📅 Tomorrow's Listing</h4>
                                    ${tomorrow.listed ? 
                                        `<p style="margin: 5px 0; font-size: 16px;"><strong>Status:</strong> <span style="color: #4caf50;">✅ Listed</span></p>
                                         <p style="margin: 5px 0; font-size: 16px;"><strong>Serial Number:</strong> ${tomorrow.serial_no}</p>
                                         <p style="margin: 5px 0; font-size: 16px;"><strong>Court Room:</strong> ${tomorrow.court_name}</p>` : 
                                        `<p style="margin: 5px 0; font-size: 16px;"><strong>Status:</strong> <span style="color: #ff9800;">❌ Not Listed</span></p>`
                                    }
                                </div>
                            </div>
                        </div>`;
                }
            } else if (result.data) {
                html += '<h2 style="color: #2e7d32; margin-bottom: 25px; font-size: 24px;">📋 Cause List Downloaded</h2>';
                html += `
                    <div style="background: white; padding: 25px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                        <h3 style="color: #1976d2; margin-bottom: 15px; font-size: 20px;">📄 Download Information</h3>
                        <div style="display: grid; gap: 12px;">
                            <div style="display: flex; padding: 10px; background: #f5f5f5; border-radius: 6px;">
                                <span style="font-weight: bold; width: 120px; color: #555;">Date:</span>
                                <span style="font-size: 18px;">${result.data.date}</span>
                            </div>
                            <div style="display: flex; padding: 10px; background: #f5f5f5; border-radius: 6px;">
                                <span style="font-weight: bold; width: 120px; color: #555;">Court:</span>
                                <span style="font-size: 18px;">${result.data.court}</span>
                            </div>
                            <div style="display: flex; padding: 10px; background: #f5f5f5; border-radius: 6px;">
                                <span style="font-weight: bold; width: 120px; color: #555;">Total Cases:</span>
                                <span style="font-size: 18px; color: #1976d2; font-weight: bold;">${result.data.cases.length}</span>
                            </div>
                            <div style="display: flex; padding: 10px; background: #f5f5f5; border-radius: 6px;">
                                <span style="font-weight: bold; width: 120px; color: #555;">Saved As:</span>
                                <span style="font-size: 18px; color: #4caf50;">${result.filename}</span>
                            </div>
                        </div>
                    </div>
                    <div style="background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                        <h3 style="color: #1976d2; margin-bottom: 15px; font-size: 20px;">📋 Case List Preview</h3>
                        <div style="max-height: 300px; overflow-y: auto; border: 1px solid #e0e0e0; border-radius: 6px;">
                            <table style="width: 100%; border-collapse: collapse;">
                                <thead style="background: #f5f5f5; position: sticky; top: 0;">
                                    <tr>
                                        <th style="padding: 12px; text-align: left; border-bottom: 1px solid #e0e0e0;">Serial</th>
                                        <th style="padding: 12px; text-align: left; border-bottom: 1px solid #e0e0e0;">Case Number</th>
                                        <th style="padding: 12px; text-align: left; border-bottom: 1px solid #e0e0e0;">Parties</th>
                                    </tr>
                                </thead>
                                <tbody>`;
                
                result.data.cases.forEach((case_item, index) => {
                    html += `
                        <tr style="${index % 2 === 0 ? 'background: #fafafa;' : 'background: white;'}">
                            <td style="padding: 12px; border-bottom: 1px solid #e0e0e0; font-weight: bold; color: #1976d2;">${case_item.serial_no}</td>
                            <td style="padding: 12px; border-bottom: 1px solid #e0e0e0;">${case_item.case_no}</td>
                            <td style="padding: 12px; border-bottom: 1px solid #e0e0e0;">${case_item.parties}</td>
                        </tr>`;
                });
                
                html += `
                                </tbody>
                            </table>
                        </div>
                    </div>`;
            } else {
                html += '<h2 style="color: #2e7d32; margin-bottom: 25px; font-size: 24px;">📄 Search Results</h2>';
                html += `<div style="background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);"><pre style="font-size: 14px; line-height: 1.5; margin: 0; white-space: pre-wrap;">${JSON.stringify(result, null, 2)}</pre></div>`;
            }
            
            html += '</div>';
            resultDiv.innerHTML = html;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/search', methods=['POST'])
def api_search():
    try:
        data = request.get_json()
        scraper = ECourtsScraper()
        
        if data['method'] == 'cnr':
            result = scraper.search_case_by_cnr(data['cnr'])
        else:
            result = scraper.search_case_by_details(
                data['case_type'], data['case_number'], data['year']
            )
        
        if data.get('download_pdf') and 'error' not in result:
            pdf_result = scraper.download_case_pdf("web_case")
            result['pdf_download'] = pdf_result
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/causelist', methods=['POST'])
def api_causelist():
    try:
        scraper = ECourtsScraper()
        result = scraper.download_cause_list()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting eCourts Scraper Web Interface...")
    print("Open http://localhost:5001 in your browser")
    print("eCourts India Case Search & Cause List Downloader")
    print("Features: CNR Search, Case Details, PDF Download, Cause Lists")
    app.run(debug=True, host='0.0.0.0', port=5001)