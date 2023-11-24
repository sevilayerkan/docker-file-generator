import glob
import os
import json
from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'



@app.route('/', methods=['GET', 'POST'])


def index():
    if request.method == 'POST':
        json_files = request.form.getlist('json_files')
        uploaded_files = request.files.getlist('uploaded_files')
        output_dir = request.form.get('output_dir', './')
        output_filename = request.form.get(
            'output_filename', 'docker-compose.yml')

        if not json_files and not uploaded_files:
            flash("Please select or upload at least one JSON file.", "error")
            return redirect('/')

        all_files = json_files + save_uploaded_files(uploaded_files)

        if not any(file.endswith('.json') for file in all_files):
            flash("No valid JSON files selected or uploaded.", "error")
            return redirect('/')

        generate_docker_compose(all_files, output_dir, output_filename)
        return redirect('/success')

    json_directory = './json_files'
    json_files = get_json_files(json_directory)

    return render_template('index.html', json_files=json_files)

@app.route('/success')
def success():
    return render_template('success.html')


def get_json_files(directory):
    json_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files


def save_uploaded_files(files):
    saved_files = []
    for file in files:
        if file.filename:
            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            saved_files.append(file_path)
    return saved_files


def generate_docker_compose(json_files, output_dir, output_filename):
    docker_compose = []

    docker_compose.append("version: '3'\n\nservices:\n")

    service_names = []

    for json_file in json_files:
        try:
            with open(json_file, 'r') as file:
                config = json.load(file)

            for service_name, service_config in config.items():
                if service_name in service_names:
                    flash(f"Warning: Duplicate service name '{service_name}' in '{json_file}'. Skipping.")
                    continue

                service_names.append(service_name)

                docker_compose.append(f"  {service_name}:\n")
                docker_compose.append("    image: {}\n".format(service_config.get('image', '')))
                docker_compose.append("    ports:\n")
                for port in service_config.get('ports', []):
                    docker_compose.append(f"      - {port}\n")
                docker_compose.append("    command: {}\n".format(service_config.get('command', '')))
                docker_compose.append("\n")
        except FileNotFoundError:
            flash(f"Error: JSON file '{json_file}' not found.")
            return
        except json.JSONDecodeError:
            flash(f"Error: Invalid JSON format in '{json_file}'.")
            return

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)

    try:
        with open(output_path, "w") as file:
            file.writelines(docker_compose)
        flash(f"Docker Compose file '{output_path}' generated successfully!")
    except IOError:
        flash(f"Error: Failed to write Docker Compose file '{output_path}'. Check the output directory.")
        return


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
