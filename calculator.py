#!/usr/bin/env python3
"""Professional Scientific Calculator with Modern Dark Theme GUI using tkinter."""

import json
import math
import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime
from pathlib import Path


class ScientificCalculator:
    """A scientific calculator that evaluates expressions and maintains calculation history."""
    
    HISTORY_FILE = "history.json"
    
    def __init__(self):
        """Initialize the calculator and load history."""
        self.history = self._load_history()
    
    def _load_history(self):
        """Load calculation history from JSON file."""
        if Path(self.HISTORY_FILE).exists():
            try:
                with open(self.HISTORY_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _save_history(self):
        """Save calculation history to JSON file."""
        try:
            with open(self.HISTORY_FILE, 'w') as f:
                json.dump(self.history, f, indent=2)
        except IOError as e:
            raise IOError(f"Could not save history: {e}")
    
    def _add_to_history(self, expression, result):
        """Add a calculation to history with timestamp."""
        entry = {
            "expression": expression,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        self.history.append(entry)
        self._save_history()
    
    def _validate_expression(self, expression):
        """Validate expression syntax before evaluation."""
        if expression.count('(') != expression.count(')'):
            raise SyntaxError("Unbalanced parentheses")
        
        allowed_chars = set('0123456789+-*/(). ,sqrtsincoswpie^')
        if not all(c.lower() in allowed_chars for c in expression.replace(' ', '')):
            raise SyntaxError("Unsupported characters")
    
    def evaluate(self, expression):
        """
        Safely evaluate a mathematical expression.
        Supports: +, -, *, /, (, ), sqrt(), sin(), cos(), pow(), ^
        """
        try:
            self._validate_expression(expression)
            
            expression = expression.replace('^', '**')
            
            safe_dict = {
                '__builtins__': {},
                'sqrt': math.sqrt,
                'sin': math.sin,
                'cos': math.cos,
                'pow': math.pow,
                'pi': math.pi,
                'e': math.e
            }
            
            result = eval(expression, safe_dict)
            self._add_to_history(expression, result)
            
            return result
        
        except ZeroDivisionError:
            raise ValueError("Division by zero")
        except SyntaxError as e:
            raise SyntaxError(f"Invalid syntax: {str(e)}")
        except NameError as e:
            raise SyntaxError(f"Unknown function or variable: {str(e)}")
        except ValueError as e:
            raise ValueError(f"Math error: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error: {str(e)}")
    
    def clear_history(self):
        """Clear all calculation history."""
        self.history = []
        self._save_history()


class CalculatorGUI:
    """Modern Dark Theme GUI Calculator using tkinter."""
    
    # Color scheme
    COLORS = {
        'bg': '#1e1e1e',           # Dark background
        'fg': '#ffffff',           # White text
        'display_bg': '#2d2d2d',   # Display background
        'button_number': '#3d3d3d', # Number buttons
        'button_operator': '#ff9500', # Operator buttons
        'button_function': '#0d8fc7', # Function buttons
        'button_equals': '#4caf50',   # Equals button
        'button_clear': '#f44336',    # Clear button
        'accent': '#0d8fc7'
    }
    
    def __init__(self, root):
        """Initialize the GUI calculator."""
        self.root = root
        self.calculator = ScientificCalculator()
        self.current_input = ""
        self.last_result = None
        
        self._setup_window()
        self._create_widgets()
    
    def _setup_window(self):
        """Configure the main window."""
        self.root.title("Professional Scientific Calculator")
        self.root.geometry("500x700")
        self.root.configure(bg=self.COLORS['bg'])
        self.root.resizable(False, False)
    
    def _create_widgets(self):
        """Create and layout all GUI widgets."""
        # Main container
        container = tk.Frame(self.root, bg=self.COLORS['bg'])
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title = tk.Label(
            container, text="🧮 Scientific Calculator",
            font=("Arial", 20, "bold"), fg=self.COLORS['fg'],
            bg=self.COLORS['bg']
        )
        title.pack(pady=(0, 10))
        
        # Display area
        display_frame = tk.Frame(container, bg=self.COLORS['display_bg'], relief=tk.SUNKEN, bd=2)
        display_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.display = tk.Entry(
            display_frame, font=("Arial", 24, "bold"),
            fg=self.COLORS['accent'], bg=self.COLORS['display_bg'],
            border=0, justify=tk.RIGHT
        )
        self.display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.display.bind('<Return>', lambda e: self._evaluate())
        self.display.bind('<BackSpace>', lambda e: self._backspace())
        
        # Button grid
        self._create_button_grid(container)
        
        # History button at bottom
        history_btn = tk.Button(
            container, text="📋 History",
            font=("Arial", 11, "bold"), bg=self.COLORS['accent'],
            fg=self.COLORS['fg'], command=self._show_history,
            relief=tk.FLAT, padx=10, pady=8
        )
        history_btn.pack(fill=tk.X, pady=(10, 0))
    
    def _create_button_grid(self, parent):
        """Create the calculator button grid."""
        grid_frame = tk.Frame(parent, bg=self.COLORS['bg'])
        grid_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button layout: [label, button_type]
        buttons = [
            # Row 1: Functions
            [("√", "func"), ("^", "operator"), ("sin", "func"), ("cos", "func"), ("C", "clear")],
            # Row 2: Numbers and operations
            [("7", "number"), ("8", "number"), ("9", "number"), ("/", "operator"), ("(", "operator")],
            # Row 3
            [("4", "number"), ("5", "number"), ("6", "number"), ("*", "operator"), (")", "operator")],
            # Row 4
            [("1", "number"), ("2", "number"), ("3", "number"), ("-", "operator"), ("π", "func")],
            # Row 5
            [("0", "number"), (".", "number"), ("e", "func"), ("+", "operator"), ("=", "equals")],
        ]
        
        for row in buttons:
            row_frame = tk.Frame(grid_frame, bg=self.COLORS['bg'])
            row_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
            
            for label, btn_type in row:
                self._create_button(row_frame, label, btn_type)
    
    def _create_button(self, parent, label, btn_type):
        """Create a single calculator button."""
        if btn_type == "number":
            bg = self.COLORS['button_number']
            fg = self.COLORS['fg']
        elif btn_type == "operator":
            bg = self.COLORS['button_operator']
            fg = self.COLORS['bg']
        elif btn_type == "func":
            bg = self.COLORS['button_function']
            fg = self.COLORS['fg']
        elif btn_type == "equals":
            bg = self.COLORS['button_equals']
            fg = self.COLORS['fg']
        else:  # clear
            bg = self.COLORS['button_clear']
            fg = self.COLORS['fg']
        
        btn = tk.Button(
            parent, text=label, font=("Arial", 14, "bold"),
            bg=bg, fg=fg, relief=tk.FLAT,
            command=lambda: self._handle_button_click(label, btn_type),
            activebackground=self._lighten_color(bg),
            activeforeground=fg
        )
        btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    def _lighten_color(self, color):
        """Lighten a hex color slightly for hover effect."""
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = min(255, r + 30), min(255, g + 30), min(255, b + 30)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def _handle_button_click(self, label, btn_type):
        """Handle button click events."""
        if btn_type == "clear":
            self._clear_display()
        elif btn_type == "equals":
            self._evaluate()
        elif label == "√":
            self._insert_text("sqrt(")
        elif label == "π":
            self._insert_text("pi")
        elif label == "e":
            self._insert_text("e")
        elif label == "sin":
            self._insert_text("sin(")
        elif label == "cos":
            self._insert_text("cos(")
        else:
            self._insert_text(label)
    
    def _insert_text(self, text):
        """Insert text into the display."""
        current = self.display.get()
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, current + text)
        self.display.see(tk.END)
    
    def _backspace(self):
        """Remove the last character."""
        current = self.display.get()
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, current[:-1])
    
    def _clear_display(self):
        """Clear the display."""
        self.display.delete(0, tk.END)
        self.current_input = ""
    
    def _evaluate(self):
        """Evaluate the expression and display result."""
        expression = self.display.get().strip()
        
        if not expression:
            return
        
        try:
            result = self.calculator.evaluate(expression)
            self.last_result = result
            self.display.delete(0, tk.END)
            
            if isinstance(result, float):
                if result == int(result):
                    self.display.insert(tk.END, str(int(result)))
                else:
                    self.display.insert(tk.END, f"{result:.10g}")
            else:
                self.display.insert(tk.END, str(result))
            
        except (ValueError, SyntaxError) as e:
            messagebox.showerror("Calculation Error", f"Error: {str(e)}")
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, expression)
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
    
    def _show_history(self):
        """Open a window to display calculation history."""
        history_window = tk.Toplevel(self.root)
        history_window.title("Calculation History")
        history_window.geometry("600x400")
        history_window.configure(bg=self.COLORS['bg'])
        
        # Header
        header = tk.Label(
            history_window, text="📋 Calculation History",
            font=("Arial", 14, "bold"), fg=self.COLORS['fg'],
            bg=self.COLORS['bg']
        )
        header.pack(pady=10)
        
        # Display history
        if not self.calculator.history:
            msg = tk.Label(
                history_window, text="No calculations in history yet.",
                font=("Arial", 12), fg=self.COLORS['accent'],
                bg=self.COLORS['bg']
            )
            msg.pack(pady=20)
        else:
            text_widget = scrolledtext.ScrolledText(
                history_window, font=("Courier", 10),
                bg=self.COLORS['display_bg'], fg=self.COLORS['fg'],
                relief=tk.SUNKEN, bd=2
            )
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
            text_widget.config(state=tk.DISABLED)
            
            history_text = self._format_history()
            text_widget.config(state=tk.NORMAL)
            text_widget.insert(tk.END, history_text)
            text_widget.config(state=tk.DISABLED)
        
        # Buttons
        button_frame = tk.Frame(history_window, bg=self.COLORS['bg'])
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        if self.calculator.history:
            clear_btn = tk.Button(
                button_frame, text="Clear History",
                font=("Arial", 10, "bold"), bg=self.COLORS['button_clear'],
                fg=self.COLORS['fg'], command=lambda: self._clear_history(history_window),
                relief=tk.FLAT, padx=10, pady=5
            )
            clear_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = tk.Button(
            button_frame, text="Close",
            font=("Arial", 10, "bold"), bg=self.COLORS['button_number'],
            fg=self.COLORS['fg'], command=history_window.destroy,
            relief=tk.FLAT, padx=10, pady=5
        )
        close_btn.pack(side=tk.RIGHT, padx=5)
    
    def _format_history(self):
        """Format history entries for display."""
        if not self.calculator.history:
            return ""
        
        lines = []
        for idx, entry in enumerate(self.calculator.history, 1):
            expr = entry.get('expression', 'N/A')
            result = entry.get('result', 'N/A')
            timestamp = entry.get('timestamp', 'N/A')
            
            lines.append(f"{idx}. {expr} = {result}")
            lines.append(f"   Time: {timestamp}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _clear_history(self, window):
        """Clear history with confirmation."""
        if messagebox.askyesno("Confirm", "Clear all history?"):
            self.calculator.clear_history()
            window.destroy()
            messagebox.showinfo("Success", "History cleared!")


def main():
    """Entry point for the GUI calculator."""
    root = tk.Tk()
    gui = CalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
