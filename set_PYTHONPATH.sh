#!/bin/bash

# Add project to PYTHONPATH
# Script must be sourced to alter path in current shell

function EXT_COLOUR () { echo -ne "\033[1;38;5;$1m"; }

# Check that script was sourced
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]
then
	DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
	export PYTHONPATH=$DIR:$PYTHONPATH
else
	echo -e "`EXT_COLOUR 160`\nScript was run in a subshell (./set_PYTHONPATH)" 
	echo -e "Must source script to alter env (. set_PYTHONPATH) `EXT_COLOUR 0`" 
fi
