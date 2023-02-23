#!/bin/bash

# Run the Python script twice in the background
python3 main.py arg1 arg2 &
python3 main.py arg3 arg4 &

# Wait for both instances to complete
wait

# There should be an error which indicates that it is running twice