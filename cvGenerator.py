import json
import subprocess
import os
import yaml
from pathlib import Path
from datetime import date
import sys
import argparse

def generate_pdf(cv="default", design="default", language="en", output_pdf="cv.pdf"):
    output_yaml="cv.yaml"
    with open(f"CVs/{cv}/base.json", encoding="utf-8") as f:
        data = json.load(f)
    with open(f"Designs/{design}.json", encoding="utf-8") as f:
        design = json.load(f)
    with open(f"CVs/{cv}/Lang/{language}.json", encoding="utf-8") as f:
        loaded_sections = json.load(f)
    with open(f"Lang/{language}.json", encoding="utf-8") as f:
        lang = json.load(f)
    sections = {}
    for data_section in data.get("sections", []):
        if data_section in loaded_sections:
            sections[loaded_sections[data_section]["title"]] = loaded_sections[data_section]["entries"]
    data["sections"] = sections
    output = {"cv": data, "design": design, "rendercv_settings": {"date": date.today()}, "locale": lang}
    with open(output_yaml, "w", encoding="utf-8") as f:
        yaml.dump(output, f, allow_unicode=True)
    
    subprocess.run(["rendercv", "render", output_yaml, "-o", output_pdf], check=True)
    os.remove(output_yaml)
    print(f"PDF generado: {output_pdf}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generar CV en PDF")
    parser.add_argument("--cv", default="default", help="Nombre del CV")
    parser.add_argument("--design", default="default", help="Nombre del diseño")
    parser.add_argument("--language", default="en", help="Idioma")
    parser.add_argument("--output", default="cv.pdf", help="Nombre del archivo PDF de salida")
    args = parser.parse_args()
    generate_pdf(
        cv=args.cv,
        design=args.design,
        language=args.language,
        output_pdf=args.output
    )

