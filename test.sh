#!/bin/bash

# Run the Python script twice in the background
python3 main.py &
python3 main.py &

# Wait for both instances to complete
wait

# There should be an error which indicates that it is running twice