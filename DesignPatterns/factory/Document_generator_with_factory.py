from abc import ABC, abstractmethod
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# Abstract Product: Defines the interface for document generators
class DocumentGenerator(ABC):
    @abstractmethod
    def generate(self, data: dict, output_path: str) -> None:
        pass

# Concrete Product: PDF Document Generator
class PdfDocumentGenerator(DocumentGenerator):
    def generate(self, data: dict, output_path: str) -> None:
        c = canvas.Canvas(output_path, pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, "Sales Report")
        c.drawString(100, 730, f"Date: {data['date']}")
        c.drawString(100, 710, f"Total Sales: ${data['total_sales']:.2f}")
        c.drawString(100, 690, "Items Sold:")
        y = 670
        for item in data['items']:
            c.drawString(120, y, f"- {item['name']}: {item['quantity']} units at ${item['price']:.2f} each")
            y -= 20
        c.save()
        print(f"PDF document generated at {output_path}")

# Concrete Product: HTML Document Generator
class HtmlDocumentGenerator(DocumentGenerator):
    def generate(self, data: dict, output_path: str) -> None:
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Sales Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        ul { list-style-type: disc; margin-left: 20px; }
    </style>
</head>
<body>
    <h1>Sales Report</h1>
    <p><strong>Date:</strong> {data['date']}</p>
    <p><strong>Total Sales:</strong> ${data['total_sales']:.2f}</p>
    <h3>Items Sold:</h3>
    <ul>
""".format(data=data)
        for item in data['items']:
            html_content += f"        <li>{item['name']}: {item['quantity']} units at ${item['price']:.2f} each</li>\n"
        html_content += """    </ul>
</body>
</html>
"""
        with open(output_path, 'w') as f:
            f.write(html_content)
        print(f"HTML document generated at {output_path}")

# Concrete Product: Plain Text Document Generator
class TextDocumentGenerator(DocumentGenerator):
    def generate(self, data: dict, output_path: str) -> None:
        text_content = f"Sales Report\n"
        text_content += f"Date: {data['date']}\n"
        text_content += f"Total Sales: ${data['total_sales']:.2f}\n"
        text_content += "Items Sold:\n"
        for item in data['items']:
            text_content += f"- {item['name']}: {item['quantity']} units at ${item['price']:.2f} each\n"
        with open(output_path, 'w') as f:
            f.write(text_content)
        print(f"Text document generated at {output_path}")

# Factory: Creates the appropriate document generator
class DocumentGeneratorFactory:
    @staticmethod
    def get_document_generator(doc_type: str) -> DocumentGenerator:
        if doc_type.lower() == "pdf":
            return PdfDocumentGenerator()
        elif doc_type.lower() == "html":
            return HtmlDocumentGenerator()
        elif doc_type.lower() == "text":
            return TextDocumentGenerator()
        else:
            raise ValueError(f"Unknown document type: {doc_type}")

# Client code: Generates a document based on user input
def generate_sales_report(data: dict, doc_type: str, output_path: str) -> None:
    try:
        # Get the appropriate document generator from the factory
        generator = DocumentGeneratorFactory.get_document_generator(doc_type)
        # Generate the document
        generator.generate(data, output_path)
    except ValueError as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    # Sample sales report data
    sales_data = {
        "date": "2025-06-11",
        "total_sales": 1500.75,
        "items": [
            {"name": "Laptop", "quantity": 2, "price": 500.00},
            {"name": "Mouse", "quantity": 5, "price": 20.15},
            {"name": "Keyboard", "quantity": 3, "price": 100.00}
        ]
    }

    # Ensure output directory exists
    output_dir = "reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate documents in different formats
    generate_sales_report(sales_data, "pdf", f"{output_dir}/sales_report.pdf")
    generate_sales_report(sales_data, "html", f"{output_dir}/sales_report.html")
    generate_sales_report(sales_data, "text", f"{output_dir}/sales_report.txt")
    generate_sales_report(sales_data, "docx", f"{output_dir}/sales_report.docx")