import os

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
    if not abs_full_path.startswith(abs_working_dir):
        return f'Error: Cannot read  "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abs_full_path):
        return f'Error: "{abs_full_path}" is not a directory'
    
    #Todo Finish stuff later fill out the rest of the function to CH2l3

    pass