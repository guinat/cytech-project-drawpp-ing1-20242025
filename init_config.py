#!/usr/bin/env python3

import os
import json
from compiler.codegen.codegen import create_default_config

def init_codegen_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "compiler", "codegen", "codegen_config.json")
    create_default_config(config_path)
    print(f"Configuration file created at: {config_path}")

if __name__ == "__main__":
    init_codegen_config()