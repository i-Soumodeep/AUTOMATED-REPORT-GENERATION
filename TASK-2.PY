import csv
from fpdf import FPDF
from datetime import datetime

class PDFReportGenerator:
    def __init__(self, data_file, report_title="Automated Report"):
        self.data_file = data_file
        self.report_title = report_title
        self.data = self._read_data()
        self.analysis = self._analyze_data()
        
    def _read_data(self):
        """Read data from CSV file"""
        try:
            with open(self.data_file, mode='r') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except FileNotFoundError:
            print(f"Error: File '{self.data_file}' not found.")
            return []
        except Exception as e:
            print(f"Error reading file: {e}")
            return []
    
    def _analyze_data(self):
        """Perform basic data analysis"""
        if not self.data:
            return {}
            
        analysis = {
            'record_count': len(self.data),
            'columns': list(self.data[0].keys()) if self.data else [],
            'generation_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Add more analysis as needed
        return analysis
    
    def generate_report(self, output_file="report.pdf"):
        """Generate PDF report"""
        if not self.data:
            print("No data available to generate report")
            return
            
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, self.report_title, ln=1, align='C')
        pdf.ln(10)
        
        # Report metadata
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Generated on: {self.analysis['generation_date']}", ln=1)
        pdf.cell(0, 10, f"Records analyzed: {self.analysis['record_count']}", ln=1)
        pdf.cell(0, 10, f"Columns in dataset: {', '.join(self.analysis['columns'])}", ln=1)
        pdf.ln(15)
        
        # Data summary header
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Data Summary", ln=1)
        pdf.set_font("Arial", '', 12)
        pdf.ln(5)
        
        # Create table header
        col_widths = [40, 40, 40, 40]  # Adjust based on your data
        headers = self.data[0].keys()
        
        pdf.set_font("Arial", 'B', 12)
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, border=1)
        pdf.ln()
        
        # Add data rows (first 10 rows for demo)
        pdf.set_font("Arial", '', 10)
        for row in self.data[:10]:
            for i, header in enumerate(headers):
                pdf.cell(col_widths[i], 10, str(row.get(header, '')), border=1)
            pdf.ln()
        
        # Analysis section
        pdf.ln(15)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Analysis", ln=1)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, "This automated report analyzed the dataset and found the above information. "
                      "The complete dataset contains {} records with {} columns each.".format(
                      self.analysis['record_count'], len(self.analysis['columns'])))
        
        # Save the PDF
        pdf.output(output_file)
        print(f"Report generated successfully: {output_file}")

# Example usage
if __name__ == "__main__":
    # Create sample CSV file if it doesn't exist
    sample_data = [
        ["Name", "Age", "Department", "Salary"],
        ["John Doe", 32, "Marketing", 55000],
        ["Jane Smith", 28, "Engineering", 72000],
        ["Mike Johnson", 45, "HR", 48000],
        ["Sarah Williams", 38, "Engineering", 75000],
        ["David Brown", 29, "Marketing", 52000]
    ]
    
    with open('sample_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(sample_data)
    
    # Generate report
    report = PDFReportGenerator('sample_data.csv', "Employee Data Analysis Report")
    report.generate_report("employee_report.pdf")