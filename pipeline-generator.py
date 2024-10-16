import tkinter as tk
from tkinter import messagebox
import logging
import subprocess

# Set up logging
logging.basicConfig(filename='pipeline_generator.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to run the frontend script with user inputs
def run_frontend_script(pipeline_name, repository_url, default_branch, credentials_id, slack_channel, s3_bucket, build_command_1, build_command_2, source_location):
    try:
        logging.info(f"Running frontend pipeline script for: {pipeline_name}")
        subprocess.run([
            "python3", "./frontend-pipeline-generator-v2.py", pipeline_name, repository_url, default_branch, credentials_id,
            slack_channel, s3_bucket, build_command_1, build_command_2, source_location
        ], check=True)
        messagebox.showinfo("Pipeline", f"Frontend pipeline {pipeline_name} executed successfully!")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing frontend script: {e}")
        messagebox.showerror("Error", "Error running frontend pipeline script")

# Function to run the backend script with user inputs
def run_backend_script(pipeline_name, repository_url, default_branch, credentials_id, slack_channel, build_command_1, build_command_2, image_name, account_id, region, cluster_name, service_name, task_name, task_definition_file_name):
    try:
        logging.info(f"Running backend pipeline script for: {pipeline_name}")
        subprocess.run([
            "python3", "./backend-pipeline-generator.py", pipeline_name, repository_url, default_branch, credentials_id,
            slack_channel, build_command_1, build_command_2, image_name, account_id, region, cluster_name, service_name, task_name,
            task_definition_file_name
        ], check=True)
        messagebox.showinfo("Pipeline", f"Backend pipeline {pipeline_name} executed successfully!")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing backend script: {e}")
        messagebox.showerror("Error", "Error running backend pipeline script")

# Function to handle frontend pipeline inputs
def frontend_pipeline():
    def submit():
        pipeline_name = entry_pipeline_name.get()
        repository_url = entry_repository_url.get()
        default_branch = entry_default_branch.get()
        credentials_id = entry_credentials_id.get()
        slack_channel = entry_slack_channel.get()
        s3_bucket = entry_s3_bucket.get()
        build_command_1 = entry_build_command_1.get()
        build_command_2 = entry_build_command_2.get()
        source_location = entry_source_location.get()

        run_frontend_script(pipeline_name, repository_url, default_branch, credentials_id, slack_channel, s3_bucket, build_command_1, build_command_2, source_location)
        pipeline_window.destroy()

    pipeline_window = tk.Toplevel(root)
    pipeline_window.title("Frontend Pipeline")

    # Input fields for frontend pipeline
    tk.Label(pipeline_window, text="Pipeline Name:").grid(row=0, column=0)
    entry_pipeline_name = tk.Entry(pipeline_window)
    entry_pipeline_name.grid(row=0, column=1)

    tk.Label(pipeline_window, text="Repository URL:").grid(row=1, column=0)
    entry_repository_url = tk.Entry(pipeline_window)
    entry_repository_url.grid(row=1, column=1)

    tk.Label(pipeline_window, text="Default Branch:").grid(row=2, column=0)
    entry_default_branch = tk.Entry(pipeline_window)
    entry_default_branch.grid(row=2, column=1)

    tk.Label(pipeline_window, text="Credentials ID:").grid(row=3, column=0)
    entry_credentials_id = tk.Entry(pipeline_window)
    entry_credentials_id.grid(row=3, column=1)

    tk.Label(pipeline_window, text="Slack Channel:").grid(row=4, column=0)
    entry_slack_channel = tk.Entry(pipeline_window)
    entry_slack_channel.grid(row=4, column=1)

    tk.Label(pipeline_window, text="S3 Bucket:").grid(row=5, column=0)
    entry_s3_bucket = tk.Entry(pipeline_window)
    entry_s3_bucket.grid(row=5, column=1)

    tk.Label(pipeline_window, text="Build Command 1:").grid(row=6, column=0)
    entry_build_command_1 = tk.Entry(pipeline_window)
    entry_build_command_1.grid(row=6, column=1)

    tk.Label(pipeline_window, text="Build Command 2:").grid(row=7, column=0)
    entry_build_command_2 = tk.Entry(pipeline_window)
    entry_build_command_2.grid(row=7, column=1)

    tk.Label(pipeline_window, text="Source Location:").grid(row=8, column=0)
    entry_source_location = tk.Entry(pipeline_window)
    entry_source_location.grid(row=8, column=1)

    submit_button = tk.Button(pipeline_window, text="Submit", command=submit)
    submit_button.grid(row=9, column=1)

# Function to handle backend pipeline inputs
def backend_pipeline():
    def submit():
        pipeline_name = entry_pipeline_name.get()
        repository_url = entry_repository_url.get()
        default_branch = entry_default_branch.get()
        credentials_id = entry_credentials_id.get()
        slack_channel = entry_slack_channel.get()
        build_command_1 = entry_build_command_1.get()
        build_command_2 = entry_build_command_2.get()
        image_name = entry_image_name.get()
        account_id = entry_account_id.get()
        region = entry_region.get()
        cluster_name = entry_cluster_name.get()
        service_name = entry_service_name.get()
        task_name = entry_task_name.get()
        task_definition_file_name = entry_task_definition_file_name.get()

        run_backend_script(pipeline_name, repository_url, default_branch, credentials_id, slack_channel, build_command_1, build_command_2, image_name, account_id, region, cluster_name, service_name, task_name, task_definition_file_name)
        pipeline_window.destroy()

    pipeline_window = tk.Toplevel(root)
    pipeline_window.title("Backend Pipeline")

    # Input fields for backend pipeline
    tk.Label(pipeline_window, text="Pipeline Name:").grid(row=0, column=0)
    entry_pipeline_name = tk.Entry(pipeline_window)
    entry_pipeline_name.grid(row=0, column=1)

    tk.Label(pipeline_window, text="Repository URL:").grid(row=1, column=0)
    entry_repository_url = tk.Entry(pipeline_window)
    entry_repository_url.grid(row=1, column=1)

    tk.Label(pipeline_window, text="Default Branch:").grid(row=2, column=0)
    entry_default_branch = tk.Entry(pipeline_window)
    entry_default_branch.grid(row=2, column=1)

    tk.Label(pipeline_window, text="Credentials ID:").grid(row=3, column=0)
    entry_credentials_id = tk.Entry(pipeline_window)
    entry_credentials_id.grid(row=3, column=1)

    tk.Label(pipeline_window, text="Slack Channel:").grid(row=4, column=0)
    entry_slack_channel = tk.Entry(pipeline_window)
    entry_slack_channel.grid(row=4, column=1)

    tk.Label(pipeline_window, text="Build Command 1:").grid(row=5, column=0)
    entry_build_command_1 = tk.Entry(pipeline_window)
    entry_build_command_1.grid(row=5, column=1)

    tk.Label(pipeline_window, text="Build Command 2:").grid(row=6, column=0)
    entry_build_command_2 = tk.Entry(pipeline_window)
    entry_build_command_2.grid(row=6, column=1)

    tk.Label(pipeline_window, text="Docker Image Name:").grid(row=7, column=0)
    entry_image_name = tk.Entry(pipeline_window)
    entry_image_name.grid(row=7, column=1)

    tk.Label(pipeline_window, text="Account ID:").grid(row=8, column=0)
    entry_account_id = tk.Entry(pipeline_window)
    entry_account_id.grid(row=8, column=1)

    tk.Label(pipeline_window, text="Region:").grid(row=9, column=0)
    entry_region = tk.Entry(pipeline_window)
    entry_region.grid(row=9, column=1)

    tk.Label(pipeline_window, text="Cluster Name:").grid(row=10, column=0)
    entry_cluster_name = tk.Entry(pipeline_window)
    entry_cluster_name.grid(row=10, column=1)

    tk.Label(pipeline_window, text="Service Name:").grid(row=11, column=0)
    entry_service_name = tk.Entry(pipeline_window)
    entry_service_name.grid(row=11, column=1)

    tk.Label(pipeline_window, text="Task Name:").grid(row=12, column=0)
    entry_task_name = tk.Entry(pipeline_window)
    entry_task_name.grid(row=12, column=1)

    tk.Label(pipeline_window, text="Task Definition File Name:").grid(row=13, column=0)
    entry_task_definition_file_name = tk.Entry(pipeline_window)
    entry_task_definition_file_name.grid(row=13, column=1)

    submit_button = tk.Button(pipeline_window, text="Submit", command=submit)
    submit_button.grid(row=14, column=1)

# Main window
root = tk.Tk()
root.title("Pipeline Generator")

# Buttons to select the pipeline type
frontend_button = tk.Button(root, text="Frontend Pipeline", command=frontend_pipeline)
frontend_button.pack()

backend_button = tk.Button(root, text="Backend Pipeline", command=backend_pipeline)
backend_button.pack()

# Start the GUI event loop
root.mainloop()
