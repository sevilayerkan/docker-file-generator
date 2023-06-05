import argparse
import json
import os
from rich import print
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()


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
                    console.print(
                        f"[yellow]Warning:[/yellow] Duplicate service name '{service_name}' in '{json_file}'. Skipping.")
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
            console.print(
                f"[red]Error:[/red] JSON file '{json_file}' not found.")
            return
        except json.JSONDecodeError:
            console.print(
                f"[red]Error:[/red] Invalid JSON format in '{json_file}'.")
            return

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Determine the output path
    output_path = os.path.join(output_dir, output_filename)

    try:
        # Save the Docker Compose file
        with open(output_path, "w") as file:
            file.writelines(docker_compose)
        console.print(
            f"[green]Docker Compose file '{output_path}' generated successfully![/green]")
    except IOError:
        console.print(
            f"[red]Error:[/red] Failed to write Docker Compose file '{output_path}'. Check the output directory.")
        return


def select_json_files():
    console.print("[bold]JSON File Selection[/bold]")
    console.print(
        "Enter the JSON file paths separated by commas, or press Enter to skip:"
    )
    json_files = Prompt.ask("> ", default="")

    if not json_files:
        console.print("JSON file selection skipped.")
        return []

    json_files = [f.strip() for f in json_files.split(",")]
    return json_files


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Docker Compose YAML Generator')
    parser.add_argument('-o', '--output', type=str, default='./',
                        help='Output directory for Docker Compose file')
    parser.add_argument('-f', '--filename', type=str, default='docker-compose.yml',
                        help='Output filename for Docker Compose file')
    args = parser.parse_args()

    json_files = select_json_files()
    output_dir = args.output
    output_filename = args.filename

    generate_docker_compose(json_files, output_dir, output_filename)

    # Wait for user input to exit
    input("Press Enter to exit...")
    