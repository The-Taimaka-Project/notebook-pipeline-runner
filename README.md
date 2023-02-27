# Setup

Type:

`pip3 install -r requirements.txt`

Then type

`python3 main.py`.

For help, type

`python3 main.py -h`.

Bypass the confirmation prompt by typing

`python3 main.py --bypass-confirm`.

## To Run as CRON JOB

In the terminal, run

`pwd` to get the path to the directory containing the main.py file.

Then type

`crontab -e`.

This will open the crontab file in your default text editor. It will most likely be Vim.
Press `i` to enter insert mode, and then add the following line to the file:

`0 0 * * * python3 /path/to/main.py --bypass-confirm`

Replace `/path/to/main.py` with the actual path to the main.py file. Then press `esc`, type
`:wq`, and press `enter` to save and exit the file.

You should be good! : D

## Testing

To run the test script that verifies the program will not run multiple instances
concurrently:

`chmod +x test.sh`

`./test.sh`
