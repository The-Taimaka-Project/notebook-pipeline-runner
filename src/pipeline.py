from datetime import datetime
from time import sleep
from typing import List, Tuple
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter
from .colors import BOLD, CYAN, END, GREEN, RED, print_with_color


def run_notebook(notebook_path: str, output_dir: str):
    notebook_file_name = notebook_path.split('/')[-1]
    print_with_color("Running notebook: ", CYAN, True, notebook_file_name)

    # Load the Jupyter Notebook
    with open(notebook_path, 'r') as f:
        nb = nbformat.read(f, as_version=4)

    # Execute the Jupyter Notebook
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': '.'}})

    print_with_color("Notebook execution finished: ",
                     GREEN,
                     True,
                     notebook_file_name)

    # Export the Jupyter Notebook as an HTML file
    html_exporter = HTMLExporter()
    html_data, resources = html_exporter.from_notebook_node(nb)

    output_dir = output_dir + '/'
    print_with_color("Writing notebook to output directory: ", CYAN,
                     bold=True,
                     childText=output_dir + notebook_path.split('/')[-1] + ".html"
                     )

    # Write the HTML output to a file
    with open('{0}{1}.html'.format(output_dir, notebook_file_name), 'w') as f:
        f.write(html_data)


def run_pipeline(log_directory, output_dir, notebooks):
    print("Running pipeline... consisting of {0} notebooks\n".format(len(notebooks)))

    instance_log_directory = log_directory + '/instance_logs.log'
    error_logs_directory = log_directory + '/error_logs.log'

    log_result = []
    error_log_results = []

    index = 0
    for notebook in notebooks:
        print("Running Notebook {0} of {1} ===========================".format(index + 1, len(notebooks)))
        try:
            run_notebook(notebook, output_dir)
            log_result.append(notebook + " - Success")
        except Exception as e:
            log_result.append(notebook + " - Failed")
            error_log_results.append(notebook + " - Failed")
            error_log_results.append(str(e))

            print_with_color("Error running notebook: ",
                             RED, True,
                             "Halting pipeline execution. Please check the logs.")
            break

        index += 1
        # new line
        print("")

    _write_to_logs([(log_result, instance_log_directory), (error_log_results, error_logs_directory)])


def _write_to_logs(log: List[Tuple]):
    def write_log_file(log_array, log_name):
        if len(log_array) == 0:
            return

        print()
        with open(log_name, 'a') as f:
            f.write("==================================================================================\n")
            for log in log_array:
                f.write(log + " - " + str(datetime.now()) + '\n')

    for log_array, log_name in log:
        write_log_file(log_array, log_name)
