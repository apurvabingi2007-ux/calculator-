import tkinter as tk
from tkinter import messagebox, ttk
import json
import math
from datetime import datetime
from pathlib import Path


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("350x600")
        self.root.resizable(False, False)
        
        # Color scheme
        self.bg_dark = "#1e1e1e"
        self.btn_num = "#333333"
        self.btn_op = "#4b4b4b"
        self.btn_equal = "#0078d7"
        self.text_color = "#ffffff"
        self.hover_color = "#404040"
        
        self.root.configure(bg=self.bg_dark)
        
        # Initialize state
        self.expression = ""
        self.result = ""
        self.mode = "calculator"
        self.history_file = Path("history.json")
        
        # Setup UI
        self.setup_display()
        self.setup_menu()
        self.setup_calculator()
        
    def setup_display(self):
        """Create two-line display"""
        display_frame = tk.Frame(self.root, bg=self.bg_dark)
        display_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        # Expression display
        self.expr_label = tk.Label(
            display_frame, text="", bg="#2a2a2a", fg="#888888",
            font=("Arial", 12), anchor="e", padx=10, pady=5
        )
        self.expr_label.pack(fill=tk.BOTH, pady=(0, 5))
        
        # Result display
        self.result_label = tk.Label(
            display_frame, text="0", bg="#2a2a2a", fg=self.text_color,
            font=("Arial", 28, "bold"), anchor="e", padx=10, pady=10
        )
        self.result_label.pack(fill=tk.BOTH)
        
    def setup_menu(self):
        """Create menu bar with Mode toggle and History"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        mode_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Mode", menu=mode_menu)
        mode_menu.add_command(label="Calculator", command=self.show_calculator)
        mode_menu.add_command(label="Unit Converter", command=self.show_converter)
        
        hist_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="History", menu=hist_menu)
        hist_menu.add_command(label="View History", command=self.view_history)
        hist_menu.add_command(label="Clear History", command=self.clear_history)
        
    def setup_calculator(self):
        """Create calculator button grid"""
        calc_frame = tk.Frame(self.root, bg=self.bg_dark)
        calc_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top row: AC, DEL, (, ), /
        top_row = tk.Frame(calc_frame, bg=self.bg_dark)
        top_row.pack(fill=tk.X, pady=(0, 5))
        
        self.create_button("AC", top_row, 0, 0, self.clear_all, "#5a0000")
        self.create_button("DEL", top_row, 1, 0, self.delete_last, "#5a0000")
        self.create_button("(", top_row, 2, 0, lambda: self.append_char("("))
        self.create_button(")", top_row, 3, 0, lambda: self.append_char(")"))
        self.create_button("÷", top_row, 4, 0, lambda: self.append_char("/"))
        
        # Scientific row
        sci_row = tk.Frame(calc_frame, bg=self.bg_dark)
        sci_row.pack(fill=tk.X, pady=(0, 5))
        
        self.create_button("√", sci_row, 0, 0, lambda: self.append_char("sqrt("))
        self.create_button("∛", sci_row, 1, 0, lambda: self.append_char("cbrt("))
        self.create_button("log₁₀", sci_row, 2, 0, lambda: self.append_char("log10("))
        self.create_button("ln", sci_row, 3, 0, lambda: self.append_char("log("))
        self.create_button("^", sci_row, 4, 0, lambda: self.append_char("**"))
        
        # Main grid
        main_frame = tk.Frame(calc_frame, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Numbers 7-8-9
        row1 = tk.Frame(main_frame, bg=self.bg_dark)
        row1.pack(fill=tk.X, pady=(0, 5))
        self.create_button("7", row1, 0, 0)
        self.create_button("8", row1, 1, 0)
        self.create_button("9", row1, 2, 0)
        self.create_button("×", row1, 4, 0, lambda: self.append_char("*"), color=self.btn_op)
        
        # Numbers 4-5-6
        row2 = tk.Frame(main_frame, bg=self.bg_dark)
        row2.pack(fill=tk.X, pady=(0, 5))
        self.create_button("4", row2, 0, 0)
        self.create_button("5", row2, 1, 0)
        self.create_button("6", row2, 2, 0)
        self.create_button("−", row2, 4, 0, lambda: self.append_char("-"), color=self.btn_op)
        
        # Numbers 1-2-3
        row3 = tk.Frame(main_frame, bg=self.bg_dark)
        row3.pack(fill=tk.X, pady=(0, 5))
        self.create_button("1", row3, 0, 0)
        self.create_button("2", row3, 1, 0)
        self.create_button("3", row3, 2, 0)
        self.create_button("+", row3, 4, 0, lambda: self.append_char("+"), color=self.btn_op)
        
        # Bottom row: 0, ., =
        row4 = tk.Frame(main_frame, bg=self.bg_dark)
        row4.pack(fill=tk.X)
        self.create_button("0", row4, 0, 0, width=2)
        self.create_button(".", row4, 2, 0)
        self.create_button("=", row4, 4, 0, self.calculate, color=self.btn_equal)
        
    def create_button(self, text, parent, col, row, command=None, color=None, width=1):
        """Create styled button"""
        if command is None:
            command = lambda t=text: self.append_char(t)
        
        if color is None:
            color = self.btn_num
        
        btn = tk.Button(
            parent, text=text, font=("Arial", 14, "bold"),
            bg=color, fg=self.text_color, activebackground=self.hover_color,
            activeforeground=self.text_color, relief=tk.FLAT,
            padx=10, pady=10, command=command, cursor="hand2"
        )
        btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        parent.grid_columnconfigure(col, weight=width)
        
    def append_char(self, char):
        """Append character to expression"""
        self.expression += char
        self.update_display()
        
    def update_display(self):
        """Update display labels"""
        self.expr_label.config(text=self.expression)
        try:
            if self.expression:
                result = self.safe_eval(self.expression)
                self.result = str(result)
            else:
                self.result = "0"
        except:
            self.result = "Error"
        
        self.result_label.config(text=self.result)
        
    def safe_eval(self, expr):
        """Safely evaluate mathematical expression"""
        # Replace symbols
        expr = expr.replace("÷", "/").replace("×", "*").replace("−", "-")
        
        # Create safe namespace
        safe_dict = {
            "sqrt": math.sqrt,
            "cbrt": lambda x: x ** (1/3),
            "log10": math.log10,
            "log": math.log,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "pi": math.pi,
            "e": math.e,
        }
        
        result = eval(expr, {"__builtins__": {}}, safe_dict)
        
        # Round to 10 decimals to avoid floating point errors
        if isinstance(result, float):
            result = round(result, 10)
        
        return result
        
    def calculate(self):
        """Calculate result and save to history"""
        try:
            if not self.expression:
                return
            
            result = self.safe_eval(self.expression)
            
            # Save to history
            self.save_history(self.expression, result)
            
            self.expression = str(result)
            self.result = str(result)
            self.update_display()
            
        except ZeroDivisionError:
            messagebox.showerror("Math Error", "Division by zero")
            self.result = "Error"
            self.result_label.config(text=self.result)
        except ValueError as e:
            messagebox.showerror("Math Error", f"Invalid input: {str(e)}")
            self.result = "Error"
            self.result_label.config(text=self.result)
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
            self.result = "Error"
            self.result_label.config(text=self.result)
            
    def delete_last(self):
        """Delete last character"""
        self.expression = self.expression[:-1]
        self.update_display()
        
    def clear_all(self):
        """Clear expression"""
        self.expression = ""
        self.result = "0"
        self.update_display()
        
    def save_history(self, expr, result):
        """Save calculation to history.json"""
        try:
            history = []
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    history = json.load(f)
            
            history.append({
                "expression": expr,
                "result": result,
                "timestamp": datetime.now().isoformat()
            })
            
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")
            
    def view_history(self):
        """Display history in a popup window"""
        try:
            if not self.history_file.exists():
                messagebox.showinfo("History", "No history yet")
                return
            
            with open(self.history_file, 'r') as f:
                history = json.load(f)
            
            if not history:
                messagebox.showinfo("History", "No history yet")
                return
            
            # Create history window
            hist_window = tk.Toplevel(self.root)
            hist_window.title("Calculation History")
            hist_window.geometry("400x300")
            hist_window.configure(bg=self.bg_dark)
            
            # Create text widget
            text_widget = tk.Text(
                hist_window, bg="#2a2a2a", fg=self.text_color,
                font=("Arial", 10), wrap=tk.WORD
            )
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Add history
            for item in reversed(history[-20:]):  # Show last 20
                expr = item.get("expression", "")
                result = item.get("result", "")
                timestamp = item.get("timestamp", "")
                
                text_widget.insert(tk.END, f"{expr} = {result}\n")
                text_widget.insert(tk.END, f"  {timestamp}\n\n")
            
            text_widget.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Cannot load history: {e}")
            
    def clear_history(self):
        """Clear all history"""
        if messagebox.askyesno("Confirm", "Clear all history?"):
            try:
                if self.history_file.exists():
                    self.history_file.unlink()
                messagebox.showinfo("Success", "History cleared")
            except Exception as e:
                messagebox.showerror("Error", f"Cannot clear history: {e}")
                
    def show_calculator(self):
        """Switch to calculator mode"""
        self.root.geometry("350x600")
        
    def show_converter(self):
        """Open unit converter window"""
        converter_window = tk.Toplevel(self.root)
        converter_window.title("Unit Converter")
        converter_window.geometry("350x300")
        converter_window.configure(bg=self.bg_dark)
        
        # Converter type selector
        tk.Label(
            converter_window, text="Conversion Type:", bg=self.bg_dark,
            fg=self.text_color, font=("Arial", 11)
        ).pack(pady=(10, 5))
        
        converter_var = tk.StringVar(value="length")
        type_frame = tk.Frame(converter_window, bg=self.bg_dark)
        type_frame.pack(pady=5)
        
        tk.Radiobutton(
            type_frame, text="Length", variable=converter_var, value="length",
            bg=self.bg_dark, fg=self.text_color, selectcolor=self.btn_op
        ).pack(anchor=tk.W)
        
        tk.Radiobutton(
            type_frame, text="Weight", variable=converter_var, value="weight",
            bg=self.bg_dark, fg=self.text_color, selectcolor=self.btn_op
        ).pack(anchor=tk.W)
        
        tk.Radiobutton(
            type_frame, text="Temperature", variable=converter_var, value="temp",
            bg=self.bg_dark, fg=self.text_color, selectcolor=self.btn_op
        ).pack(anchor=tk.W)
        
        # Input fields
        tk.Label(
            converter_window, text="From:", bg=self.bg_dark,
            fg=self.text_color, font=("Arial", 10)
        ).pack(pady=(10, 0))
        
        from_entry = tk.Entry(
            converter_window, bg="#333333", fg=self.text_color,
            font=("Arial", 11), width=20
        )
        from_entry.pack(pady=5)
        
        tk.Label(
            converter_window, text="To:", bg=self.bg_dark,
            fg=self.text_color, font=("Arial", 10)
        ).pack()
        
        to_label = tk.Label(
            converter_window, text="0", bg="#2a2a2a", fg=self.text_color,
            font=("Arial", 14, "bold"), padx=10, pady=10
        )
        to_label.pack(fill=tk.X, padx=20, pady=5)
        
        def do_convert():
            try:
                value = float(from_entry.get())
                conv_type = converter_var.get()
                
                if conv_type == "length":
                    # cm to inches
                    result = value / 2.54
                    to_label.config(text=f"{result:.4f} inches")
                elif conv_type == "weight":
                    # kg to pounds
                    result = value * 2.20462
                    to_label.config(text=f"{result:.4f} lbs")
                elif conv_type == "temp":
                    # Celsius to Fahrenheit
                    result = (value * 9/5) + 32
                    to_label.config(text=f"{result:.2f} °F")
            except ValueError:
                messagebox.showerror("Error", "Invalid input")
        
        from_entry.bind("<KeyRelease>", lambda e: do_convert())
        
        tk.Button(
            converter_window, text="Convert", command=do_convert,
            bg=self.btn_equal, fg=self.text_color,
            font=("Arial", 11, "bold"), padx=20, pady=10
        ).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
