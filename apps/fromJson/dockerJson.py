import argparse
import json
import os


def generate_docker_compose(json_files, output_dir, output_filename):
    docker_compose = []

    # Add version and services
    docker_compose.append("version: '3'\n\nservices:\n")

    # Track services to detect duplicate attributes
    service_names = []

    # Generate services from JSON configuration files
    for json_file in json_files:
        try:
            with open(json_file, 'r') as file:
                config = json.load(file)

            for service_name, service_config in config.items():
                # Check for duplicate service names
                if service_name in service_names:
                    print(
                        f"Warning: Duplicate service name '{service_name}' in '{json_file}'. Skipping.")
                    continue

                # Add service name to the list
                service_names.append(service_name)

                docker_compose.append(f"  {service_name}:\n")
                docker_compose.append("    image: {}\n".format(
                    service_config.get('image', '')))
                docker_compose.append("    ports:\n")
                for port in service_config.get('ports', []):
                    docker_compose.append(f"      - {port}\n")
                docker_compose.append("    command: {}\n".format(
                    service_config.get('command', '')))
                docker_compose.append("\n")
        except FileNotFoundError:
            print(f"Error: JSON file '{json_file}' not found.")
            return
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{json_file}'.")
            return

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Determine the output path
    output_path = os.path.join(output_dir, output_filename)

    try:
        # Save the Docker Compose file
        with open(output_path, "w") as file:
            file.writelines(docker_compose)
        print(f"Docker Compose file '{output_path}' generated successfully!")
    except IOError:
        print(
            f"Error: Failed to write Docker Compose file '{output_path}'. Check the output directory.")
        return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Docker Compose YAML Generator')
    parser.add_argument('-j', '--json', nargs='+', type=str,
                        help='Path to JSON configuration file(s)')
    parser.add_argument('-o', '--output', type=str, default='./',
                        help='Output directory for Docker Compose file')
    parser.add_argument('-f', '--filename', type=str, default='docker-compose.yml',
                        help='Output filename for Docker Compose file')
    args = parser.parse_args()

    if args.json:
        generate_docker_compose(args.json, args.output, args.filename)
    else:
        print("Please provide at least one JSON configuration file using the '-j' or '--json' argument.")
