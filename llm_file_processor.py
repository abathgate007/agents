"""
llm_file_processor.py

Author: Andrew Bathgate
Date: 2025-07-16

Description:
    Interactive utility to apply a prompt (with placeholders) to every file in a folder tree.
    The prompt can reference both a reusable design review document and per-file code.

    Prompt must contain the following placeholders:
        {DESIGN_REVIEW} will be replaced with the full contents of the selected design review file
        {CODE}          will be replaced with the contents of the current file being reviewed

    Example prompt:
        You are a world-class application security engineer...
        Here is the Design Review: {DESIGN_REVIEW}
        Here is the code: {CODE}
"""

import os
import asyncio
from pathlib import Path
from typing import List, Optional
from tkinter import Tk, filedialog
from dotenv import load_dotenv

from llm_model import LLMModel

class LLMFileProcessor:
    def __init__(self, prompt_text: str, design_review: str, folder_path: str, model: LLMModel):
        self.prompt_template = prompt_text
        self.design_review = design_review
        self.folder_path = Path(folder_path)
        self.model = model

    def _get_all_files(self) -> List[Path]:
        ignored_extensions = {'ico.', '.md', '.css', '.lock', '.txt', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg'}
        ignored_dirs = {'tests', 'test_harness', '__pycache__'}

        files = []
        for p in self.folder_path.rglob("*"):
            if not p.is_file():
                continue

            # Skip if any parent folder starts with '.' or is in ignored_dirs
            if any(part.startswith('.') or part in ignored_dirs for part in p.parts):
                continue

            # Skip if file extension is in ignore list
            if p.suffix.lower() in ignored_extensions:
                continue

            files.append(p)
        print(f"\n📁 Total files to process: {len(files)}")
        for i, f in enumerate(files, 1):
            print(f"{i}: {f}")
        return files

    async def _process_file(self, file_path: Path) -> Optional[str]:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()

            prompt = self.prompt_template.replace("{DESIGN_REVIEW}", self.design_review).replace("{CODE}", code)
            response = await self.model.call(prompt)
            return response
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")
            return None

    async def process_all_files(self) -> List[tuple]:
        files = self._get_all_files()
        results = []
        for i, file_path in enumerate(files, 1):
            print(f"\n🔍 [{i}/{len(files)}] Processing: {file_path}")
            response = await self._process_file(file_path)
            results.append((file_path, response))
            print(f"✅ Result for {file_path}:\n{'-'*40}\n{response or '❌ No response.'}\n")
        return results

    def run(self) -> List[tuple]:
        return asyncio.run(self.process_all_files())

# File/folder selection utils
def select_file(title="Select a File", filetypes=[("Text Files", "*.txt")]) -> Optional[str]:
    root = Tk()
    root.withdraw()
    return filedialog.askopenfilename(title=title, filetypes=filetypes)

def select_folder(title="Select Folder") -> Optional[str]:
    root = Tk()
    root.withdraw()
    return filedialog.askdirectory(title=title)

# Entry point
if __name__ == "__main__":
    load_dotenv()

    prompt_path = select_file("Select Prompt File")
    if not prompt_path:
        print(" Prompt file not selected.")
        exit()

    design_review_path = select_file("Select Design Review File")
    if not design_review_path:
        print(" Design review file not selected.")
        exit()

    folder_path = select_folder("Select Folder to Analyze")
    if not folder_path:
        print(" Folder not selected.")
        exit()

    with open(prompt_path, 'r', encoding='utf-8') as pf:
        prompt_text = pf.read()

    with open(design_review_path, 'r', encoding='utf-8') as df:
        design_review = df.read()

    model = LLMModel(
        model_name="gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY"),
        model_type="openai"
    )

    processor = LLMFileProcessor(prompt_text, design_review, folder_path, model)
    results = processor.run()

    for path, output in results:
        print(f"\n📄 {path}\n{'-'*40}\n{output or ' No response.'}\n")
    # Write results to mitigationreport.txt next to the prompt file
    output_dir = Path(prompt_path).parent
    output_file = output_dir / "mitigationreport.txt"

    with open(output_file, 'w', encoding='utf-8') as f:
        for path, output in results:
            f.write(f"📄 {path}\n")
            f.write("-" * 40 + "\n")
            f.write((output or " No response.") + "\n\n")

    print(f"\n✅ All results written to: {output_file}")