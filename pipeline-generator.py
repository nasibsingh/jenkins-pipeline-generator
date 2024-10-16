import os

def run_frontend_generator():
    """Runs the frontend pipeline generator script."""
    os.system("python3 frontend-pipeline-generator.py")

def run_backend_generator():
    """Runs the backend pipeline generator script."""
    os.system("python3 backend-pipeline-generator.py")

def main():
    # Ask the user which pipeline they want to create
    print("Which pipeline do you want to generate?")
    print("1. Frontend Pipeline")
    print("2. Backend Pipeline")

    choice = input("Enter 1 for Frontend or 2 for Backend: ")

    if choice == "1":
        print("Generating Frontend Pipeline...")
        run_backend_generator()
    elif choice == "2":
        print("Generating Backend Pipeline...")
        run_backend_generator()
    else:
        print("Invalid input. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
