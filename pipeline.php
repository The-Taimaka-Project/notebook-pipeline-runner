<?php

enum PipelineState: String {
    case Running = "Running";
    case Completed = "Completed";
    case Failed = "Failed";
}

$path_to_history_log = './history.log';
$path_to_state_file = './state.txt';

function logStatus($return_code, $output) {
    global $path_to_history_log, $path_to_state_file;

    $state = $return_code == 0 ? PipelineState::Completed : PipelineState::Failed;

    file_put_contents($path_to_state_file, $state . date('Y-m-d H:i:s'), LOCK_EX);
    file_put_contents($path_to_history_log, $state . date('Y-m-d H:i:s'), FILE_APPEND);

    return array('status' => $state, 'output' => implode("\n", $output));
}

// add an argument to the function to pass the notebook name
function runNotebook($notebook) {
    global $path_to_history_log, $path_to_state_file;
    $command = 'jupyter nbconvert --to html ' . $notebook;
    $timeout = 20 * 60; // in seconds

    set_time_limit($timeout);
    exec($command, $output, $return_code);
    return logStatus($return_code, $output);
}

$notebooks = array('notebook1.ipynb', 'notebook2.ipynb', 'notebook3.ipynb');
$path_to_lock_file = './pipeline.lock';

if(!file_exists($path_to_lock_file) && flock($path_to_lock_file, LOCK_EX | LOCK_NB)) {
    global $notebooks, $path_to_lock_file, $path_to_state_file;

    file_put_contents($path_to_lock_file, date('Y-m-d H:i:s'));
    file_put_contents($path_to_state_file, PipelineState::Running . date('Y-m-d H:i:s'), LOCK_EX);

    $result = array();
    $result = runPipeline();

    foreach ($notebooks as $notebook) {
        $output = runNotebook($notebook);
        $result[$notebook] = $output;
    }

    file_put_contents($path_to_state_file, PipelineState::Completed . date('Y-m-d H:i:s'), LOCK_EX);

    header('Content-Type: application/json');
    echo json_encode($result);

    flock($path_to_lock_file, LOCK_UN);
} else {
    // Return an error indicating that the pipeline is already running
    header('Content-Type: application/json');
    echo json_encode(array('status' => 'Error', 'output' => 'Pipeline is already running'));
}

?>
