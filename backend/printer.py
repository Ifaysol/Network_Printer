import os
import win32print
import win32api
import time
import pythoncom
import win32com.client

# Set your printer name (use the local printer name, not the UNC path)
PRINTER_NAME_LOCAL = "HP Laser 103 107 108"

def print_file(file_path):
    """Prints a file based on its extension (PDF, DOCX, XLSX)"""
    file_extension = file_path.lower().split(".")[-1]
    
    if file_extension == "pdf":
        print_pdf(file_path)
    elif file_extension in ["docx", "doc"]:
        print_word(file_path)
    elif file_extension in ["xlsx", "xls"]:
        print_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def print_pdf(file_path):
    """Print PDF file using default PDF viewer and send to specific printer"""
    try:
        # Using "printto" ensures the file goes to the specified printer.
        win32api.ShellExecute(0, "printto", file_path, f'"{PRINTER_NAME_LOCAL}"', ".", 0)
    except Exception as e:
        raise Exception(f"Error printing PDF: {e}")

def print_word(file_path):
    """Print Word document using MS Word and send to specific printer"""
    try:
        pythoncom.CoInitialize()
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0  # Disable dialogs

        # Hardcode the ActivePrinter string once you know your printer’s port.
        # For example, if your printer port is "Ne01:", then:
        active_printer = "HP Laser 103 107 108 on Ne01:"  # Replace "Ne01:" with your actual port

        word.ActivePrinter = active_printer

        # Open the document in read-only mode.
        doc = word.Documents.Open(os.path.abspath(file_path), ReadOnly=True)
        time.sleep(2)  # Wait a moment for the document to fully load
        # Force synchronous printing.
        doc.PrintOut(Background=False)
        time.sleep(5)  # Allow time for the print job to be spooled
        doc.Close(False)
        word.Quit()
    except Exception as e:
        raise Exception(f"Error printing Word file: {e}")

def print_excel(file_path):
    """Print Excel file using MS Excel and send to specific printer"""
    try:
        pythoncom.CoInitialize()
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        workbook = excel.Workbooks.Open(os.path.abspath(file_path))
        workbook.PrintOut(ActivePrinter=PRINTER_NAME_LOCAL)
        time.sleep(5)  # Wait for the print job to spool.
        workbook.Close(False)
        excel.Quit()
    except Exception as e:
        raise Exception(f"Error printing Excel file: {e}")