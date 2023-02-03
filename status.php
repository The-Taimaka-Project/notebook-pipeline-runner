<?php

// Function to get the latest state of the data pipeline
function getPipelineState() {
    $stateFile = '/path/to/state/file';
    if (file_exists($stateFile)) {
        return file_get_contents($stateFile);
    }
    return 'Not available';
}

// Function to get the latest log filename of the data pipeline
function getLatestLogFile() {
    $logDirectory = '/path/to/log/directory';
    $logFiles = array_diff(scandir($logDirectory), array('.', '..'));
    if (count($logFiles) > 0) {
        sort($logFiles);
        return $logFiles[count($logFiles) - 1];
    }
    return 'Not available';
}

// Get the state and log information
$state = getPipelineState();
$logFile = getLatestLogFile();

// Return the state and log information as a JSON object
header('Content-Type: application/json');
echo json_encode(array('state' => $state, 'logFile' => $logFile));

?>
