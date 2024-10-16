# Pipeline Generator

This is a Python-based GUI application that allows users to generate Jenkins pipeline scripts for frontend and backend projects. The GUI provides an easy way to input the required details, preview the inputs, and generate the pipeline scripts based on the user's confirmation.

## Features:
- **Frontend Pipeline**: Generates a Jenkins pipeline script for frontend applications. Requires inputs such as repository URL, branch, S3 bucket, and build commands.

- **Backend Pipeline**: Generates a Jenkins pipeline script for backend services. Requires additional inputs such as Docker image name, ECS cluster and service details, and task definition information.

- **GUI Interface**: A user-friendly graphical interface allows for easy input of pipeline details.
 
- **Input Preview**: Before generating the pipeline, the user can preview all inputs and confirm or modify as needed.

- **Scroll Functionality**: The input section is scrollable to accommodate large sets of inputs.

- **Single Submission**: All questions for the pipeline are asked in one go with a single submit button at the end.

## Prerequisites:
- Python 3.11.x or higher
- `tkinter` installed (comes pre-installed with most Python distributions)

## How to Run:

1. Clone the repository:
```bash
git clone <repository-url>
cd pipeline-generator
```

2. Install dependencies: If you are missing `Tkinter`, install it based on your operating system:
  - **macOS**: Tkinter comes pre-installed.
  - **Ubuntu/Debian**: Install with `sudo apt-get install python3-tk`.
  - **Windows**: Tkinter is included with Python by default.


3. Run the program:
```bash
python3 pipeline-generator.py
```


## Usage:

1. On running the program, a window will pop up asking you to select whether to generate a **Frontend** or **Backend** pipeline.
2. Fill in all the required fields for the selected pipeline.
3. Once you have entered all details, a preview of your inputs will be shown.
4. Confirm the details or go back to make changes.
5. After confirmation, the pipeline script will be generated and saved in the current directory.

The script will ask for the following inputs:

### Frontend Pipeline Inputs:
    - Pipeline Name: Name of the Jenkins pipeline.
    - Git Repository URL: URL of the Git repository.
    - Default Branch Name: The default branch for the pipeline.
    - Jenkins Credentials ID: ID for accessing the Git repository.
    - Slack Channel Name: Slack channel for build notifications.
    - S3 Bucket Name: AWS S3 bucket for deployment.
    - Build Command1: Commands to run in the build stage.
    - Build Command2: Commands to run in the build stage.
    - AWS S3 Source Location: Source location for the S3 copy process.
    
### Backend Pipeline Inputs:
    - Pipeline Name: Name of the Jenkins pipeline.
    - Git Repository URL: URL of the Git repository.
    - Default Branch Name: The default branch for the pipeline.
    - Jenkins Credentials ID: ID for accessing the Git repository.
    - Slack Channel Name: Slack channel for build notifications.
    - Build Command1: Commands to run in the build stage.
    - Build Command2: Commands to run in the build stage.
    - Docker Image Name: Name of the Docker image.
    - AWS Account ID: AWS account ID for ECR.
    - AWS Region: Region of AWS resources.
    - ECS Cluster Name: Name of the ECS cluster.
    - ECS Service Name: Name of the ECS service.
    - Task Name: Name of the ECS task.
    - Task Definition Name: Name of the ECS task associated with the service.
    
### Contributing
Feel free to fork this repository and make any improvements. For major changes, please open an issue first to discuss what you would like to change.

### License
This project is licensed under the MIT License.
