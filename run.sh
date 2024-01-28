#!/bin/sh



source ./.venv/bin/activate
env PATH="/web_trade/.venv/bin:$PATH"
python -m web_trade.main
echo 'startup'

