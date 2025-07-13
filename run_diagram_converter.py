import tkinter as tk
from tkinter import filedialog, messagebox
from diagram_to_mermaid_converter import DiagramToMermaidConverter

class DiagramConversionRunner:
    """
    UI wrapper to allow user to select input image and output file location,
    then trigger the diagram-to-Mermaid conversion.
    """

    def __init__(self, model_name="gpt-4o"):
        self.converter = DiagramToMermaidConverter(model_name=model_name)

    def run(self):
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        try:
            # Ask for input image
            image_path = filedialog.askopenfilename(
                title="Select Architecture Diagram Image",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp *.bmp *.gif")]
            )
            if not image_path:
                print("No image selected.")
                return

            # Ask for output file
            output_path = filedialog.asksaveasfilename(
                title="Save Mermaid Diagram As",
                defaultextension=".mmd",
                filetypes=[("Mermaid files", "*.mmd"), ("Text files", "*.txt")]
            )
            if not output_path:
                print("No output path selected.")
                return

            # Call the converter
            mermaid_text = self.converter.convert(image_path, output_path)
            messagebox.showinfo("Success", f"Mermaid diagram saved to:\n{output_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed:\n{e}")
if __name__ == "__main__":
    runner = DiagramConversionRunner()
    runner.run()