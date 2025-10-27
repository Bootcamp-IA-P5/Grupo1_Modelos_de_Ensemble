"""
Script simple para probar los endpoints de drift
"""

import requests
import json

BASE_URL = "http://localhost:8000"

# 1. Establecer baseline con datos de ejemplo (más muestras)
print("1. Estableciendo baseline...")
baseline_data = {
    "baseline_data": [
        [2500, 180, 15, 200, 50, 1000, 220, 230, 140, 500] + [0]*44,
        [2600, 190, 16, 210, 55, 1100, 225, 235, 145, 510] + [0]*44,
        [2400, 170, 14, 190, 45, 900, 215, 225, 135, 490] + [0]*44
    ]
}

response = requests.post(f"{BASE_URL}/drift/baseline", json=baseline_data)
print(f"   Respuesta: {response.json()}")

# 2. Verificar status
print("\n2. Verificando status...")
response = requests.get(f"{BASE_URL}/drift/status")
print(f"   Status: {json.dumps(response.json(), indent=2)}")

# 3. Verificar drift con datos similares
print("\n3. Verificando drift con datos similares...")
new_data = {
    "features": [
        [2550, 185, 15, 205, 52, 1050, 222, 232, 142, 505] + [0]*44
    ]
}
try:
    response = requests.post(f"{BASE_URL}/drift/check", json=new_data)
    print(f"   Drift: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"   Error: {e}")
    print(f"   Status: {response.status_code}")
    print(f"   Text: {response.text}")

# 4. Verificar drift con datos diferentes
print("\n4. Verificando drift con datos diferentes...")
different_data = {
    "features": [[5000, 300, 30, 400, 100, 2000, 240, 250, 160, 1000] + [0]*44]
}
response = requests.post(f"{BASE_URL}/drift/check", json=different_data)
print(f"   Drift: {json.dumps(response.json(), indent=2)}")

# 5. Ver historial
print("\n5. Verificando historial...")
response = requests.get(f"{BASE_URL}/drift/history")
print(f"   Historia: {json.dumps(response.json(), indent=2)}")

print("\n✅ Pruebas completadas!")
