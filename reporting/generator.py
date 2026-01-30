from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os
import datetime

class ReportGenerator:
    def __init__(self, template_dir="reporting/templates"):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def generate(self, steps, output_dir="."):
        template = self.env.get_template("report.html")
        
        # Prepare context
        context = {
            "steps": steps,
            "generation_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        html_content = template.render(context)
        
        # Save HTML
        html_path = os.path.join(output_dir, "report.html")
        with open(html_path, "w") as f:
            f.write(html_content)
        print(f"HTML Report saved to {html_path}")

        # Save PDF
        pdf_path = os.path.join(output_dir, "report.pdf")
        HTML(string=html_content, base_url=output_dir).write_pdf(pdf_path)
        print(f"PDF Report saved to {pdf_path}")
        
        return html_path, pdf_path
