import requests
import os
from agents import function_tool

@function_tool
def send_whatsapp_message(number: str, message: str) -> str:
    """
    Send WhatsApp message via UltraMSG API
    """
    instance_id = os.getenv("INSTANCE_ID")
    token = os.getenv("API_TOKEN")
    
    if not instance_id or not token:
        return "❌ WhatsApp API credentials missing. Please check INSTANCE_ID and API_TOKEN."
    
    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
    
    payload = {
        "token": token,
        "to": number,
        "body": message
    }
    
    print(f"📤 Sending WhatsApp message to {number} via UltraMSG...")
    print(f"Payload: {payload}")
    print(f"URL: {url}")
    
    try:
        response = requests.post(url, data=payload)
        
        print(f"📨 UltraMSG Response [{response.status_code}]: {response.text}")
        
        if response.status_code == 200:
            return f"✅ Message successfully sent to {number}"
        else:
            return f"❌ Failed to send message. Error: {response.text}"
    
    except Exception as e:
        return f"❌ Error sending WhatsApp message: {str(e)}"