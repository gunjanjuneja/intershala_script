import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import time
from dotenv import load_dotenv
import os
import schedule
load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_NUMBER')
recipient_number = os.getenv('RECIPIENT_NUMBER')
recipient_number2 = os.getenv('RECIPIENT_NUMBER2')
recipient_number3 =[recipient_number, recipient_number2]
# recipient_number = 'whatsapp:+918168667070'
# recipient_numbers = ['whatsapp:+918168667070','whatsapp:+919354207979']

url = 'https://internshala.com/internships/python%2Fdjango-internship'
seen_internships = set()
def fetch_internships():
   
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve content: {response.status_code}")
        return []

    
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup.prettify())
    
    
    internship_cards = soup.find_all('div', class_='internship_meta')
    internships = []
 

    for card in internship_cards:
        title_tag = card.find('h3')
        location_tag = card.find(id='location_names')
        stipend_tag = card.find('span', class_='stipend')
        # button_container = card.find('div', class_='button_container_card')
        button_container = soup.find('div', class_='button_container_card')
        if button_container:
            apply_link_tag = button_container.find('a', class_='view_detail_button_outline')
            if apply_link_tag:
               apply_link = apply_link_tag['href']
               print(f"Apply Link: {apply_link}")
            else:
                print("Apply link not found")
        else:
            print("Button container not found")



        print(f"Title Tag: {title_tag}")
        print(f"Location Tag: {location_tag}")
        
        
        if title_tag and location_tag:
            title = title_tag.text.strip()
            location = location_tag.text.strip()
            stipend = stipend_tag.text.strip() if stipend_tag else 'Not specified'
            apply_link = 'https://internshala.com' + apply_link_tag ['href']if apply_link_tag else 'Apply link not available'
            internship = {'title': title, 'location': location, 'stipend': stipend, 'apply_link': apply_link}
            
            internships.append(internship)


    return internships

def send_whatsapp_message(internship_details, recipient_number3):
    client = Client(account_sid, auth_token)
    message_body = f"{internship_details['title']} - {internship_details['location']}\n"
    message_body += f"Stipend: {internship_details.get('stipend', 'Not specified')}\n"
    message_body += f"Apply here: {internship_details.get('apply_link', 'Not specified')}"

    for number in recipient_number3:
        try:
            print(f"Sending message to {number}")
            message = client.messages.create(
                body=message_body,
                from_=twilio_number,
                to=number
            )
            print(f'Message sent to {number}: {message.sid}')
        except Exception as e:
            print(f'Failed to send message to {number}: {e}')

def job():
    global seen_internships
    internships = fetch_internships()
    new_internships = [i for i in internships if i['title'] not in seen_internships]

    if new_internships:
        for internship in new_internships:
            send_whatsapp_message(internship, recipient_number3)
            seen_internships.add(internship['title'])
    else:
        message_body = "No new internships found in the latest check."
        for number in recipient_number3:
            try:
                print(f"Sending message to {number}")
                message = Client.messages.create(
                    body=message_body,
                    from_=twilio_number,
                    to=number
                )
                print(f'Message sent to {number}: {message.sid}')
            except Exception as e:
                print(f'Failed to send message to {number}: {e}')

def main():
    # Schedule the job every 2 minutes
    schedule.every(2).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()


import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Twilio configuration
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_NUMBER')
recipient_number = os.getenv('RECIPIENT_NUMBER')
recipient_number2 = os.getenv('RECIPIENT_NUMBER2')
recipient_numbers = [recipient_number, recipient_number2]

# URL to fetch internships
url = 'https://internshala.com/internships/python%2Fdjango-internship'

def fetch_internships():
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve content: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    internship_cards = soup.find_all('div', class_='internship_meta')
    internships = []

    for card in internship_cards:
        title_tag = card.find('h3')
        location_tag = card.find(id='location_names')
        stipend_tag = card.find('span', class_='stipend')
        button_container = card.find('div', class_='button_container_card')

        if button_container:
            apply_link_tag = button_container.find('a', class_='view_detail_button_outline')
            apply_link = 'https://internshala.com' + apply_link_tag['href'] if apply_link_tag else 'Apply link not available'

            if title_tag and location_tag:
                title = title_tag.text.strip()
                location = location_tag.text.strip()
                stipend = stipend_tag.text.strip() if stipend_tag else 'Not specified'
                internship = {'title': title, 'location': location, 'stipend': stipend, 'apply_link': apply_link}
                internships.append(internship)

    return internships

def send_whatsapp_message(internship_details, recipient_numbers):
    client = Client(account_sid, auth_token)
    message_body = f"{internship_details['title']} - {internship_details['location']}\n"
    message_body += f"Stipend: {internship_details.get('stipend', 'Not specified')}\n"
    message_body += f"Apply here: {internship_details.get('apply_link', 'Not specified')}"

    for number in recipient_numbers:
        try:
            print(f"Sending message to {number}")
            message = client.messages.create(
                body=message_body,
                from_=twilio_number,
                to=number
            )
            print(f'Message sent to {number}: {message.sid}')
        except Exception as e:
            print(f'Failed to send message to {number}: {e}')

def main():
    internships = fetch_internships()
    if internships:
        for internship in internships:
            send_whatsapp_message(internship, recipient_numbers)
    else:
        print("No internships found.")

if __name__ == '__main__':
    main()
