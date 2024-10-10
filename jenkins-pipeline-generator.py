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
    agent any // Define agent

    environment {{
        BUILD_USER = '' // Store the user who triggered the build
        currentStage = '' // Track the current stage
    }}

    parameters {{
        // Allow customization of branch name with a default value
        gitParameter branchFilter: 'origin/(.*)', defaultValue: '{default_branch}', name: 'BRANCH', type: 'PT_BRANCH'
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
                slackSend channel: '{slack_channel}',
                          color: 'warning', // Color for warning
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
                git branch: "${{params.BRANCH}}", credentialsId: '{credentials_id}', url: '{repository_url}'
            }}
        }}

        stage('Build') {{
            steps {{
                script {{
                    // Update the current stage for tracking
                    currentStage = 'Build'
                }}
                // Execute the customized build command
                sh '{build_command_1}'
                sh '{build_command_2}'
            }}
        }}

        stage('Deploy') {{
            steps {{
                script {{
                    // Update the current stage for tracking
                    currentStage = 'Deploy'
                }}
                // Deploy the build artifacts to S3 using the provided bucket name and source location
                sh "aws s3 cp {source_location} s3://{s3_bucket}/ --recursive"
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
            slackSend channel: '{slack_channel}',
                      color: COLOR_MAP['SUCCESS'], // Green color for success
                      message: "SUCCESS: ${{JOB_NAME}} Build ${{env.BUILD_NUMBER}} succeeded by ${{BUILD_USER}}"
        }}
        failure {{
            script {{
                // Get the build user again in case of failure
                BUILD_USER = getBuildUser()
            }}
            // Send failure message to Slack with the failed stage
            slackSend channel: '{slack_channel}',
                      color: COLOR_MAP['FAILURE'], // Red color for failure
                      message: "FAILURE: ${{JOB_NAME}} Build ${{env.BUILD_NUMBER}} failed in *{{currentStage}}* stage by ${{BUILD_USER}}"
        }}
    }}
}}
"""

    # Write the generated pipeline script to a file
    with open(f"{pipeline_name}_pipeline.groovy", "w") as file:
        file.write(pipeline_template)
    
    print(f"Pipeline script {pipeline_name}_pipeline.groovy generated successfully.")

# Run the pipeline generator
generate_pipeline()
