import os
import resend

def send_email(subject, message_body):
    # Check for required API key
    if os.environ.get('RESEND_API_KEY') is None:
        raise Exception("RESEND_API_KEY is not set")
    
    # Set the API key for resend
    resend.api_key = os.environ.get('RESEND_API_KEY')
    
    # Get email addresses from environment variables
    from_email = os.environ.get('RESEND_FROM_EMAIL')
    to_emails_str = os.environ.get('RESEND_TO_EMAILS')  # Changed from SENDGRID_TO_EMAIL
    
    if not from_email or not to_emails_str:
        raise Exception("RESEND_FROM_EMAIL or RESEND_TO_EMAILS is not set")
    
    # Parse comma-separated email addresses and strip whitespace
    to_emails = [email.strip() for email in to_emails_str.split(',') if email.strip()]
    
    if not to_emails:
        raise Exception("No valid email addresses found in RESEND_TO_EMAILS")
    
    # Debug prints
    #print(f"To emails: {to_emails}")
    #print(f"From email: {from_email}")
    #print(f"Subject: {subject}")
    
    # Prepare email parameters for Resend API
    params = {
        "from": from_email,
        "to": to_emails,
        "subject": subject,
        "html": message_body,
    }
    
    try:
        # Send email using Resend API
        response = resend.Emails.send(params)
        # print(f"Email sent successfully: {response}")
        return response
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise e
