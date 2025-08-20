import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Execute Python files with optional arguments, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                type=types.Type.STRING,
                description="Optional arguments to pass to the Python file.",
                )
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    
    full_path = os.path.join(working_directory, file_path)
    abs_working_dir = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)

    if not abs_full_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if(os.path.exists(abs_full_path) is not True):
        return f'Error: File "{file_path}" not found.'
    
    if(abs_full_path.endswith('.py') is not True):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        processResults=  subprocess.run(["python", abs_full_path] + args, timeout=30, capture_output=True )
        print(f'stdout: {processResults.stdout}')
        print(f'stderr: {processResults.stderr}')
        if(processResults.check_returncode):
            return f'STDOUT:{processResults.stdout} STDERR:{processResults.stderr}, "Process exited with code X"'
        else:
            return f'STDOUT:{processResults.stdout} STDERR:{processResults.stderr}, "No output produced"'
    except Exception as err:
        return(f"Error: executing Python file: {err}")
        raise

    pass