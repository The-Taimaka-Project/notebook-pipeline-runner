# Notebook Pipeline Runner

## Requirements

Make sure you have `pip3` and `python3` installed. If you don't, run

`sudo apt update`

and then

`sudo apt-get install python3-pip`.

Then, install the requirements by running

`pip3 install -r requirements.txt`

Then type

`python3 main.py`.

### Requirements.txt * IMPORTANT *

Requirements.txt is a file that contains all the dependencies for the program. Right now, it contains
dependencies needed to run the dummy-test notebooks. Everywhere an external library is used in the notebooks,
you must add it to requirements.txt.

Make sure you add *all* libraries used in the notebooks into the requirements.txt file. If you don't,
the program WILL cause an error mid-pipeline.

When you've added, type `pip3 install -r requirements.txt` to install these dependencies into your environment.

### To bypass confirmation

Bypass the confirmation prompt by typing

`python3 main.py --bypass-confirm`.

### Modifying the Pipeline

To modify the pipeline, edit the `main.py` file. The `main.py` file contains the main function, which
contains an array called `notebooks`, which contains the path to each notebook that will be run
and in what order they will be run. Modify this array to your liking.

## To Run as CRON Job

In the terminal, run

`pwd` to get the path to the directory containing the main.py file.

Then type

`crontab -e`.

This will open the crontab file in your default text editor. It will most likely be Vim.
Press `i` to enter insert mode, and then add the following line to the file:

`0 0 * * * python3 /path/to/main.py --bypass-confirm`

Replace `/path/to/main.py` with the actual path to the main.py file. Then press `esc`, type
`:wq`, and press `enter` to save and exit the file.

You should be good to go. The program will now run every day at midnight.
If you want to modify the date/time at which it runs, you can check out [https://crontab.guru/](crontab.guru).


## Testing

To run the test script that verifies the program will not run multiple instances
concurrently:

`chmod +x test.sh`

`./test.sh`
