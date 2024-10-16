import tkinter as tk
from tkinter import simpledialog, messagebox

# Function to preview the input data and ask for confirmation
def preview_and_confirm(pipeline_name, inputs, generate_function):
    preview_message = "\n".join([f"{key}: {value}" for key, value in inputs.items()])
    
    confirm = messagebox.askyesno("Confirm Inputs", f"Please review the provided inputs:\n\n{preview_message}\n\nDo you want to proceed?")
    
    if confirm:
        # If confirmed, call the pipeline generation function
        generate_function(pipeline_name, inputs)
    else:
        # If not confirmed, restart the input process
        if "frontend" in pipeline_name.lower():
            generate_frontend_pipeline()
        else:
            generate_backend_pipeline()

# Function to generate frontend pipeline script
def generate_frontend_pipeline():
    pipeline_name = simpledialog.askstring("Input", "Enter the pipeline name:")
    inputs = {
        "Repository URL": simpledialog.askstring("Input", "Enter the Git repository URL:"),
        "Default Branch": simpledialog.askstring("Input", "Enter the default branch name:"),
        "Credentials ID": simpledialog.askstring("Input", "Enter the Jenkins credentials ID for Git:"),
        "Slack Channel": simpledialog.askstring("Input", "Enter the Slack channel name:"),
        "S3 Bucket": simpledialog.askstring("Input", "Enter the S3 bucket name for deployment:"),
        "Build Command 1": simpledialog.askstring("Input", "Enter the command1 to run in the Build stage:"),
        "Build Command 2": simpledialog.askstring("Input", "Enter the command2 to run in the Build stage:"),
        "Source Location": simpledialog.askstring("Input", "Enter the source location for the AWS S3 cp command:"),
        "Is Production": simpledialog.askstring("Input", "Is this a production-level pipeline? (yes/no)").lower()
    }

    preview_and_confirm(pipeline_name, inputs, generate_frontend_pipeline_script)

# Function to generate backend pipeline script
def generate_backend_pipeline():
    pipeline_name = simpledialog.askstring("Input", "Enter the pipeline name:")
    inputs = {
        "Repository URL": simpledialog.askstring("Input", "Enter the Git repository URL:"),
        "Default Branch": simpledialog.askstring("Input", "Enter the default branch name:"),
        "Credentials ID": simpledialog.askstring("Input", "Enter the Jenkins credentials ID for Git:"),
        "Slack Channel": simpledialog.askstring("Input", "Enter the Slack channel name:"),
        "Build Command 1": simpledialog.askstring("Input", "Enter the command1 to run in the Build stage:"),
        "Build Command 2": simpledialog.askstring("Input", "Enter the command2 to run in the Build stage:"),
        "Docker Image Name": simpledialog.askstring("Input", "Enter the Docker image name:"),
        "Account ID": simpledialog.askstring("Input", "Enter the AWS account ID:"),
        "Region": simpledialog.askstring("Input", "Enter the AWS region:"),
        "ECS Cluster Name": simpledialog.askstring("Input", "Enter the ECS cluster name:"),
        "ECS Service Name": simpledialog.askstring("Input", "Enter the ECS service name:"),
        "Task Name": simpledialog.askstring("Input", "Enter the ECS task name:"),
        "Task Definition File": simpledialog.askstring("Input", "Enter the task definition file name:"),
        "Is Production": simpledialog.askstring("Input", "Is this a production-level pipeline? (yes/no)").lower()
    }

    preview_and_confirm(pipeline_name, inputs, generate_backend_pipeline_script)

# Function to actually generate the frontend pipeline script after confirmation
def generate_frontend_pipeline_script(pipeline_name, inputs):
    pipeline_template = f"""
import groovy.json.JsonOutput

def COLOR_MAP = [
    'SUCCESS': 'good',
    'ALERT': 'warning',
    'FAILURE': 'danger'
]

// Function to get the user who triggered the build
def getBuildUser() {{
    def userCause = currentBuild.rawBuild.getCause(Cause.UserIdCause)
    return userCause ? userCause.getUserId() : "Automated/Unknown"
}}

pipeline {{
    agent any

    environment {{
        BUILD_USER = ''
    }}

    parameters {{
        gitParameter branchFilter: 'origin/(.*)', defaultValue: '{inputs['Default Branch']}', name: 'BRANCH', type: 'PT_BRANCH'
    }}

    stages {{
        stage('Initialise') {{
            steps {{
                script {{
                    BUILD_USER = getBuildUser()
                }}
                slackSend channel: '{inputs['Slack Channel']}',
                          color: 'warning',
                          message: "${{JOB_NAME}} Build Initiated by ${{BUILD_USER}}"
            }}
        }}
        
        stage('Clone') {{
            steps {{
                git branch: "${{params.BRANCH}}", credentialsId: '{inputs['Credentials ID']}', url: '{inputs['Repository URL']}'
            }}
        }}

        stage('Build') {{
            steps {{
                sh '{inputs['Build Command 1']}'
                sh '{inputs['Build Command 2']}'
            }}
        }}

        stage('Deploy') {{
            steps {{
                sh "aws s3 cp {inputs['Source Location']} s3://{inputs['S3 Bucket']}/ --recursive"
            }}
        }}
    }}

    post {{
        success {{
            slackSend channel: '{inputs['Slack Channel']}', color: COLOR_MAP['SUCCESS'], message: "SUCCESS: ${{JOB_NAME}} Build succeeded"
        }}
        failure {{
            slackSend channel: '{inputs['Slack Channel']}', color: COLOR_MAP['FAILURE'], message: "FAILURE: ${{JOB_NAME}} Build failed"
        }}
    }}
}}
"""

    # If it's a production pipeline, add a confirmation step before deployment
    if inputs["Is Production"] == "yes":
        pipeline_template = pipeline_template.replace("stage('Deploy') {{", "stage('Deploy') {{\ninput message: 'Do you want to deploy?', ok: 'Deploy'")

    # Write to a file
    with open(f"{pipeline_name}_frontend_pipeline.groovy", "w") as file:
        file.write(pipeline_template)

    messagebox.showinfo("Success", f"Frontend pipeline '{pipeline_name}' generated successfully!")

# Function to actually generate the backend pipeline script after confirmation
def generate_backend_pipeline_script(pipeline_name, inputs):
    pipeline_template = f"""
import groovy.json.JsonOutput

def COLOR_MAP = [
    'SUCCESS': 'good',
    'ALERT': 'warning',
    'FAILURE': 'danger'
]

// Function to get the user who triggered the build
def getBuildUser() {{
    def userCause = currentBuild.rawBuild.getCause(Cause.UserIdCause)
    return userCause ? userCause.getUserId() : "Automated/Unknown"
}}

pipeline {{
    agent any

    environment {{
        ACCOUNT_ID = '{inputs['Account ID']}'
        BUILD_USER = ''
    }}

    parameters {{
        gitParameter branchFilter: 'origin/(.*)', defaultValue: '{inputs['Default Branch']}', name: 'BRANCH', type: 'PT_BRANCH'
    }}

    stages {{
        stage('Initialise') {{
            steps {{
                script {{
                    BUILD_USER = getBuildUser()
                }}
                slackSend channel: '{inputs['Slack Channel']}',
                          color: 'warning',
                          message: "${{JOB_NAME}} API Build Initiated by ${{BUILD_USER}}"
            }}
        }}

        stage('Clone') {{
            steps {{
                git branch: "${{params.BRANCH}}", credentialsId: '{inputs['Credentials ID']}', url: '{inputs['Repository URL']}'
            }}
        }}

        stage('Build') {{
            steps {{
                sh '{inputs['Build Command 1']}'
                sh '{inputs['Build Command 2']}'
            }}
        }}

        stage('Publish') {{
            steps {{
                sh 'aws ecr get-login-password --region {inputs['Region']} | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.{inputs['Region']}.amazonaws.com'
                sh 'docker tag {inputs['Docker Image Name']}:$BUILD_NUMBER $ACCOUNT_ID.dkr.ecr.{inputs['Region']}.amazonaws.com/{inputs['Docker Image Name']}:$BUILD_NUMBER'
                sh 'docker push $ACCOUNT_ID.dkr.ecr.{inputs['Region']}.amazonaws.com/{inputs['Docker Image Name']}:$BUILD_NUMBER'
            }}
        }}

        stage('Deploy') {{
            steps {{
                sh '''
                    cluster="{inputs['ECS Cluster Name']}"
                    service_name="{inputs['ECS Service Name']}"
                    TASK="{inputs['Task Name']}"
                    ECR_IMAGE="$ACCOUNT_ID.dkr.ecr.{inputs['Region']}.amazonaws.com/{inputs['Task Name']}:$BUILD_NUMBER"
                    
                    sed -i "s|:ECR_IMAGE|${{ECR_IMAGE}}|g" ./infrastructure/{inputs['Task Definition File']}.json
                    
                    task_revision=$(aws ecs register-task-definition --cli-input-json file://infrastructure/{inputs['Task Definition File']}.json --region {inputs['Region']} --query 'taskDefinition.revision')
                    aws ecs update-service --cluster $cluster --service $service_name --region {inputs['Region']} --task-definition {inputs['Task Name']}:$task_revision
                '''
            }}
        }}
    }}

    post {{
        success {{
            slackSend channel: '{inputs['Slack Channel']}', color: COLOR_MAP['SUCCESS'], message: "SUCCESS: ${{JOB_NAME}} API Build succeeded"
        }}
        failure {{
            slackSend channel: '{inputs['Slack Channel']}', color: COLOR_MAP['FAILURE'], message: "FAILURE: ${{JOB_NAME}} API Build failed"
        }}
    }}
}}
"""

    # If it's a production pipeline, add a confirmation step before deployment
    if inputs["Is Production"] == "yes":
        pipeline_template = pipeline_template.replace("stage('Deploy') {{", "stage('Deploy') {{\ninput message: 'Do you want to deploy?', ok: 'Deploy'")

    # Write to a file
    with open(f"{pipeline_name}_backend_pipeline.groovy", "w") as file:
        file.write(pipeline_template)

    messagebox.showinfo("Success", f"Backend pipeline '{pipeline_name}' generated successfully!")

# Set up the GUI window
root = tk.Tk()
root.title("Jenkins Pipeline Generator")

# Create buttons for frontend and backend pipeline generation
frontend_button = tk.Button(root, text="Generate Frontend Pipeline", command=generate_frontend_pipeline, width=40)
backend_button = tk.Button(root, text="Generate Backend Pipeline", command=generate_backend_pipeline, width=40)

# Place buttons in the window
frontend_button.pack(pady=20)
backend_button.pack(pady=20)

# Start the GUI loop
root.mainloop()
