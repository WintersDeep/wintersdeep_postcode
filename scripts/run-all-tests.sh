#!/bin/bash

# work out where things sit..
ECHO="/bin/echo"
SCRIPT_PATH="${BASH_SOURCE[0]}"
SCRIPT_DIRECTORY="$(dirname "${SCRIPT_PATH}")"
PROJECT_DIRECTORY="$( cd "${SCRIPT_DIRECTORY}" && cd .. && pwd )"
PYTHON="${PROJECT_DIRECTORY}/venv/bin/python"

# make sure we found python - making sure we find the virtual environment is important,
# but because we need a venv for this project, but it confirms the version and location
# of the python install, and that we dont just poke a random binary in PATH.
if [ ! -f "${PYTHON}" ]; then
  "${ECHO}" "[!] This script expects a development environment with an established /venv."
  "${ECHO}" "[!] Cannot run tests, unable to find python in virtual environment."
  exit
fi

# run the project tests.
"${ECHO}" "[-] Running all wintersdeep_postcode test classes..."
"${PYTHON}" -m unittest discover -vs "${PROJECT_DIRECTORY}"