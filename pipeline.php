<?php

$history = './history.log';
$state = './state.txt';
$jupyter_notebook_path = './notebook.ipynb';

// add an argument to the function to pass the notebook name
function runNotebook($notebook) {
    global $history, $state, $jupyter_notebook_path;
    $command = 'jupyter nbconvert --to html ' . $notebook;

    exec($command, $output, $returnValue);

    if ($returnValue == 0) {
        file_put_contents($state, 'Completed');
        file_put_contents($history, 'Success: ' . date('Y-m-d H:i:s'), FILE_APPEND);

        return array('status' => 'Success', 'output' => implode("\n", $output));
    } else {
        file_put_contents($state, 'Failed');
        file_put_contents($history, 'Failed: ' . date('Y-m-d H:i:s'), FILE_APPEND);

        return array('status' => 'Failed', 'output' => implode("\n", $output));
    }
}

$notebooks = array('notebook1.ipynb', 'notebook2.ipynb', 'notebook3.ipynb');
$lock_file = './pipeline.lock';

if (!file_exists($lock_file)) {
    global $notebooks, $lock_file, $state;

    //put the date into the lock file
    file_put_contents($lock_file, date('Y-m-d H:i:s'));
    file_put_contents($state, 'Running');

    $result = array();
    $result = runPipeline();

    foreach ($notebooks as $notebook) {
        $output = runNotebook($notebook);
        $result[$notebook] = $output;
    }

    unlink($lock_file);

    header('Content-Type: application/json');
    echo json_encode($result);
} else {
    // Return an error indicating that the pipeline is already running
    header('Content-Type: application/json');
    echo json_encode(array('status' => 'Error', 'output' => 'Pipeline is already running'));
}

?>
