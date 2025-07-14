import os
import tkinter as tk
from tkinter import filedialog, messagebox
from design_parser import DesignParser
from pathlib import Path
from dotenv import load_dotenv

def main():
    # Set up Tkinter root and hide the main window
    root = tk.Tk()
    root.withdraw()

    print("🔍 Security Design Parser")
    print("-------------------------")

    # Use file dialog to choose a design document
    file_path = filedialog.askopenfilename(
        title="Select a Design Document",
        filetypes=[
            ("Design Documents", "*.pdf *.docx *.txt"),
            ("All Files", "*.*")
        ]
    )

    if not file_path:
        print("❌ No file selected. Exiting.")
        return

    if not Path(file_path).exists():
        messagebox.showerror("File Not Found", f"File not found: {file_path}")
        return

    try:
        with open(file_path, "rb") as file_obj:
            parser = DesignParser(file_obj=file_obj, filename=file_path)
            print(f"\n⏳ Parsing '{Path(file_path).name}' with GPT...")
            result = parser.parse()

            print("\n✅ Parsed Design Document:\n")
            print(result)

    except Exception as e:
        messagebox.showerror("Parsing Failed", str(e))
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
