import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys 
import argparse
from functions.get_files_info import schema_get_files_info, schema_get_file_content, schema_write_file
from functions.run_python_file import schema_run_python_file
from call_function import call_function, available_functions
from config import AI_LOOP_LIMIT




def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="The query string") 
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    
    if not args.query:  # Check if query was provided
        print("Error: query string is required")
        sys.exit(1)
    load_dotenv()
    


    currentIterations = 0    
    isVerbose = args.verbose 
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    messageList = []
    messageList.append(sys.argv[1])
    print(f'debug: {messageList}')
    
    while(currentIterations < AI_LOOP_LIMIT):
    
        
        try:
            response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents= messageList,
            config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt)
        
            )

            if(isVerbose):
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print("Response tokens:", response.usage_metadata.candidates_token_count)
            
            if response.function_calls is not None:
                for function_call_part in response.function_calls:
                    modelMessage = f'I want to call: {function_call_part.name}'
                    print(modelMessage)
                    messageList.append(modelMessage)
                    function_call_result = call_function(function_call_part, isVerbose )
                    ToolMessage = f"Here's the result of {function_call_part.name}"
                    messageList.append(modelMessage)
                    ToolResult = function_call_result.parts[0].function_response.response['result']
                    print(f"{ToolResult}")
                    messageList.append(ToolResult)
            else:
                return response.text
                break
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
        
            
            # for function_call_part in response.function_calls:
            #     function_call_result = call_function(function_call_part, isVerbose )
                
            #     print(f"- {function_call_result.parts[0].function_response.response['result']}")
        
        currentIterations = currentIterations + 1

    
    # if(isVerbose):
    #     print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    #     print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    # if not response.function_calls:
    #     return response.text
    
    # for function_call_part in response.function_calls:
    #     function_call_result = call_function(function_call_part, isVerbose )
    #     print(f"- {function_call_result.parts[0].function_response.response['result']}")
    # print("Hello from pycodeagent!")
    sys.exit(0)


if __name__ == "__main__":
    main()
