import requests
#
#
TOKEN = "6533789385:AAEnNaKBiS9uLK1NSrzgLVFOJLa2XvZhWZg"
CHAT_ID = "414214892"
#
#
def notify(patient, text="Angry emotion is detected in your center."):
    # Send message
    message = f"⚠️ ALERT\n\n{text}\nPatient: {patient}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)