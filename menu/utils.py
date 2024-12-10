from twilio.rest import Client

def send_whatsapp_message():
    """
    Sends a WhatsApp message using Twilio API.
    Returns the message SID if successful or raises an exception on failure.
    """
    # Twilio API credentials (use environment variables for security)
    account_sid = ''
    auth_token = ''
    from_whatsapp = 'whatsapp:+14155238886'  # Twilio WhatsApp sandbox number
    to_whatsapp = 'whatsapp:+5214499185218'  # Recipient's WhatsApp number
    content_sid = 'HXb5b62575e6e4ff6129ad7c8efe1f983e'  # Pre-approved template SID
    content_variables = {"1": "12/1", "2": "3pm"}  # Variables for the template in dictionary format

    try:
        # Initialize Twilio client
        client = Client(account_sid, auth_token)

        # Create and send the message
        message = client.messages.create(
            from_=from_whatsapp,
            content_sid=content_sid,
            content_variables=content_variables,
            to=to_whatsapp
        )

        # Return message SID for confirmation
        return message.sid

    except Exception as e:
        # Log and raise the exception for higher-level handling
        raise Exception(f"Error sending WhatsApp message: {e}")
