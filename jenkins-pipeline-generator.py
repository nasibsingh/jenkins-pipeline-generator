def generate_pipeline():
    # Collect inputs from the user
    pipeline_name = input("Enter the pipeline name: ")
    repository_url = input("Enter the Git repository URL: ")
    default_branch = input("Enter the default branch name: ")
    credentials_id = input("Enter the Jenkins credentials ID for Git: ")
    slack_channel = input("Enter the Slack channel name: ")
    s3_bucket = input("Enter the S3 bucket name for deployment: ")
    build_command_1 = input("Enter the command1 to run in the Build stage: ")
    build_command_2 = input("Enter the command2 to run in the Build stage: ")
    source_location = input("Enter the source location for the AWS S3 cp command: ")

    # Define the template for the pipeline script
    pipeline_template = f"""
pipeline {{
    agent any

    stages {{
        stage('Build') {{
            steps {{
                sh '{build_command_1}'
                sh '{build_command_2}'
            }}
        }}
        stage('Deploy') {{
            steps {{
                sh "aws s3 cp {source_location} s3://{s3_bucket}/ --recursive"
            }}
        }}
    }}
}}
"""

    # Write to file
    with open(f"{pipeline_name}_pipeline.groovy", "w") as file:
        file.write(pipeline_template)

    print(f"Pipeline script {pipeline_name}_pipeline.groovy generated successfully.")

# Run generator
generate_pipeline()
