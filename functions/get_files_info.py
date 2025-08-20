import os
from config import MAX_CHARS
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents, in the specifed file, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(  
                type=types.Type.STRING,
                description="Read file contents, in the specifed directory, relative to the working directory.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes file contents, in the specifed file, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Writes file contents, in the specifed directory, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Writes file contents, in the specifed directory, relative to the working directory.",
            ),
        },
    ),
)



def get_files_info(working_directory, directory="."):
    
    #if not os.path.isdir(directory):
        #return f'Error: "{directory}" is not a directory' 

    full_path = os.path.join(working_directory, directory)
    abs_working_dir = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)
    if not os.path.isdir(abs_full_path):
        return f'Error: "{abs_full_path}" is not a directory'
    
    if not abs_full_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
     
    #get dir files 
    directoryItems = os.listdir(abs_full_path)
    returnString = ""
    for item in directoryItems:
        itemDirectory = os.path.join(abs_full_path, item)
        returnString += f"- {item}: file_size={os.path.getsize(itemDirectory)}, is_dir={os.path.isfile(itemDirectory)!= True}\n"

    return returnString


def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_working_dir = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)
    
    if os.path.isfile(abs_full_path) != True:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    if not abs_full_path.startswith(abs_working_dir):
        return f'Error: Cannot read  "{file_path}" as it is outside the permitted working directory'
    
    #print(f"Test: {abs_full_path}")

    file_content_string =""
    try:
        if(os.stat(abs_full_path).st_size > MAX_CHARS):
            print(f'File "{file_path}" truncated at 10000 characters')
        with open(abs_full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    
    return file_content_string

def write_file(working_directory, file_path, content):

    full_path = os.path.join(working_directory, file_path)
    abs_working_dir = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)



    if not abs_full_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    getDirName = os.path.dirname(abs_full_path)
    os.makedirs(getDirName, exist_ok=True)
    
    try:

        with open(abs_full_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as err:
        return(f"Error: {err=}, {type(err)=}")
        raise
 

    
    #Todo Finish stuff later fill out the rest of the function to CH2l3

    pass