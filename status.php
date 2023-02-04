<?php

$path_to_history_log = './history.log';
$path_to_state_file = './state.txt';

function getPipelineState() {
    global $path_to_state_file;
    if (file_exists($path_to_state_file)) {
        return file_get_contents($stateFile);
    }
    return 'Not available';
}

function getLatestLogFile() {
    global $path_to_history_log;
    $logFiles = array_diff(scandir($path_to_history_log), array('.', '..'));
    if (count($logFiles) > 0) {
        sort($logFiles);
        return $logFiles[count($logFiles) - 1];
    }
    return 'Not available';
}

$state = getPipelineState();
$logFile = getLatestLogFile();

header('Content-Type: application/json');
echo json_encode(array('state' => $state, 'logFile' => $logFile));

?>
