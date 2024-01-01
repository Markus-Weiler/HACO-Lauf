import requests

# Setzen Sie die URL des API-Endpunkts
url = "https://api.raceresult.com"

# Fügen Sie benötigte Header hinzu, z.B. API-Schlüssel oder Authentifizierungsinformationen
headers = {
    "Authorization": "Bearer eyJhbGciOiJlZDI1NTE5IiwidHlwIjoiSldUIn0.eyJhdWQiOiJyZXN0cHJveHkiLCJleHAiOjE3MDM0MDk2NjYsInN1YiI6Ijg2OTU4In0.YDLkGeyW_uMVPRuoB8F-WYI4PPnH0aY3U9ZEmcdiCKcI91XTuH6M4FbPciRW8vtDagcEV8zaRDmDVo4hGW9SCg"
    # "Authorization": "86958.d2d8cb487826ad78f88cda899e423c90071bc1c0ac5e341fb26eed2f973f57d97488b430cfb40c67763cf5f306eaa5b9"
}

# Fügen Sie erforderliche oder optionale Parameter hinzu
# params = "111952"
params = {
    "race_id": "272953",  # Beispiel-Renn-ID
    # Weitere Parameter nach Bedarf
}

# Senden des GET-Requests
response = requests.get(url, headers=headers, params=params)

# Überprüfen und Verarbeiten der Antwort
if response.status_code == 200:
    data = response.json()
    print("Erfolgreich Daten erhalten:")
    print(data)
else:
    print(f"Fehler beim Abrufen der Daten: Statuscode {response.status_code}")
