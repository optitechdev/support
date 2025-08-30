import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

def send_support_email(customer_name, customer_email, ticket_description, ticket_id=None):
    api_key = os.environ.get("SENDGRID_API_KEY")
    if not api_key:
        print("❌ API-nyckel saknas.")
        return

    print("🔐 API-nyckel laddad.")

    sg = SendGridAPIClient(api_key=api_key)

    ärendenummer_text = f"\n\nÄrendenummer: {ticket_id}" if ticket_id else ""

    try:
        # Bekräftelse till användare
        message_to_user = Mail(
            from_email="support@optitech-sverige.se",
            to_emails=customer_email,
            subject=f"Vi har tagit emot ditt supportärende – {ticket_id or 'Utan nummer'}",
            plain_text_content=f"""Hej {customer_name},

Tack för att du kontaktade oss. Vi har tagit emot följande ärende:

{ticket_description}{ärendenummer_text}

Vårt supportteam återkommer så snart som möjligt.

Vänliga hälsningar,  
Supportteamet
"""
        )
        user_response = sg.send(message_to_user)
        print(f"📨 Till användare – Status: {user_response.status_code}")

        # Intern notis
        message_to_admin = Mail(
            from_email="support@optitech-sverige.se",
            to_emails="support@optitech-sverige.se",
            subject=f"Nytt supportärende från {customer_name} – {ticket_id or 'Utan nummer'}",
            plain_text_content=f"""Ett nytt ärende har inkommit:

Namn: {customer_name}
E-post: {customer_email}
Ärende:
{ticket_description}{ärendenummer_text}
"""
        )
        admin_response = sg.send(message_to_admin)
        print(f"📨 Till admin – Status: {admin_response.status_code}")

    except Exception as e:
        print("❌ Något gick fel med e-postutskicket:", e)
