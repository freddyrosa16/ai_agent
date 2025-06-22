If you've ever used Cursor or Claude Code as an "agentic" AI editor, you'll understand what we're building in this project.

We're building a toy version of Claude Code using Google's free Gemini API! As long as you have an LLM at your disposal, its actually surprisingly simple to build a (somewhat) effective custom agent.

What Does the Agent Do?
The program we're building is a CLI tool that:

Accepts a coding task
Chooses from a set of predefined functions to work on the task, for example:
Scan the files in a directory
Read a file's contents
Overwrite a file's contents
Execute the python interpreter on a file
Repeats step 2 until the task is complete (or it fails miserably, which is possible)
For example, I have a buggy calculator app, so I used my agent to fix the code:

> python3 main.py "fix my calculator app, its not starting correctly"

# Calling function: get_files_info

# Calling function: get_file_content

# Calling function: write_file

# Calling function: run_python_file

# Calling function: write_file

# Calling function: run_python_file

# Final response:

# Great! The calculator app now seems to be working correctly. The output shows the expression and the result in a formatted way.

Prerequisites
Python 3.10+ installed
Access to a Unix-like shell (e.g. zsh or bash)
Learning Goals
The learning goals of this project are:

Introduce you to multi-directory Python projects
Understand how the AI tools that you'll almost certainly use on the job actually work under the hood
Practice your Python and functional programming skills
The goal is not to build an LLM from scratch, but to instead use a pre-trained LLM to build an agent from scratch.
