# Internshala Internship Fetcher and Notifier

This script fetches the latest Python/Django internships from Internshala and sends notifications via WhatsApp using Twilio.

## Features

- Fetches the latest internships from Internshala.
- Sends notifications to multiple recipients via WhatsApp using Twilio.
- Filters out already notified internships to avoid duplicate notifications.

## Requirements

- Python 3.x
- `requests` library
- `BeautifulSoup` (from `bs4` library)
- `twilio` library
- `python-dotenv` library
- `schedule` library (if you wish to schedule the script execution)

## Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/gunjanjuneja/intershala_script.git
   cd intershala_script
