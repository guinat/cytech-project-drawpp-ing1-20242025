#!/bin/bash

# get root project directory path
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

# add project root to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$PROJECT_ROOT

echo "PYTHONPATH updated : $PYTHONPATH"
echo "Yoou can now launch compiler from compiler/ folder"
