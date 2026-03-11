#!/usr/bin/env python3

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y

def main():
    print("=== Simple Calculator ===")
    print("Operations: add, subtract, multiply, divide")
    
    while True:
        try:
            operation = input("\nEnter operation (add/subtract/multiply/divide) or 'quit' to exit: ").strip().lower()
            
            if operation == 'quit':
                print("Goodbye!")
                break
            
            if operation not in ['add', 'subtract', 'multiply', 'divide']:
                print("Invalid operation. Please choose: add, subtract, multiply, or divide")
                continue
            
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            
            if operation == 'add':
                result = add(num1, num2)
            elif operation == 'subtract':
                result = subtract(num1, num2)
            elif operation == 'multiply':
                result = multiply(num1, num2)
            elif operation == 'divide':
                result = divide(num1, num2)
            
            print(f"Result: {num1} {get_symbol(operation)} {num2} = {result}")
        
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Invalid input: {e}")

def get_symbol(operation):
    symbols = {
        'add': '+',
        'subtract': '-',
        'multiply': '*',
        'divide': '/'
    }
    return symbols.get(operation, '?')

if __name__ == "__main__":
    main()
