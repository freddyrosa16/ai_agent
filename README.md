If you've ever used **Cursor** or **Claude Code** as an agentic AI editor, you'll understand what we're building in this project.

We're building a toy version of Claude Code using Google's free Gemini API! As long as you have access to a large language model (LLM), it's surprisingly simple to build a (somewhat) effective custom agent.

## 🧠 What Does the Agent Do?

This project is a command-line interface (CLI) tool that:

- Accepts a coding task.

- Chooses from a set of predefined functions to complete the task, such as:

- Scanning the files in a directory

- Reading a file's contents

- Overwriting a file's contents

- Executing a Python file using the interpreter

- Repeats step 2 until the task is complete (or it fails — which is totally possible!).

## 🔧 Example Usage

Say you have a buggy calculator app, and you want the agent to fix it:

```bash

python3 main.py "fix my calculator app, its not starting correctly"
```

Output (Example):

```bash

- Calling function: get_files_info

- Calling function: get_file_content

- Calling function: write_file

- Calling function: run_python_file

- Calling function: write_file

- Calling function: run_python_file

- Final response:

- Great! The calculator app now seems to be working correctly. The output shows the expression and the result in a formatted way.
```

## 📦 Prerequisites

Python 3.10+ installed

Access to a Unix-like shell (e.g. zsh or bash)

## 🎯 Learning Goals

Introduce you to multi-directory Python projects

Help you understand how AI tools you'll likely use on the job actually work under the hood

Improve your Python and functional programming skills

## 🚫 The goal is not to build an LLM from scratch, but to use a pre-trained LLM to build an agent from scratch.
