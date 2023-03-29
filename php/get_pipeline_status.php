<?php

header('Content-Type: application/json');

function readLastNonBlankLine($file) {
    $awkCommand = "awk 'NF{non_blank_line=$0}END{print non_blank_line}' " . escapeshellarg($file);
    $lastNonBlankLine = shell_exec($awkCommand);

    return $lastNonBlankLine;
}

function parseLine($line) {
    $filename = '';
    $failed = false;

    if (preg_match('/([^\/]+\.ipynb)/', $line, $matches)) {
        $filename = $matches[1];
    }

    if (strpos($line, 'Failed') !== false) {
        $failed = true;
    }

    return ['filename' => $filename, 'failed' => $failed];
}

$logFile = '../logs/instance_logs.log';
$lastNonBlankLine = readLastNonBlankLine($logFile);
if ($lastNonBlankLine !== false) {
    $result = parseLine($lastNonBlankLine);
    echo json_encode(['status' => 'success', 'result' => $result]);
} else {
    echo json_encode(['status' => 'error', 'message' => 'Unable to read the log file.']);
}

?>