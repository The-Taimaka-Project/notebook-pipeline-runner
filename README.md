# Notebook Pipeline Runner

- Runs a pipeline of Jupyter Notebooks
- Prevents multiple instances of the program from running concurrently
- Log and error handling
- Emails the user when the pipeline is complete or if an error occurs


## Requirements

Requires python version 3.12 or greater. Recommend you create a virtual environment using python -m venv while running python 3.12. Any cronjobs you create should point to this venv python version (found at ./[venv name]/bin/python

You will then also need to create a kernel snapshot for jupyter using this python version. Have the virtual environment active and run python -m ipykernel install --user --name [your name here]. By default, is jupyter3.12, but you can customize it as long as you also change the kernel name parameter in one of the functions in src/pipeline.py.

### Requirements.txt * IMPORTANT *

Requirements.txt is a file that contains all the dependencies for the program. Right now, it contains
dependencies needed to run the dummy-test notebooks. Everywhere an external library is used in the notebooks,
you must add it to requirements.txt.

Make sure you add *all* libraries used in the notebooks into the requirements.txt file. If you don't,
the program WILL cause an error mid-pipeline.

When you've added, type `pip3 install -r requirements.txt` to install these dependencies into your environment.

## Setup

On the server (DigitalOcean, etc.) that you want to run the pipeline on,
type the command
```bash
git clone git@github.com:kevinmonisit/notebook-pipeline-runner.git
cd notebook-pipeline-runner
```

1. Make sure you have the requirements installed via `pip3 install -r requirements.txt`. (also make sure you have Python3)

2. Go to [SendGrid.com](https://sendgrid.com/) and create an account. At the beginning of account regisration, you're going to have to create a [verified sender](https://docs.sendgrid.com/ui/sending-email/sender-verification) and verify the email you wish to send an email from. This is the first thing you do before your account is created. Set the Sender Email to any email you wish to send alerts from. (Note: You cannot send emails to yourself with SendGrid.com)

3. When you create your account, you should see a dashboard.

<img width="1235" alt="image" src="https://user-images.githubusercontent.com/7038712/228095670-e3173df4-0f10-4989-a7b1-fad11e9bb3e0.png">

4. On the right, there is a "Settings" button. Click on that.

5. Click on `API KEYS`.

6. On the top right, click `Create API Key`.

7. Set the API Key Permissions to `Restricted Access`, and then give the API Key permission for "Mail Send".

<img width="854" alt="image" src="https://user-images.githubusercontent.com/7038712/228096711-08a03b5f-6ee9-47d3-b4be-e7ddccc17ffc.png">

8. Make sure to copy the API key

9. Go to the file `test.env` and set the `SENDGRID_API_KEY=` to `'<API KEY>'`. Make sure the single quotations are there if they aren't already.

10. Rename the file `test.env` to `.env`.

11. Fill out the `.env`, replacing `SENDGRID_FROM_EMAIL` and `SENDGRID_TO_EMAIL` with the emails you choose. `SENDGRID_FROM_EMAIL` should be the email you set up your SendGrid.com account with to send emaisl.

12. After setting the `.env` file, you can now run command `python3 main.py` from the directory of the project.

13. An email will be sent to `SENDGRID_TO_EMAIL` stating that pipeline initialization has started.

Note: SendGrid API allows for 100 free emails per day.

14. Create directories for ./out and ./logs

### To bypass confirmation

Bypass the confirmation prompt by typing

`python3 main.py --bypass-confirm`.

### Modifying the Pipeline

The process:
```bash
[ your personal computer ] -- [transferring requirements.txt and notebooks] --> [ server ]
```

1. Before you run the pipeline, from the environment (personal computer, etc.) that you usually run
the pipeline, type `python3 -m pip freeze > requirements.txt`. This will create a requirements.txt
which contains all the dependencies needed to run the pipeline normally.

2. Then, replace the `requirements.txt` file in the project directory with the one you just created.

3. Run `pip3 -m install -r requirements.txt` to install the dependencies into your environment (assuming this is the server).

4. Type `python3 main.py --bypass-confirm` to run the dummy pipeline to make sure everything works. Now, it's time to modify the pipeline to your liking
now that we've verified that the pipeline works.

5. To modify the pipeline, edit the `main.py` file. The `main.py` file contains the main function, which
contains an array called `notebooks`, containing the path to each notebook that will be run
and in what order they will be run. Modify this array to your liking.

```python
notebooks = ['./notebooks/notebook.ipynb',
             './notebooks/notebook2.ipynb',
             './notebooks/notebook4.ipynb',
             './notebooks/notebookERROR.ipynb',
             './notebooks/notebook4.ipynb'
             ]
```

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
