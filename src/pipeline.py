from datetime import datetime
import fcntl
import os
from time import sleep
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter


def run_notebook(notebook_path: str):
    # Load the Jupyter Notebook
    with open(notebook_path, 'r') as f:
        nb = nbformat.read(f, as_version=4)

    # Execute the Jupyter Notebook
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': '.'}})

    # Export the Jupyter Notebook as an HTML file
    html_exporter = HTMLExporter()
    html_data, resources = html_exporter.from_notebook_node(nb)

    # Write the HTML output to a file
    with open('%s.html'.format(notebook_path), 'w') as f:
        f.write(html_data)


def run_pipeline(log_file, notebooks):
    log_result = []
    for notebook in notebooks:
        try:
            run_notebook(notebook)
            log_result.append(notebook + " - Success")
        except Exception as e:
            log_result.append(notebook + " - Failed")
            print(e)

    with open(log_file, 'w') as f:
        for log in log_result:
            f.write(log + " - " + str(datetime.now()))
