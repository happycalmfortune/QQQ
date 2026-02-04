name: Update Stock Prices

on:
  schedule:
    - cron: '*/10 * * * *'  # Changed: Runs every 10 minutes
  workflow_dispatch:        # Allows manual run button

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: pip install yfinance pytz

    - name: Run script
      run: python update_prices.py

    - name: Commit and Push
      run: |
        git config --global user.name 'GitHub Action'
        git config --global user.email 'action@github.com'
        git add data.json
        # Only commit if data changed
        git diff --quiet && git diff --staged --quiet || (git commit -m "Update prices (10m)" && git push)
