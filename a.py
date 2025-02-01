import requests

# Configuración
base_url = "http://localhost:11434/v1/chat/completions"
api_key = "ollama"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
payload = {
    "model": "deepseek-r1:1.5b",
    "messages": [{"role": "user", "content": "Make a \"Hello World\" with go"}],
    "temperature": 0.7
}

# Realizar la solicitud
response = requests.post(base_url, headers=headers, json=payload)

# Manejar la respuesta
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error {response.status_code}: {response.text}")