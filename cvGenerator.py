import json
import subprocess
import os
import yaml
from pathlib import Path
from datetime import date

def generate_pdf(cv_file, sections_file, design_file, output_yaml="cv.yaml", output_pdf="cv.pdf"):
    with open(cv_file, encoding="utf-8") as f:
        data = json.load(f)
    with open(design_file, encoding="utf-8") as f:
        design = json.load(f)
    with open(sections_file, encoding="utf-8") as f:
        loaded_sections = json.load(f)
    sections = {}
    for data_section in data.get("sections", []):
        if data_section in loaded_sections:
            sections[data_section] = loaded_sections[data_section]
    data["sections"] = sections
    output = {"cv": data, "design": design, "rendercv_settings": {"date": date.today()}}
    with open(output_yaml, "w", encoding="utf-8") as f:
        yaml.dump(output, f, allow_unicode=True)
    
    subprocess.run(["rendercv", "render", output_yaml, "-o", output_pdf], check=True)

    print(f"PDF generado: {output_pdf}")



if __name__ == "__main__":
    generate_pdf(
        cv_file="cv.json",
        sections_file="sections.json",
        design_file="design.json",
    )
