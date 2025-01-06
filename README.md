<a name="readme-top"></a>

<br />
<div align="center">
  <a href="https://github.com/guinat/cytech-project-drawpp-ing1-20242025">
    <img src="logo.png" alt="Logo" width="100" height="100">
  </a>

  <h3 align="center">Draw++</h3>

  <p align="center">
    A custom-designed language for drawing!
    <br />
    <a href="https://github.com/guinat/cytech-project-drawpp-ing1-20242025"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/guinat/cytech-project-drawpp-ing1-20242025">View Demo</a>
    ·
    <a href="https://github.com/guinat/cytech-project-drawpp-ing1-20242025/issues">Report Bug</a>
    ·
    <a href="https://github.com/guinat/cytech-project-drawpp-ing1-20242025/issues">Request Feature</a>
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#language-features">Language Features</a></li>
    <li><a href="#ide-features">IDE Features</a></li>
  </ol>
</details>

## About The Project

Draw++ is a programming language designed to create shapes on a screen through a rich set of user-defined instructions. It integrates essential features like a cursor-based drawing system, color and style customizations, and supports advanced programming constructs such as loops, conditions, and function blocks.

It also provides an IDE for creating, editing, and debugging Draw++ code.

### Key Features

- **Elementary Instructions:** Cursor manipulation, drawing shapes (triangle, circles, rectangles), and color selection.
- **Advanced Constructs:** Variable assignments, conditionals (`if`, `else`), loops (`for`, `while`), and block instructions.
- **Integrated IDE:** Code editor with syntax highlighting, debugging tools, and live visual feedback.
- **Intermediate Code:** Transpiles Draw++ code into C for execution, combining the simplicity of scripting with the power of compiled languages.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Getting Started

To begin with Draw++, follow the steps below to set up your environment and start exploring the language.

### Prerequisites

- **Python:** Required for the Draw++ compiler. Install using:

  ```sh
  sudo apt-get install python3
  ```

- **C Compiler:** To compile the generated intermediate code. For example:

  ```sh
  sudo apt-get install gcc
  ```

### Installation


1. Clone the repository:

```sh
  git clone https://github.com/guinat/cytech-project-drawpp-ing1-20242025.git
```

2. Navigate to the project directory:

```sh
  cd cytech-project-drawpp-ing1-20242025
```

3. Create a virtual environment:

- **Windows**:
  ```sh
  python -m venv env
  env\Scripts\activate
  ```

- **Linux/macOS**:
  ```sh
  python3 -m venv venv
  source venv/bin/activate
  ```

4. Install required dependencies:

```sh
  pip install -r requirements.txt
```

5. Install the project in editable mode:

```sh
  pip install -e .
```

6. Launch the IDE:

```sh
  cd ide
  python3 main.py
```
> ⚠️ It is important to launch the IDE from the right directory. Otherwise, the code wont run.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Language Features

### Basic Syntax

- Statements end with `;`.
- Supports data types: `int`, `float`, `bool`, `string`, and `color`.

### Key Constructs

- **Variables and Constants:** Define and use values with `var`.
- **Control Flow:** Use `if`, `else`, `while`, and `for` loops for dynamic behavior.
- **Drawing Tools:** Control a `cursor` to draw lines, circles, and more.

For a detailed grammar, visit [Draw++ Language Grammar](https://github.com/guinat/cytech-project-drawpp-ing1-20242025/blob/main/grammar/drawpp_grammar.bnf).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## IDE Features

The Draw++ IDE includes:

- Syntax highlighting and error reporting.
- Code execution and live debugging.
- Tools for shape manipulation: zoom, rotate, select, etc.
- Multi-file management and interactive error correction.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Terminal Features

The Draw++ terminal is a powerful and interactive component that enhances the development experience by providing a seamless way to execute and debug Draw++ code. This terminal is specifically designed to cater to the needs of developers working with the Draw++ language.

### Key Features of the Terminal

- **Interactive Command Execution**:
  The terminal allows users to execute commands interactively. Whether you need to debug, analyze, or run Draw++ code, the terminal is equipped to handle it all.

- **Lexical and Syntax Analysis**:
  Perform lexical analysis using the `lex` command to tokenize Draw++ code and syntax analysis with the `parse` command to generate an abstract syntax tree (AST). These features help identify errors in the early stages of development.

  Example:
  ```
  draw++> lex var int x = 10;
  === Generated Tokens ===
  Token(type='VAR', value='var')
  Token(type='INT', value='int')
  Token(type='IDENTIFIER', value='x')
  Token(type='ASSIGN', value='=')
  Token(type='INTEGER', value='10')
  Token(type='SEMICOLON', value=';')
  ```

- **Debugging and Error Detection**:
  The terminal supports debugging with commands such as `debug` to analyze Draw++ files or inline code for errors. It provides detailed feedback, making error resolution straightforward.

  Example:
  ```
  draw++> debug example.dpp
  [INFO] Lexical Analysis Passed.
  [INFO] Syntax Analysis Passed.
  [INFO] No errors detected.
  ```

- **Command History**:
  Maintain a history of executed commands for easy reference and reuse. Use the `history` command to view previously executed commands.

- **File Management**:
  List available example files in the project directory using the `see` command or save processed data (source code, tokens, or AST) with the `save` command.

- **Customizable Execution**:
  The `run` command supports executing Draw++ source files or inline code directly. The terminal also compiles and runs the code seamlessly.

  Example:
  ```
  draw++> run -c "cursor c = create_cursor(0, 0); c.draw_circle(50, true);"
  Compiling...
  Running executable...
  [Output]: Circle drawn successfully.
  ```

### Integration with the Draw++ IDE

The terminal is tightly integrated with the Draw++ IDE, allowing developers to:
- Execute Draw++ code snippets or entire files.
- Debug and analyze code in real-time.
- Enhance productivity with interactive feedback and suggestions.
- Use advanced tools such as error correction, AST visualization, and dynamic compilation.

### Benefits

- **Real-Time Feedback**: Immediate insights into code behavior and errors.
- **Simplified Debugging**: Streamlined commands for analyzing and fixing issues.
- **Enhanced Productivity**: Combines the power of a traditional terminal with domain-specific tools for Draw++.