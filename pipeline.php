<?php
/**
 * File name: pipeline.php
 * Purpose:
 *  To run a data pipeline consisting of multiple Jupyter notebooks
 *  while preventing concurrent runs and maintaining logs.
 * Created: February 4, 2023
 */

enum PipelineState: String {
    case RUNNING = "Running";
    case COMPLETED = "Completed";
    case FAILED = "Failed";
}

enum Result: String {
    case SUCCESS = "Success";
    case FAILURE = "Failure";
}

$path_to_history_log = './history.log';
$path_to_state_file = './state.txt';
$path_to_lock_file = './pipeline.lock';

/**
 * *****************************************************************************
 *                            Helper Functions
 * *****************************************************************************
 */

function logStatus($return_code, $output) {
    global $path_to_history_log, $path_to_state_file;

    $state = $return_code == 0 ? PipelineState::COMPLETED : PipelineState::FAILED;

    file_put_contents($path_to_state_file, $state . date('Y-m-d H:i:s'), LOCK_EX);
    file_put_contents($path_to_history_log, $state . date('Y-m-d H:i:s'), FILE_APPEND);

    return array('status' => $state, 'output' => implode("\n", $output));
}

function respondAndExit($status, $output) {
    header('Content-Type: application/json');
    echo json_encode(array('status' => $status, 'output' => $output));
    exit;
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

function runPipeline($notebooks, $path_to_lock_file, $path_to_state_file) {
    file_put_contents($path_to_lock_file, date('Y-m-d H:i:s'));
    file_put_contents($path_to_state_file, PipelineState::Running . date('Y-m-d H:i:s'), LOCK_EX);

    $result = array();
    $result = runPipeline();

    foreach ($notebooks as $notebook) {
        $output = runNotebook($notebook);
        $result[$notebook] = $output;
    }

    file_put_contents($path_to_state_file, PipelineState::Completed . date('Y-m-d H:i:s'), LOCK_EX);

    return result;
}

/**
 * *****************************************************************************
 *                        Helper Functions End
 * *****************************************************************************
 */

/**
 * Main Script
 */

$fp = fopen($path_to_lock_file, 'c');

if(!flock($fp, LOCK_EX | LOCK_NB)) {
    respondAndExit(Result::FAILURE, 'Pipeline is already running');
}

if(file_exists($path_to_lock_file)) {
    $pid = file_get_contents($path_to_lock_file);

    if(posix_kill($pid, 0)) {
        respondAndExit(Result::FAILURE, 'Pipeline is already running');
    } else {
        unlink($path_to_lock_file));
        respondAndExit(Result::FAILURE, 'Lockfile was stale, removed it. Please try again.');
    }
}

file_put_contents($path_to_lock_file, getmypid());

$notebooks = array('notebook1.ipynb', 'notebook2.ipynb', 'notebook3.ipynb');
$result = runPipeline($notebooks, $path_to_state_file);

header('Content-Type: application/json');
echo json_encode($result);


unlink($lockfile);
flock($fp, LOCK_UN);
fclose($fp);

?>
