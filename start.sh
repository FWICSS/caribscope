#!/bin/bash
set -e

if [ -f "/app/data/hurricanes_Past_In_Caribbean.csv" ]; then
    python -m src.data.precompute
fi

exec streamlit run app.py --server.port=8501 --server.address=0.0.0.0
