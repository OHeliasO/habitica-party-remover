# Habitica Party Remover

This project automates the removal of inactive members from a Habitica party using the Habitica API.

## Features
- Automatically checks all party members for inactivity
- Removes members who have not logged in for a configurable number of days (default: 14)
- Logs all removals to a file (`removed_members.log`)
- Skips the party leader and members with no login record

## Requirements
- Python 3.11+
- Habitica account and API credentials

## Setup
1. Clone this repository:
   ```bash
   git clone <repo-url>
   cd habitica-party-remover
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # or, if using conda:
   conda env create -f environment.yml
   conda activate HABITICA
   ```
3. Copy the sample environment file and fill in your Habitica credentials:
   ```bash
   cp .env-sample .env
   # Edit .env with your API User ID, API Token, Group ID, and Client Name
   ```

## Configuration
- Edit `.env` to set your Habitica API credentials and group information.
- You can change the inactivity limit by modifying the `INACTIVITY_LIMIT` variable in `src/main.py`.

## Usage
Run the main script:
```bash
python src/main.py
```

## Notes
- Removals are logged in `removed_members.log` with a timestamp.
- The script skips the party leader and members with no login record.
- Make sure your API credentials are kept secure and never shared publicly.
- For more information, see the [Habitica API documentation](https://habitica.com/apidoc/).

