# Scripts

## Description

Basic scripts for automating tasks. OSX flavored for now.

## Installation

To run python scripts:

- Setup Python environment

    ```bash
    cd python_src
    ./py-env-setup.sh
    ```

- Setup scripts.env

    ```bash
    export PYTHONPATH="path/to/root-module"
    export DOWNLOADS=""
    export SCREENSHOTS=""
    ```

## Usage

- Python scripts can be executed manually from root shell scripts, e.g.

    ```bash
    ./clean-downloads.sh
    ```

- Or set to run with cron. Sample tab to clean Downloads folder every day at 21:00:00 UTC and log cron output

    ```bash
    0 21 * * * cd /path/to/scripts/ && ./clean-downloads.sh > /path/to/scripts/cron-logs/clean-downloads.log 2>&1
    ```

    To set tab

    ```bash
    crontab -e
    ```
