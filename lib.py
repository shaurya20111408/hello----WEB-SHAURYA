import math
import sys
from typing import Union


class Calculator:
      """Advanced calculator with scientific functions and history."""

      def __init__(self):
          self.history = []
          self.constants = {
              'pi': math.pi,
              'e': math.e,
              'tau': math.tau,
          }

      # --- Basic Operations ---
      def add(self, a: float, b: float) -> float:
          return a + b

      def subtract(self, a: float, b: float) -> float:
          return a - b

      def multiply(self, a: float, b: float) -> float:
          return a * b

      def divide(self, a: float, b: float) -> float:
          if b == 0:
              raise ZeroDivisionError("Cannot divide by zero")
          return a / b

      def power(self, a: float, b: float) -> float:
          return a ** b

      def modulo(self, a: float, b: float) -> float:
          if b == 0:
              raise ZeroDivisionError("Cannot modulo by zero")
          return a % b

      def floor_divide(self, a: float, b: float) -> float:
          if b == 0:
              raise ZeroDivisionError("Cannot divide by zero")
          return a // b

      # --- Scientific Functions ---
      def sqrt(self, a: float) -> float:
          if a < 0:
              raise ValueError("Cannot take square root of negative number")
          return math.sqrt(a)

      def log(self, a: float, base: float = math.e) -> float:
          if a <= 0:
              raise ValueError("Logarithm undefined for non-positive numbers")
          if base <= 0 or base == 1:
              raise ValueError("Invalid logarithm base")
          return math.log(a, base)

      def ln(self, a: float) -> float:
          return self.log(a, math.e)

      def log10(self, a: float) -> float:
          return self.log(a, 10)

      def sin(self, a: float, degrees: bool = False) -> float:
          if degrees:
              a = math.radians(a)
          return math.sin(a)

      def cos(self, a: float, degrees: bool = False) -> float:
          if degrees:
              a = math.radians(a)
          return math.cos(a)

      def tan(self, a: float, degrees: bool = False) -> float:
          if degrees:
              a = math.radians(a)
          return math.tan(a)

      def asin(self, a: float, degrees: bool = False) -> float:
          if not -1 <= a <= 1:
              raise ValueError("arcsin domain is [-1, 1]")
          result = math.asin(a)
          return math.degrees(result) if degrees else result

      def acos(self, a: float, degrees: bool = False) -> float:
          if not -1 <= a <= 1:
              raise ValueError("arccos domain is [-1, 1]")
          result = math.acos(a)
          return math.degrees(result) if degrees else result

      def atan(self, a: float, degrees: bool = False) -> float:
          result = math.atan(a)
          return math.degrees(result) if degrees else result

      def factorial(self, n: int) -> int:
          if n < 0:
                raise ValueError("Factorial is not defined for negative numbers")       
          if n > 170:
              raise ValueError("Result too large (max 170!)")
          return math.factorial(n)

      def abs(self, a: float) -> float:
          return abs(a)

      def round(self, a: float, ndigits: int = 0) -> float:
          return round(a, ndigits)

      def ceil(self, a: float) -> int:
          return math.ceil(a)

      def floor(self, a: float) -> int:
          return math.floor(a)

      # --- Expression Evaluation ---
      def evaluate(self, expression: str) -> float:
          """Safely evaluate a mathematical expression."""
          # Allow only safe characters
          allowed_chars = set("0123456789.+-*/()% ")
          allowed_chars.update("abcdefghijklmnopqrstuvwxyz_")

          if not all(c in allowed_chars for c in expression.lower()):
              raise ValueError("Invalid characters in expression")

          # Replace constants
          for const, value in self.constants.items():
              expression = expression.replace(const, str(value))

          # Replace ^ with ** for power
          expression = expression.replace('^', '**')

          try:
              result = eval(expression, {"__builtins__": {}}, {
                  'sin': lambda x: self.sin(x),
                  'cos': lambda x: self.cos(x),
                  'tan': lambda x: self.tan(x),
                  'sqrt': lambda x: self.sqrt(x),
                  'log': lambda x, b=math.e: self.log(x, b),
                  'ln': lambda x: self.ln(x),
                  'log10': lambda x: self.log10(x),
                  'factorial': lambda x: self.factorial(int(x)),
                  'abs': lambda x: self.abs(x),
                  'round': lambda x, n=0: self.round(x, n),
                  'ceil': lambda x: self.ceil(x),
                  'floor': lambda x: self.floor(x),
                  'pi': math.pi,
                  'e': math.e,
                  'tau': math.tau,
              })
              return float(result)
          except ZeroDivisionError:
              raise
          except Exception as e:
              raise ValueError(f"Invalid expression: {e}")

      # --- History Management ---
      def add_to_history(self, expression: str, result: float):
          self.history.append((expression, result))

      def show_history(self, limit: int = 10):
          if not self.history:
              print("No history yet.")
              return
          print(f"\n📜 Last {min(limit, len(self.history))} entries:")
          for i, (expr, result) in enumerate(self.history[-limit:], start=1):
              print(f"  {i}. {expr} = {result}")

      def clear_history(self):
          self.history.clear()
          print("History cleared.")


def format_result(value: float) -> str:
      """Format result nicely (avoid unnecessary decimals)."""
      if value == int(value):
          return str(int(value))
      return f"{value:.10g}"


def print_menu():
      print("\n" + "=" * 50)
      print("🧮 ADVANCED CALCULATOR")
      print("=" * 50)
      print("Basic:     +  -  *  /  //  %  ^ (power)")
      print("Scientific: sin cos tan asin acos atan")
      print("           sqrt log ln log10")
      print("           fact abs round ceil floor")
      print("Constants: pi e tau")
      print("Commands:  hist  clear  help  quit")
      print("=" * 50)


def parse_input(user_input: str, calc: Calculator) -> Union[float,
  None]:
      """Parse and execute user input."""
      parts = user_input.strip().split()
      if not parts:
          return None

      cmd = parts[0].lower()

      # Commands
      if cmd in ('quit', 'exit', 'q'):
          print("Goodbye! 👋")
          sys.exit(0)
      elif cmd in ('help', 'h', '?'):
          print_menu()
          return None
      elif cmd in ('hist', 'history'):
          limit = int(parts[1]) if len(parts) > 1 else 10
          calc.show_history(limit)
          return None
      elif cmd == 'clear':
          calc.clear_history()
          return None

      # Try as expression first (e.g., "2 + 3 * 4")
      try:
          return calc.evaluate(user_input)
      except ValueError:
          pass

      # Try as function call (e.g., "sin 30" or "sin(30)")
      if len(parts) >= 2:
          func_name = cmd
          args_str = ' '.join(parts[1:])

          # Handle parentheses format: "sin(30)"
          if '(' in args_str and ')' in args_str:
              try:
                  return calc.evaluate(user_input)
              except ValueError:
                  pass

          # Handle space-separated format: "sin 30"
          try:
              args = [float(x) for x in args_str.split()]
          except ValueError:
              raise ValueError(f"Invalid arguments for {func_name}")

          func_map = {
              'sin': (lambda a: calc.sin(a, degrees=True), 1),
              'cos': (lambda a: calc.cos(a, degrees=True), 1),
              'tan': (lambda a: calc.tan(a, degrees=True), 1),
              'asin': (lambda a: calc.asin(a, degrees=True), 1),
              'acos': (lambda a: calc.acos(a, degrees=True), 1),
              'atan': (lambda a: calc.atan(a, degrees=True), 1),
              'sqrt': (calc.sqrt, 1),
              'log': (calc.log, 2),
              'ln': (calc.ln, 1),
              'log10': (calc.log10, 1),
              'fact': (calc.factorial, 1),
              'factorial': (calc.factorial, 1),
              'abs': (calc.abs, 1),
              'round': (calc.round, 2),
              'ceil': (calc.ceil, 1),
              'floor': (calc.floor, 1),
          }

          if func_name in func_map:
              func, expected_args = func_map[func_name]
              if len(args) != expected_args:
                  raise ValueError(
                      f"{func_name} expects {expected_args} argument(s)"
                  )
              return func(*args)

      raise ValueError(f"Unknown command or invalid expression: {user_input}")


def main():
      calc = Calculator()
      print_menu()
      print("Enter expressions like: 2 + 3 * 4")
      print("Or functions like: sin 30  (degrees by default)")
      print("Or with parentheses: sqrt(16)")

      while True:
          try:
              user_input = input("\n> ").strip()
              if not user_input:
                  continue

              result = parse_input(user_input, calc)
              if result is not None:
                  formatted = format_result(result)
                  print(f"= {formatted}")
                  calc.add_to_history(user_input, result)

          except KeyboardInterrupt:
              print("\nGoodbye! 👋")
              break
          except ZeroDivisionError as e:
              print(f"Error: {e}")
          except ValueError as e:
              print(f"Error: {e}")
          except Exception as e:
              print(f"Unexpected error: {e}")


if __name__ == "__main__":
        main()