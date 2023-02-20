from datetime import datetime
import fcntl
import os
from time import sleep
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter
from .colors import color


def run_notebook(notebook_path: str, output_dir: str):
    notebook_file_name = notebook_path.split('/')[-1]
    print(color.BOLD + color.CYAN + "Running notebook: " + notebook_file_name + color.END)

    # Load the Jupyter Notebook
    with open(notebook_path, 'r') as f:
        nb = nbformat.read(f, as_version=4)

    # Execute the Jupyter Notebook
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': '.'}})

    # Export the Jupyter Notebook as an HTML file
    html_exporter = HTMLExporter()
    html_data, resources = html_exporter.from_notebook_node(nb)

    output_dir = output_dir + '/'
    print(color.BOLD + "Writing notebook to output directory: " + output_dir +
          notebook_path.split('/')[-1] + ".html" + color.END)

    # Write the HTML output to a file
    with open('{0}{1}.html'.format(output_dir, notebook_file_name), 'w') as f:
        f.write(html_data)


def run_pipeline(log_file, output_dir, notebooks):
    log_result = []
    for notebook in notebooks:
        try:
            run_notebook(notebook, output_dir)
            log_result.append(notebook + " - Success")
        except Exception as e:
            log_result.append(notebook + " - Failed")
            print(e)

    with open(log_file, 'a') as f:
        for log in log_result:
            f.write(log + " - " + str(datetime.now()) + '\n')
