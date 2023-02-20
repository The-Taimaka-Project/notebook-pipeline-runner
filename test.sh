#!/bin/bash

# Run the Python script twice in the background
python3 pipeline.py arg1 arg2 &
python3 pipeline.py arg3 arg4 &

# Wait for both instances to complete
wait
