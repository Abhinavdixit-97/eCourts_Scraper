#!/usr/bin/env python3
"""
Desktop GUI for eCourts Scraper using tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import json
from datetime import datetime
from ecourts_scraper import ECourtsScraper
import threading

class ECourtGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("⚖️ eCourts Scraper - India Court Search")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.scraper = ECourtsScraper()
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = tk.Label(main_frame, text="⚖️ eCourts Scraper", 
                              font=('Arial', 24, 'bold'), 
                              bg='#f0f0f0', fg='#2c3e50')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        subtitle_label = tk.Label(main_frame, text="Search Indian Court Cases & Download Cause Lists", 
                                 font=('Arial', 12), 
                                 bg='#f0f0f0', fg='#7f8c8d')
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 30))
        
        # Search method frame
        search_frame = ttk.LabelFrame(main_frame, text="🔍 Search Method", padding="15")
        search_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.search_method = tk.StringVar(value="cnr")
        ttk.Radiobutton(search_frame, text="CNR Number", variable=self.search_method, 
                       value="cnr", command=self.toggle_fields).grid(row=0, column=0, padx=(0, 20))
        ttk.Radiobutton(search_frame, text="Case Details", variable=self.search_method, 
                       value="details", command=self.toggle_fields).grid(row=0, column=1)
        
        # CNR frame
        self.cnr_frame = ttk.LabelFrame(main_frame, text="📋 CNR Search", padding="15")
        self.cnr_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(self.cnr_frame, text="CNR Number:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.cnr_entry = ttk.Entry(self.cnr_frame, width=40, font=('Arial', 11))
        self.cnr_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.cnr_entry.insert(0, "DLCT01-123456-2024")
        
        # Case details frame
        self.details_frame = ttk.LabelFrame(main_frame, text="⚖️ Case Details Search", padding="15")
        self.details_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Case details fields
        ttk.Label(self.details_frame, text="Case Type:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.case_type_entry = ttk.Entry(self.details_frame, width=15)
        self.case_type_entry.grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.case_type_entry.insert(0, "CC")
        
        ttk.Label(self.details_frame, text="Case Number:").grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
        self.case_number_entry = ttk.Entry(self.details_frame, width=15)
        self.case_number_entry.grid(row=1, column=1, sticky=tk.W, padx=(0, 10))
        self.case_number_entry.insert(0, "123")
        
        ttk.Label(self.details_frame, text="Year:").grid(row=0, column=2, sticky=tk.W, pady=(0, 5))
        self.year_entry = ttk.Entry(self.details_frame, width=15)
        self.year_entry.grid(row=1, column=2, sticky=tk.W)
        self.year_entry.insert(0, "2024")
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="⚙️ Options", padding="15")
        options_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.download_pdf = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="📄 Download PDF (if available)", 
                       variable=self.download_pdf).grid(row=0, column=0, sticky=tk.W)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=6, column=0, columnspan=2, pady=(0, 20))
        
        search_btn = ttk.Button(buttons_frame, text="🔍 Search Case", 
                               command=self.search_case, style='Accent.TButton')
        search_btn.grid(row=0, column=0, padx=(0, 10))
        
        causelist_btn = ttk.Button(buttons_frame, text="📋 Download Cause List", 
                                  command=self.download_causelist)
        causelist_btn.grid(row=0, column=1, padx=(0, 10))
        
        demo_btn = ttk.Button(buttons_frame, text="🎯 Run Demo", 
                             command=self.run_demo)
        demo_btn.grid(row=0, column=2)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="📊 Results", padding="15")
        results_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        self.results_text = scrolledtext.ScrolledText(results_frame, width=100, height=25, 
                                                     font=('Consolas', 11), wrap=tk.WORD)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(7, weight=2)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        self.toggle_fields()
    
    def toggle_fields(self):
        if self.search_method.get() == "cnr":
            self.cnr_frame.grid()
            self.details_frame.grid_remove()
        else:
            self.cnr_frame.grid_remove()
            self.details_frame.grid()
    
    def update_status(self, message):
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def show_progress(self, show=True):
        if show:
            self.progress.start()
        else:
            self.progress.stop()
    
    def display_result(self, result):
        self.results_text.delete(1.0, tk.END)
        
        if isinstance(result, dict) and 'error' in result:
            self.results_text.insert(tk.END, "❌ ERROR OCCURRED\n")
            self.results_text.insert(tk.END, "=" * 80 + "\n\n")
            self.results_text.insert(tk.END, f"Error Details: {result['error']}\n\n")
            self.results_text.insert(tk.END, "=" * 80 + "\n")
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.results_text.insert(tk.END, "⚖️ eCOURTS SCRAPER RESULTS\n")
        self.results_text.insert(tk.END, "=" * 80 + "\n")
        self.results_text.insert(tk.END, f"🕒 Search completed at: {timestamp}\n\n")
        
        if isinstance(result, dict):
            if result.get('case_found'):
                self.results_text.insert(tk.END, "✅ CASE SEARCH SUCCESSFUL\n")
                self.results_text.insert(tk.END, "-" * 50 + "\n\n")
                
                if 'case_details' in result:
                    details = result['case_details']
                    self.results_text.insert(tk.END, "📋 CASE INFORMATION:\n")
                    self.results_text.insert(tk.END, f"   Case Number    : {details.get('case_type', 'N/A')}/{details.get('case_number', 'N/A')}/{details.get('year', 'N/A')}\n")
                    self.results_text.insert(tk.END, f"   Parties        : {details.get('parties', 'N/A')}\n")
                    self.results_text.insert(tk.END, f"   Court          : {details.get('court', 'N/A')}\n\n")
                
                if 'listing_info' in result:
                    self.results_text.insert(tk.END, "📅 COURT LISTING STATUS:\n")
                    self.results_text.insert(tk.END, "-" * 40 + "\n")
                    listing = result['listing_info']
                    
                    today = listing.get('today', {})
                    self.results_text.insert(tk.END, "📅 TODAY'S LISTING:\n")
                    if today.get('listed'):
                        self.results_text.insert(tk.END, f"   Status         : ✅ LISTED\n")
                        self.results_text.insert(tk.END, f"   Serial Number  : {today.get('serial_no')}\n")
                        self.results_text.insert(tk.END, f"   Court Room     : {today.get('court_name')}\n\n")
                    else:
                        self.results_text.insert(tk.END, "   Status         : ❌ NOT LISTED\n\n")
                    
                    tomorrow = listing.get('tomorrow', {})
                    self.results_text.insert(tk.END, "📅 TOMORROW'S LISTING:\n")
                    if tomorrow.get('listed'):
                        self.results_text.insert(tk.END, f"   Status         : ✅ LISTED\n")
                        self.results_text.insert(tk.END, f"   Serial Number  : {tomorrow.get('serial_no')}\n")
                        self.results_text.insert(tk.END, f"   Court Room     : {tomorrow.get('court_name')}\n\n")
                    else:
                        self.results_text.insert(tk.END, "   Status         : ❌ NOT LISTED\n\n")
            
            elif 'data' in result:  # Cause list
                self.results_text.insert(tk.END, "📋 CAUSE LIST DOWNLOAD SUCCESSFUL\n")
                self.results_text.insert(tk.END, "-" * 50 + "\n\n")
                data = result['data']
                
                self.results_text.insert(tk.END, "📄 DOWNLOAD INFORMATION:\n")
                self.results_text.insert(tk.END, f"   Date           : {data.get('date', 'N/A')}\n")
                self.results_text.insert(tk.END, f"   Court          : {data.get('court', 'N/A')}\n")
                self.results_text.insert(tk.END, f"   Total Cases    : {len(data.get('cases', []))}\n")
                self.results_text.insert(tk.END, f"   Saved As       : {result.get('filename', 'N/A')}\n\n")
                
                self.results_text.insert(tk.END, "📋 CASE LIST PREVIEW:\n")
                self.results_text.insert(tk.END, "-" * 80 + "\n")
                self.results_text.insert(tk.END, f"{'Serial':<8} {'Case Number':<15} {'Parties':<50}\n")
                self.results_text.insert(tk.END, "-" * 80 + "\n")
                
                for case in data.get('cases', []):
                    serial = case.get('serial_no', 'N/A')
                    case_no = case.get('case_no', 'N/A')
                    parties = case.get('parties', 'N/A')
                    if len(parties) > 45:
                        parties = parties[:42] + "..."
                    self.results_text.insert(tk.END, f"{serial:<8} {case_no:<15} {parties:<50}\n")
                
                self.results_text.insert(tk.END, "-" * 80 + "\n")
        
        self.results_text.insert(tk.END, "\n" + "=" * 80 + "\n")
        self.results_text.insert(tk.END, "✅ Operation completed successfully!\n")
        self.results_text.see(tk.END)
    
    def search_case(self):
        def search_thread():
            try:
                self.show_progress(True)
                self.update_status("Searching case...")
                
                if self.search_method.get() == "cnr":
                    cnr = self.cnr_entry.get().strip()
                    if not cnr:
                        messagebox.showerror("Error", "Please enter a CNR number")
                        return
                    result = self.scraper.search_case_by_cnr(cnr)
                else:
                    case_type = self.case_type_entry.get().strip()
                    case_number = self.case_number_entry.get().strip()
                    year = self.year_entry.get().strip()
                    
                    if not all([case_type, case_number, year]):
                        messagebox.showerror("Error", "Please fill all case details")
                        return
                    
                    result = self.scraper.search_case_by_details(case_type, case_number, year)
                
                if self.download_pdf.get() and 'error' not in result:
                    self.update_status("Downloading PDF...")
                    pdf_result = self.scraper.download_case_pdf("gui_case")
                    result['pdf_download'] = pdf_result
                
                self.root.after(0, lambda: self.display_result(result))
                self.root.after(0, lambda: self.update_status("Search completed"))
                
            except Exception as e:
                self.root.after(0, lambda: self.display_result({'error': str(e)}))
                self.root.after(0, lambda: self.update_status("Search failed"))
            finally:
                self.root.after(0, lambda: self.show_progress(False))
        
        threading.Thread(target=search_thread, daemon=True).start()
    
    def download_causelist(self):
        def download_thread():
            try:
                self.show_progress(True)
                self.update_status("Downloading cause list...")
                
                result = self.scraper.download_cause_list()
                
                self.root.after(0, lambda: self.display_result(result))
                self.root.after(0, lambda: self.update_status("Cause list downloaded"))
                
            except Exception as e:
                self.root.after(0, lambda: self.display_result({'error': str(e)}))
                self.root.after(0, lambda: self.update_status("Download failed"))
            finally:
                self.root.after(0, lambda: self.show_progress(False))
        
        threading.Thread(target=download_thread, daemon=True).start()
    
    def run_demo(self):
        # Import and run demo with mock data
        from demo import MockECourtsScraper
        
        def demo_thread():
            try:
                self.show_progress(True)
                self.update_status("Running demo...")
                
                mock_scraper = MockECourtsScraper()
                result = mock_scraper.search_case_by_cnr("DLCT01-123456-2024")
                
                self.root.after(0, lambda: self.display_result(result))
                self.root.after(0, lambda: self.update_status("Demo completed"))
                
            except Exception as e:
                self.root.after(0, lambda: self.display_result({'error': str(e)}))
                self.root.after(0, lambda: self.update_status("Demo failed"))
            finally:
                self.root.after(0, lambda: self.show_progress(False))
        
        threading.Thread(target=demo_thread, daemon=True).start()

def main():
    root = tk.Tk()
    app = ECourtGUI(root)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()