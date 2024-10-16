import os
import sys

def run_frontend_generator():
    """Runs the frontend pipeline generator script."""
    os.system("python3 frontend-pipeline-generator.py")

def run_backend_generator():
    """Runs the backend pipeline generator script."""
    os.system("python3 backend-pipeline-generator.py")

def main():
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        # Ask the user which pipeline they want to create
        print("Which pipeline do you want to generate?")
        print("1. Frontend Pipeline")
        print("2. Backend Pipeline")

        choice = input("Enter 1 for Frontend or 2 for Backend: ")

        if choice == "1":
            print("Generating Frontend Pipeline...")
            run_backend_generator()
            break
        elif choice == "2":
            print("Generating Backend Pipeline...")
            run_backend_generator()
            break
        else:
            attempts +=1
            print(f"Invalid input. You have {max_attempts - attempts} attempts left. Please enter 1 or 2.")
    
    if attempts == max_attempts:
        print("Too many invalid attempts. Exiting program.")
        sys.exit(1)

if __name__ == "__main__":
    main()
