# 🧮 PythonCalc - A Lightweight CLI Calculator
PythonCalc is a lightweight, extensible command-line calculator tool built in Python. Designed for quick arithmetic operations and basic scripting experimentation, PythonCalc allows users to evaluate mathematical expressions, perform unit conversions, and even write their own plugins for specialized calculations.

## 🚀 Features
- Basic arithmetic: +, -, *, /, **, %
- Built-in constants: pi, e, phi
- Simple function support: sin, cos, log, etc.
- Expression evaluation using Python’s AST module
- Plugin system for custom extensions
- Lightweight and fast – no heavy GUI or dependencies

## 🛠️ Installation
```bash
cd pythoncalc
pip install -r requirements.txt
```

## 📦 Usage
**Run the interactive calculator:**

```bash
python calc.py
```

**Evaluate a single expression:**
```bash
python calc.py "3 * (2 + 5)"
# Output: 21
```

## 🔌 Plugin Support
You can add your own custom functions or constants by placing Python scripts in the plugins/ directory.
Example:

```python
# plugins/fibonacci.py
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)
```

## 📁 Project Structure
```pgsql
pythoncalc/
├── calc.py
└── README.md
```

## License
MIT License.
