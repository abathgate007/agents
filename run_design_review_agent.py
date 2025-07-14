import os
import asyncio
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from dotenv import load_dotenv
from config import load_config
from design import Design
from design_parser import DesignParser
from diagram_to_mermaid_converter import DiagramToMermaidConverter
from security_design_reviewer import SecurityDesignReviewer
from llm_model import LLMModel
from evaluated_output import EvaluatedOutput
import config  # Assumes you have a config.py defining openai_api_key, etc.

def get_file(title, filetypes):
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(title=title, filetypes=filetypes)

def select_files():
    print("🔐 Security Design Review Agent")
    print("-------------------------------")

    # Prompt for requirements doc
    req_path = get_file("Select Requirements Document", [
        ("Design Documents", "*.pdf *.docx *.txt"),
        ("All Files", "*.*")
    ])

    if not req_path or not Path(req_path).exists():
        print("❌ No valid requirements document selected. Exiting.")
        return None, None

    # Prompt for optional architecture
    arch_path = get_file("Select Optional Architecture Diagram or Mermaid File", [
        ("Architecture or Mermaid", "*.png *.jpg *.jpeg *.mmd *.txt"),
        ("All Files", "*.*")
    ])

    return req_path, arch_path if arch_path and Path(arch_path).exists() else None

def build_models():
    return [
        LLMModel(model_name="gpt-4o", api_key=config.openai_api_key, model_type="openai"),
        LLMModel(model_name="deepseek-chat", api_key=config.deepseek_api_key, base_url="https://api.deepseek.com/v1", model_type="openai"),
        LLMModel(model_name="claude-3-7-sonnet-latest", api_key=config.anthropic_api_key, model_type="anthropic"),
        LLMModel(model_name="gemini-2.0-flash", api_key=config.google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/", model_type="google"),
        LLMModel(model_name="llama-3.3-70b-versatile", api_key=config.groq_api_key, base_url="https://api.groq.com/openai/v1", model_type="openai")
    ]

async def run_review(req_path: str, arch_path: str):
    design = Design()

    # Add requirements text
    try:
        with open(req_path, "rb") as f:
            parser = DesignParser(file_obj=f, filename=req_path)
            text = parser.parse()
            design.add_text(text)
            print("✅ Requirements parsed and added.")
    except Exception as e:
        print(f"❌ Error parsing requirements: {e}")
        return

    # Optional: add mermaid diagram
    if arch_path:
        ext = Path(arch_path).suffix.lower()
        try:
            if ext in [".png", ".jpg", ".jpeg"]:
                converter = DiagramToMermaidConverter()
                mermaid = converter.convert(image_path=arch_path, output_path="output.mmd")
                if mermaid:
                    design.add_mermaid(mermaid)
                    print("✅ Mermaid diagram added from image.")
            elif ext in [".mmd", ".txt"]:
                with open(arch_path, "r", encoding="utf-8") as f:
                    design.add_mermaid(f.read())
                    print("✅ Mermaid diagram loaded from file.")
            else:
                print(f"⚠️ Unsupported file type: {ext}")
        except Exception as e:
            print(f"❌ Error processing architecture file: {e}")

    models = build_models()
    reviewer = SecurityDesignReviewer(models=models)

    print("\n⏳ Running security design review...")
    try:
        result: EvaluatedOutput = await reviewer.review(design)
        print("\n✅ Security Review Results:\n")
        print(result)
    except Exception as e:
        print(f"❌ Review failed: {e}")

if __name__ == "__main__":
    load_dotenv()
    config = load_config()
    req_path, arch_path = select_files()
    if req_path:
        asyncio.run(run_review(req_path, arch_path))
