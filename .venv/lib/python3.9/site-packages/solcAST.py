import subprocess
import json


def get_ast(solidity_file_path):
    command = [
        "solc",
        "--ast-compact-json",
        solidity_file_path
    ]
    # put the subprocess in a try...except in case solc fails
    try:
        result = subprocess.run(
            command, # a list of strings that specifies the program to run and its arguments
            capture_output=True, # capture command output
            text=True, # decoding to strings
            check=False  # Change to False to see the output even if an error occurs
        )

        # Extract only the JSON part from the stdout string
        json_start = result.stdout.find("{")
        json_end = result.stdout.rfind("}") + 1
        json_string = result.stdout[json_start:json_end]

        # This is the stream where a program sends its regular, non-error output. In this case, a successful solc run would send the JSON Abstract Syntax Tree (AST) to stdout.
        print("STDOUT:", result.stdout)

        # This is a separate stream specifically for error messages, warnings, and diagnostic information. If your Solidity code has a syntax error, solc would typically write the error details to stderr, not stdout.
        print("STDERR:", result.stderr)

        # stdout is a JSON structured string and ast_json converts it to to a native python dictionary (or list automatically, but it is a dictionary in this case)
        ast_json = json.loads(json_string)
        print("Successfully accessed the AST!")
        return ast_json

    # This block catches the error that happens when the json.loads() function fails to parse its input string.
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
    # This block is designed to catch the error that occurs when the operating system can't find the program you're trying to execute.
    except FileNotFoundError:
        print("Error: 'solc' command not found. Is it installed and in your PATH?")



