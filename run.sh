#!/bin/sh



source ./.venv/bin/activate
env PATH="/web_trade/.venv/bin:$PATH"
python -m webcur.main
echo 'startup'

