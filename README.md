# BuildAPCWatcher

### Setup

BuildAPCWatcher can be ran via Docker run or with python and pip.

#### Via Docker

See `run_bash.sh`, executable if using \*nix, if on Windows run the individual commands in the file.

This will build the container, and the subsequent command runs the container.

#### Via python

Install python3 and pip. Afterwards, install dependencies via `python3 -m pip install -r requirements.txt`.

Run via `python3 buildapcwatch.py`

### Configuration

You'll need the following:
* A reddit account with an 'application' set up, see the 'create an app' section under reddit @ preferences -> apps
* A gmail account to send notifications (recommend using a throwaway one)

Copy the `example_config.py` file to `config.py`, edit the fields w/ your credentials.

Other configuration involves setting up the desired type of alerts - currently supported are email and sms (for at&t and verizon only, but easily extended)

