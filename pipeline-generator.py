import tkinter as tk
from tkinter import messagebox, Scrollbar

class PipelineForm(tk.Frame):
    def __init__(self, parent, pipeline_type):
        super().__init__(parent)
        self.pipeline_type = pipeline_type
        self.inputs = {}

        # Title of the window
        self.label = tk.Label(self, text=f"Enter details for {pipeline_type} Pipeline")
        self.label.pack(pady=10)

        # Create a scrollable canvas
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Add the form fields inside the scrollable frame
        self.create_form()

        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def create_form(self):
        self.fields = {}
        
        # Common fields for both pipelines
        common_fields = [
            "Pipeline Name", "Repository URL", "Default Branch", "Credentials ID",
            "Slack Channel", "Build Command 1", "Build Command 2", "Is Production (yes/no)"
        ]
        backend_specific_fields = [
            "Docker Image Name", "Account ID", "Region", 
            "ECS Cluster Name", "ECS Service Name", "Task Name", "Task Definition File"
        ]
        frontend_specific_fields = ["S3 Bucket", "Source Location"]

        fields_to_create = common_fields + (frontend_specific_fields if self.pipeline_type == "Frontend" else backend_specific_fields)

        # Dynamically create labels and entry widgets for all fields inside scrollable frame
        for field in fields_to_create:
            label = tk.Label(self.scrollable_frame, text=field)
            label.pack(pady=5)
            entry = tk.Entry(self.scrollable_frame, width=50)
            entry.pack(pady=5)
            self.fields[field] = entry

        # Submit button at the very end of the form
        self.submit_button = tk.Button(self.scrollable_frame, text="Submit", command=self.preview_inputs)
        self.submit_button.pack(pady=20)

    def preview_inputs(self):
        # Gather input from all fields
        for field, entry in self.fields.items():
            self.inputs[field] = entry.get()

        # Preview the inputs before generating the pipeline
        preview_message = "\n".join([f"{key}: {value}" for key, value in self.inputs.items()])
        
        confirm = messagebox.askyesno("Confirm Inputs", f"Please review the provided inputs:\n\n{preview_message}\n\nDo you want to proceed?")

        if confirm:
            if self.pipeline_type == "Frontend":
                generate_frontend_pipeline_script(self.inputs)
            else:
                generate_backend_pipeline_script(self.inputs)
            root.destroy()
        else:
            # If not confirmed, the user can modify inputs
            pass

def generate_frontend_pipeline_script(inputs):
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
        BUILD_USER = '' // Store the user who triggered the build
        currentStage = '' // Track the current stage
    }}

    parameters {{
        gitParameter branchFilter: 'origin/(.*)', defaultValue: '{inputs['Default Branch']}', name: 'BRANCH', type: 'PT_BRANCH'
    }}

    stages {{
        stage('Initialise') {{
            steps {{
                script {{
                    // Get the build user and set the current stage to 'Initialise'
                    BUILD_USER = getBuildUser()
                    currentStage = 'Initialise'
                }}
                // Send notification to Slack when the build starts
                slackSend channel: '{inputs['Slack Channel']}',
                          color: 'warning',
                          message: "${{JOB_NAME}} Build Initiated by ${{BUILD_USER}}"
            }}
        }}
        
        stage('Clone') {{
            steps {{
                script {{
                    // Update the current stage for tracking
                    currentStage = 'Clone'
                }}
                // Clone the selected branch using provided credentials and repository URL
                git branch: "${{params.BRANCH}}", credentialsId: '{inputs['Credentials ID']}', url: '{inputs['Repository URL']}'
            }}
        }}

        stage('Build') {{
            steps {{
                script {{
                    // Update the current stage for tracking
                    currentStage = 'Build'
                }}
                // Execute the customized build commands
                sh '{inputs['Build Command 1']}'
                sh '{inputs['Build Command 2']}'
            }}
        }}

        stage('Deploy') {{
            steps {{
                script {{
                    // Update the current stage for tracking
                    currentStage = 'Deploy'
                }}
                sh "aws s3 cp {inputs['Source Location']} s3://{inputs['S3 Bucket']}/ --recursive"
            }}
        }}
    }}

    post {{
        success {{
            script {{
                // Get the build user again in case of success
                BUILD_USER = getBuildUser()
            }}
            // Send success message to Slack
            slackSend channel: '{inputs['Slack Channel']}', color: COLOR_MAP['SUCCESS'], message: "SUCCESS: ${{JOB_NAME}} Build ${{env.BUILD_NUMBER}} succeeded by ${{BUILD_USER}}"
        }}
        failure {{
            script {{
                // Get the build user again in case of failure
                BUILD_USER = getBuildUser()
            }}
            // Send failure message to Slack with the failed stage
            slackSend channel: '{inputs['Slack Channel']}', color: COLOR_MAP['FAILURE'], message: "FAILURE: ${{JOB_NAME}} Build ${{env.BUILD_NUMBER}} failed in *${{currentStage}}* stage by ${{BUILD_USER}}"
        }}
    }}
}}
"""
    if inputs["Is Production (yes/no)"].lower() == "yes":
        pipeline_template = pipeline_template.replace("stage('Deploy') {{", "stage('Deploy') {{\ninput message: 'Do you want to deploy?', ok: 'Deploy'")
    
    with open(f"{inputs['Pipeline Name']}_frontend_pipeline.groovy", "w") as file:
        file.write(pipeline_template)

    messagebox.showinfo("Success", f"Frontend pipeline '{inputs['Pipeline Name']}' generated successfully!")

def generate_backend_pipeline_script(inputs):
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
                    // Get the build user and set the current stage to 'Initialise'
                    BUILD_USER = getBuildUser()
                    currentStage = 'Initialise'
                }}
                // Send notification to Slack when the build starts
                slackSend channel: '{inputs['Slack Channel']}',
                          color: 'warning',
                          message: "${{JOB_NAME}} API Build Initiated by ${{BUILD_USER}}"
            }}
        }}

        stage('Clone') {{
            steps {{
                script {{
                    // Update the current stage for tracking
                    currentStage = 'Clone'
                }}
                // Clone the selected branch using provided credentials and repository URL
                git branch: "${{params.BRANCH}}", credentialsId: '{inputs['Credentials ID']}', url: '{inputs['Repository URL']}'
            }}
        }}

        stage('Build') {{
            steps {{
                script {{
                    // Update the current stage for tracking
                    currentStage = 'Build'
                }}
                //Build image
                sh '{inputs['Build Command 1']}'
                sh '{inputs['Build Command 2']}'
            }}
        }}

        stage('Publish') {{
            steps {{
                script {{
                    // Update the current stage for tracking
                    currentStage = 'Publish'
                    }}
                    //Login to AWS ECR
                    sh 'aws ecr get-login-password --region {inputs['Region']} | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.{inputs['Region']}.amazonaws.com'
                    //Push image to ECR
                    sh 'docker tag {inputs['Docker Image Name']}:$BUILD_NUMBER $ACCOUNT_ID.dkr.ecr.{inputs['Region']}.amazonaws.com/{inputs['Docker Image Name']}:$BUILD_NUMBER'
                    sh 'docker push $ACCOUNT_ID.dkr.ecr.{inputs['Region']}.amazonaws.com/{inputs['Docker Image Name']}:$BUILD_NUMBER'
            }}
        }}

        stage('Deploy') {{
            steps {{
                script {{
                    // Update the current stage for tracking
                    currentStage = 'Create revision'
                }}
                //create revision
                sh '''
                    cluster="{inputs['ECS Cluster Name']}"
                    service_name="{inputs['ECS Service Name']}"
                    TASK="{inputs['Task Name']}"
                    ECR_IMAGE="$ACCOUNT_ID.dkr.ecr.{inputs['Region']}.amazonaws.com/{inputs['Task Name']}:$BUILD_NUMBER"
                    
                    sed -i "s|:ECR_IMAGE|${{ECR_IMAGE}}|g" ./infrastructure/{inputs['Task Definition File']}.json
                    
                    task_revision=$(aws ecs register-task-definition --region {inputs['Region']} --cli-input-json file://infrastructure/{inputs['Task Definition File']}.json)
                    task_revision_data=$(echo $task_revision | jq '.taskDefinition.revision')

                    NEW_SERVICE=$(aws ecs update-service --cluster $cluster --service $service_name --task-definition $TASK --force-new-deployment)
                    echo "${{TASK}}, Revision: ${{task_revision_data}}"

                    aws ecs wait services-stable --cluster $cluster --services $service_name
                '''
            }}
        }}
    }}

    post {{
        success {{
            script {{
                // Get the build user again in case of success
                BUILD_USER = getBuildUser()
            }}
            // Send success message to Slack
            slackSend channel: '{inputs['Slack Channel']}', color: COLOR_MAP['SUCCESS'], message: "SUCCESS: ${{JOB_NAME}} API Build ${{env.BUILD_NUMBER}} succeeded by ${{BUILD_USER}}"
        }}
        failure {{
            script {{
                // Get the build user again in case of success
                BUILD_USER = getBuildUser()
            }}
            // Send failure message to Slack with the failed stage
            slackSend channel: '{inputs['Slack Channel']}', color: COLOR_MAP['FAILURE'], message: "FAILURE: ${{JOB_NAME}} API Build ${{env.BUILD_NUMBER}} failed in *${{currentStage}}* stage by ${{BUILD_USER}}"
        }}
    }}
}}
"""

    if inputs["Is Production (yes/no)"].lower() == "yes":
        pipeline_template = pipeline_template.replace("stage('Deploy') {{", "stage('Deploy') {{\ninput message: 'Do you want to deploy?', ok: 'Deploy'")

    with open(f"{inputs['Pipeline Name']}_backend_pipeline.groovy", "w") as file:
        file.write(pipeline_template)

    messagebox.showinfo("Success", f"Backend pipeline '{inputs['Pipeline Name']}' generated successfully!")

# Main program
def open_pipeline_form(pipeline_type):
    form_window = tk.Toplevel(root)
    form_window.geometry("500x800")
    form = PipelineForm(form_window, pipeline_type)
    form.pack(fill="both", expand=True)

# Set up the main GUI window
root = tk.Tk()
root.title("Jenkins Pipeline Generator")
root.geometry("500x150")

# Create buttons for frontend and backend pipeline generation
frontend_button = tk.Button(root, text="Generate Frontend Pipeline", command=lambda: open_pipeline_form("Frontend"), width=50)
backend_button = tk.Button(root, text="Generate Backend Pipeline", command=lambda: open_pipeline_form("Backend"), width=50)

# Place buttons in the main window
frontend_button.pack(pady=20)
backend_button.pack(pady=20)

# Start the GUI loop
root.mainloop()
