def execute_python_file(file, python_version='3.10'):
    """Execute a Python file in a Docker container and return the output"""
    workspace_folder = "auto_gpt_workspace"

    try:
        print(f"Executing file '{file}' in workspace '{workspace_folder}'")

        if not file.endswith(".py"):
            raise ValueError("Invalid file type. Only .py files are allowed.")

        file_path = os.path.join(workspace_folder, file)

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File '{file}' does not exist.")

        client = docker.from_env()

        container = client.containers.run(
            f'python:{python_version}',
            f'python {file}',
            volumes={
                os.path.abspath(workspace_folder): {
                    'bind': '/workspace',
                    'mode': 'ro'}},
            working_dir='/workspace',
            stderr=True,
            stdout=True,
            detach=True,
        )

        output = container.wait()
        logs = container.logs().decode('utf-8')
        container.remove()

        return logs

    except ValueError as ve:
        return f"Error: {str(ve)}"
    except FileNotFoundError as fe:
        return f"Error: {str(fe)}"
    except docker.errors.ImageNotFound as ine:
        return f"Error: {str(ine)}"
    except docker.errors.APIError as ae:
        return f"Error: {str(ae)}"
    except Exception as e:
        return f"Error: {str(e)}"
