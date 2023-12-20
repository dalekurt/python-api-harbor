import os

def generate_project_structure():
    # Generate server directory structure
    generate_server_structure()

    # Generate worker directory structure
    generate_worker_structure()

    # Generate frontend directory structure
    generate_frontend_structure()

def generate_server_structure():
    server_structure = [
        ("server/app/routes", "__init__.py"),
        ("server/app/routes", "api.py"),
        ("server/app/workflows", "__init__.py"),
        ("server/app/workflows", "api_workflow.py"),
        ("server/app", "__init__.py"),
        ("server/app", "models.py"),
        ("server/config", "__init__.py"),
        ("server/config", "development.py"),
        ("server", "requirements.txt"),
        ("server", "run.py"),
    ]

    generate_structure("server", server_structure)

def generate_worker_structure():
    worker_structure = [
        ("worker/tasks", "__init__.py"),
        ("worker/tasks", "worker_tasks.py"),
        ("worker/config", "__init__.py"),
        ("worker/config", "celery_config.py"),
        ("worker", "requirements.txt"),
        ("worker", "run_worker.py"),
    ]

    generate_structure("worker", worker_structure)

def generate_frontend_structure():
    frontend_structure = [
        ("frontend/public", "index.html"),
        ("frontend/src/components", "__init__.py"),
        ("frontend/src/components", "Component1.js"),
        ("frontend/src/components", "Component2.js"),
        ("frontend/src", "App.js"),
        ("frontend/src", "index.js"),
        ("frontend", "package.json"),
        ("frontend", ".gitignore"),
    ]

    generate_structure("frontend", frontend_structure)

def generate_structure(base_path, structure):
    for folder, file in structure:
        path = os.path.join(base_path, folder)
        os.makedirs(path, exist_ok=True)
        open(os.path.join(path, file), 'w').close()
        print(f"Generated file: {os.path.join(folder, file)}")

if __name__ == "__main__":
    generate_project_structure()
