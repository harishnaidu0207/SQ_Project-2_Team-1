import boto3
import zipfile
import os

# Package the Lambda function with multiple files or dependencies
def create_lambda_zip(function_name, file_list):
    with zipfile.ZipFile(f'{function_name}.zip', 'w') as lambda_zip:
        for file_name in file_list:
            lambda_zip.write(file_name)

# Create or update the Lambda function
def deploy_lambda_function(function_name, zip_file, role_arn, handler_name, runtime='python3.8'):
    client = boto3.client('lambda')

    try:
        with open(zip_file, 'rb') as f:
            zipped_code = f.read()

        # Check if the function already exists
        try:
            response = client.get_function(FunctionName=function_name)
            function_exists = True
        except client.exceptions.ResourceNotFoundException:
            function_exists = False

        if function_exists:
            # Update the function code
            response = client.update_function_code(
                FunctionName=function_name,
                ZipFile=zipped_code,
            )
            print(f'Lambda function {function_name} updated successfully.')
        else:
            # Create the function
            response = client.create_function(
                FunctionName=function_name,
                Runtime=runtime,
                Role=role_arn,
                Handler=handler_name,
                Code=dict(ZipFile=zipped_code),
                Timeout=120,  # Adjust the timeout as needed (increased to 120s)
                MemorySize=256,  # Adjust the memory size as needed (increased to 256MB)
            )
            print(f'Lambda function {function_name} created successfully.')

    except Exception as e:
        print(f'Error creating/updating Lambda function: {str(e)}')

# Deployment parameters
function_name = 'LambdaIngestionFunction'
file_list = ['upload_to_s3_lambda.py'] 
zip_file = f'{function_name}.zip'
role_arn = 'arn:aws:iam::637423377183:role/proj5role'
handler_name = 'upload_to_s3_lambda.lambda_handler'

# Create the ZIP package and deploy
create_lambda_zip(function_name, file_list)
deploy_lambda_function(function_name, zip_file, role_arn, handler_name)

# Clean up only the zip file
os.remove(zip_file)
