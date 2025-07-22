#!/usr/bin/env python3
"""
PythonCalc - Lightweight CLI Calculator with Plugin Support
"""

import argparse
import math
import os
import sys
import ast
import operator
import importlib.util

# Core math operations (safe eval)
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}

# Built-in safe functions
SAFE_FUNCTIONS = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "sqrt": math.sqrt,
    "abs": abs,
    "round": round,
}

# Built-in constants
CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
    "phi": (1 + 5 ** 0.5) / 2,
}

# Plugin function store
PLUGINS = {}

def load_plugins(plugin_dir='plugins'):
    """Dynamically load Python plugins"""
    if not os.path.isdir(plugin_dir):
        return
    for filename in os.listdir(plugin_dir):
        if filename.endswith(".py"):
            path = os.path.join(plugin_dir, filename)
            spec = importlib.util.spec_from_file_location(filename[:-3], path)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
                for attr in dir(module):
                    if not attr.startswith("_"):
                        obj = getattr(module, attr)
                        if callable(obj):
                            PLUGINS[attr] = obj
            except Exception as e:
                print(f"Failed to load plugin {filename}: {e}")

def eval_expr(expr):
    """Parse and evaluate a math expression safely"""
    try:
        tree = ast.parse(expr, mode='eval')
        return _eval_node(tree.body)
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")

def _eval_node(node):
    if isinstance(node, ast.Num):  # e.g., 3, 4.2
        return node.n
    elif isinstance(node, ast.BinOp):  # e.g., 3 + 4
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            return SAFE_OPERATORS[op_type](left, right)
    elif isinstance(node, ast.UnaryOp):  # e.g., -3
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            return SAFE_OPERATORS[op_type](operand)
    elif isinstance(node, ast.Call):  # e.g., sin(3.14)
        func_name = getattr(node.func, 'id', None)
        args = [_eval_node(arg) for arg in node.args]
        if func_name in SAFE_FUNCTIONS:
            return SAFE_FUNCTIONS[func_name](*args)
        if func_name in PLUGINS:
            return PLUGINS[func_name](*args)
    elif isinstance(node, ast.Name):  # constants like pi, e
        if node.id in CONSTANTS:
            return CONSTANTS[node.id]
    raise ValueError("Unsafe or unsupported expression.")

def main():
    parser = argparse.ArgumentParser(description="Lightweight Python Calculator")
    parser.add_argument("expression", nargs='?', help="Math expression to evaluate (e.g. '3 + 4 * 2')")
    args = parser.parse_args()

    load_plugins()

    if args.expression:
        try:
            result = eval_expr(args.expression)
            print(result)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Interactive mode (type 'exit' to quit)")
        while True:
            try:
                expr = input(">>> ")
                if expr.lower() in ("exit", "quit"):
                    break
                result = eval_expr(expr)
                print(result)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
