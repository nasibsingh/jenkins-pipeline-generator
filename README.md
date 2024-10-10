# Jenkins Pipeline Generator

This repository contains two Python scripts, `frontend-pipeline-generator.py` and `backend-pipeline-generator.py`, that automate the creation of Jenkins pipelines for frontend and backend projects, respectively. The scripts prompt the user for various inputs and generate Groovy pipeline scripts based on the provided data.

## Files:
- `frontend-pipeline-generator.py`: Generates a Jenkins pipeline for frontend projects, allowing users to customize stages such as building, deploying to AWS S3, and more.
- `backend-pipeline-generator.py`: Generates a Jenkins pipeline for backend services, including stages for Docker image creation, pushing to AWS ECR, and ECS service deployment.

## Features:
- **Frontend Pipeline Generator** (`frontend-pipeline-generator.py`):
  - Prompts for pipeline name, Git repository URL, branch name, Slack channel for notifications, build commands, and AWS S3 bucket name.
  - Allows customization of build commands and deployment paths.
  - Asks whether the pipeline is for production, and if so, includes a confirmation prompt before deploying to production.

- **Backend Pipeline Generator** (`backend-pipeline-generator.py`):
  - Prompts for pipeline name, repository details, AWS account and region, ECS cluster and service names, and Docker image information.
  - Generates a pipeline that builds a Docker image, pushes it to ECR, creates a new ECS task definition, and deploys the service.
  - Asks whether the pipeline is for production, and if so, includes a confirmation prompt before deploying.

## Usage:

### Running the Frontend Pipeline Generator
To generate a frontend pipeline:
```bash
python3 frontend-pipeline-generator.py
```

### Running the Backend Pipeline Generator
To generate a backend pipeline:
```bash
python3 backend-pipeline-generator.py
```

The script will ask for the following inputs:

### Frontend Pipeline Inputs:
  - Pipeline Name: Name of the Jenkins pipeline.
  - Git Repository URL: URL of the Git repository.
  - Default Branch Name: The default branch for the pipeline.
  - Jenkins Credentials ID: ID for accessing the Git repository.
  - Slack Channel Name: Slack channel for build notifications.
  - Build Commands: Commands to run in the build stage.
  - S3 Bucket Name: AWS S3 bucket for deployment.
    
### Backend Pipeline Inputs:
  - Pipeline Name: Name of the Jenkins pipeline.
  - Git Repository URL: URL of the Git repository.
  - Default Branch Name: The default branch for the pipeline.
  - Jenkins Credentials ID: ID for accessing the Git repository.
  - Slack Channel Name: Slack channel for build notifications.
  - Build Commands: Commands to run in the build stage.
  - Docker Image Name: Name of the Docker image.
  - AWS Account ID: AWS account ID for ECR.
  - AWS Region: Region of AWS resources.
  - ECS Cluster Name: Name of the ECS cluster.
  - ECS Service Name: Name of the ECS service.
  - Task Definition Name: Name of the ECS task associated with the service.
    
### Example Output:
The generated pipeline script will be saved as `pipeline_name_pipeline.groovy` in the current directory.

License:
This project is licensed under the MIT License.
