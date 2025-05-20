import tkinter as tk
from tkinter import scrolledtext, messagebox
from lexer import Lexer
from parser import Parser

class ParserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lexer & Parser GUI")

        self.input_label = tk.Label(root, text="Enter source code:")
        self.input_label.pack()

        self.input_text = tk.Text(root, height=10, width=70)
        self.input_text.pack()

        self.run_button = tk.Button(root, text="Run Lexer & Parser", command=self.run_lexer_parser)
        self.run_button.pack(pady=10)

        self.output_label = tk.Label(root, text="Output:")
        self.output_label.pack()

        self.output_text = scrolledtext.ScrolledText(root, height=15, width=70, state='disabled')
        self.output_text.pack()

    def run_lexer_parser(self):
        source_code = self.input_text.get("1.0", tk.END).strip()
        if not source_code:
            messagebox.showwarning("Input needed", "Please enter source code to parse.")
            return
        lexer = Lexer(source_code)
        try:
            tokens = lexer.tokenize()
        except SyntaxError as e:
            self.display_output(f"Lexer error: {e}")
            return

        parser = Parser(tokens)
        try:
            parse_tree = parser.parse()
        except SyntaxError as e:
            self.display_output(f"Parser error: {e}")
            return

        self.display_output("Tokens:\n" + '\n'.join(str(t) for t in tokens) + "\n\nParse Tree:\n" + str(parse_tree))

    def display_output(self, text):
        self.output_text.config(state='normal')
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state='disabled')


def run_gui():
    root = tk.Tk()
    app = ParserApp(root)
    root.mainloop()







