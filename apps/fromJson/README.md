# Docker Compose YAML Generator

This script generates a Docker Compose YAML file based on JSON configuration files. It simplifies the process of creating a Docker Compose file for managing multi-container applications.

## Requirements

- Python 3.x

## Usage

1. Ensure you have Python 3.x installed on your system.

2. Download the `dockerJson.py` script.

3. Run the script with the desired command-line options:

    ```bash
    dockerJson.py -j config1.json config2.json -o /path/to/output -f docker-compose.yml
    ```

    The script accepts the following command-line options:

    - `-j` or `--json`: Path to one or more JSON configuration files. Separate multiple file paths with spaces.

    - `-o` or `--output`: Output directory for the Docker Compose file. (Default: current directory)

    - `-f` or `--filename`: Output filename for the Docker Compose file. (Default: docker-compose.yml)

    - `-d` or `--json-dir`: Directory path for JSON configuration files. Use this option if the JSON files are located in a different directory.

4. The script will generate the Docker Compose YAML file based on the provided JSON configuration files and save it in the specified output directory with the specified filename.

5. The generated Docker Compose file can be used to deploy and manage your multi-container application using Docker Compose.

## JSON Configuration File Format

The JSON configuration files should follow a specific format to define the services and their attributes in the Docker Compose file.

Here's an example of a valid JSON configuration file:

```json
{
  "web":
  {
    "image": "nginx:latest",
    "ports": ["80:80"]
  },
  "db":
  {
    "image": "mysql:latest",
    "ports": ["3306:3306"],
    "command": "--default-authentication-plugin=mysql_native_password"
  }
}
```

## Usage

```bash
python dockerJson.py -j flask-psql.json flask-redis.json
```

```bash
python dockerJson.py -j  templates/flask-psql.json templates/flask-redis.json -o ./result -f compose.yml
```

## Notes

Each service in the Docker Compose file is defined as a key-value pair in the JSON object.

The key represents the service name, and the value is an object containing the service attributes.

Supported service attributes include:

`image` (string): The Docker image to use for the service.
`ports` (list of strings): The port mappings for the service.
`command` (string): The command to run when starting the service.
You can define multiple services in a single JSON configuration file.

Note that duplicate service names are not allowed. If a duplicate service name is detected, the script will skip the duplicate entry.
