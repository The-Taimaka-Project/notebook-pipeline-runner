<?php

header('Content-Type: application/json');

function lineOnlyContainsEqualSigns($line) {
    return preg_match('/^=+$/', trim($line));
}

function readLastSection($file) {
    $fp = fopen($file, 'r');
    if (!$fp) {
        return false;
    }

    $buffer = '';
    $section = '';
    fseek($fp, 0, SEEK_END);
    $pos = -1;

    while (fseek($fp, $pos, SEEK_END) !== -1) {
        $char = fgetc($fp);
        $buffer = $char . $buffer;
        if ($char === "\n") {
            if (lineOnlyContainsEqualSigns($buffer)) {
                break;
            }
            $section = $buffer . $section;
            $buffer = '';
        }
        $pos--;
    }

    fclose($fp);
    return $section;
}

function parseLines($lines) {
    $parsedLines = [];

    foreach (explode("\n", trim($lines)) as $line) {
        if (preg_match('/([^\/]+\.ipynb) - (Success|Failed) - (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)/', $line, $matches)) {
            $parsedLines[] = [
                'name' => $matches[1],
                'status' => $matches[2] . ' at ' . $matches[3],
            ];
        }
    }

    return $parsedLines;
}

$logFile = '../logs/instance_logs.log';
$lastSection = readLastSection($logFile);
if ($lastSection !== false) {
    $pipeline = parseLines($lastSection);
    $overallStatus = count($pipeline) > 0 && strpos($pipeline[0]['status'], 'Failed') === false ? 'Success' : 'Failure';
    echo json_encode(['status' => $overallStatus, 'pipeline' => $pipeline, 'count' => count($pipeline)]);
} else {
    echo json_encode(['status' => 'error', 'message' => 'Unable to read the log file.']);
}

?>
