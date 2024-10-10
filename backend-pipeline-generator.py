def generate_pipeline():
    # Collect inputs from the user
    pipeline_name = input("Enter the pipeline name: ")
    repository_url = input("Enter the Git repository URL: ")
    default_branch = input("Enter the default branch name: ")
    credentials_id = input("Enter the Jenkins credentials ID for Git: ")
    slack_channel = input("Enter the Slack channel name: ")
    build_command_1 = input("Enter the command1 to run in the Build stage: ")
    build_command_2 = input("Enter the command2 to run in the Build stage: ")
    image_name = input("Enter the docker image name: ")
    account_id = input("Enter the account id: ")
    region = input("Enter the region of the aws resource: ")
    cluster_name = input("Enter the ECS cluster name: ")
    service_name = input("Enter the name of the ECS service associated with the cluster: ")
    task_name = input("Enter the name of the task associated with the service: ")
    task_definition_file_name = input("Enter the name of the task-definition file: ")


    # Ask if this is a production-level pipeline
    is_production = input("Is this a production-level pipeline? (yes/no): ").lower()

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
        ACCOUNT_ID = '{account_id}'
        BUILD_USER = ''
    
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
                        message: "${{JOB_NAME}} Api Build Initiated by ${{BUILD_USER}}"
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
                //Build image
                sh '{build_command_1}'
                sh '{build_command_2}'
            }}
        }}

        stage('Publish') {{
            steps {{
                script {{
                    // Update the current stage for tracking
                    currentStage = 'Publish'
                    }}
                    //Login to AWS ECR
                    sh 'aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.{region}.amazonaws.com'
                    //Push image to ECR
                    sh 'docker tag {image_name}:$BUILD_NUMBER $ACCOUNT_ID.dkr.ecr.{region}.amazonaws.com/{image_name}:$BUILD_NUMBER'
                    sh 'docker push $ACCOUNT_ID.dkr.ecr.{region}.amazonaws.com/{image_name}:$BUILD_NUMBER'
                }}
            }}

        stage('Create revision') {{
            steps {{
                script {{
                    // Update the current stage for tracking
                    currentStage = 'Create revision'
                }}
    """
    
    # If it's a production pipeline, add a prompt for confirmation in the Deploy stage
    if is_production == "yes":
        pipeline_template += """
                // Add a confirmation input prompt for production deployments
                input(message: 'Do you want to deploy the image?', ok: 'Deploy')
        """

    # Continue with the deployment steps
    pipeline_template += f"""
                //create revision
                script {{
                    sh '''
                        cluster="{cluster_name}"
                        service_name="{service_name}"
                        TASK="{task_name}"
                        ECR_IMAGE="$ACCOUNT_ID.dkr.ecr.{region}.amazonaws.com/{task_name}:$BUILD_NUMBER"
                    
                        sed -i "s|:ECR_IMAGE|${{ECR_IMAGE}}|g" ./infrastructure/{task_definition_file_name}.json
                        
                        task_revision=$(aws ecs register-task-definition --region {region} --cli-input-json file://infrastructure/{task_definition_file_name}.json)
                        task_revision_data=$(echo $task_revision | jq '.taskDefinition.revision')
                        
                        NEW_SERVICE=$(aws ecs update-service --cluster $cluster --service $service_name --task-definition $TASK --force-new-deployment)
                        echo "${{TASK}}, Revision: ${{task_revision_data}}"
                        
                        aws ecs wait services-stable --cluster $cluster --services $service_name
                    '''
                }}
            }}
        }}
    }}

    post{{
        success {{
            script {{
                // Get the build user again in case of success
                BUILD_USER = getBuildUser()
            }}
            // Send success message to Slack
            slackSend channel: '{slack_channel}',
                        color: COLOR_MAP['SUCCESS'], // Green color for success
                        message: "SUCCESS: ${{JOB_NAME}} API Build ${{env.BUILD_NUMBER}} succeeded by ${{BUILD_USER}}"
        }}
        failure {{
            script {{
                // Get the build user again in case of success
                BUILD_USER = getBuildUser()
            }}
            // Send failure message to Slack with the failed stage
            slackSend channel: '{slack_channel}',
                      color: COLOR_MAP['FAILURE'], // Red color for failure
                      message: "FAILURE: ${{JOB_NAME}} API Build ${{env.BUILD_NUMBER}} failed in *${{currentStage}}* stage by ${{BUILD_USER}}"
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
