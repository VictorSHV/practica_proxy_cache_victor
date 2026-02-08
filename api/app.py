from flask import Flask, jsonify
import redis
import time
import os

app = Flask(__name__)

# Conexión a Redis (Caché Nivel 2)
cache = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379)

@app.route('/')
def get_data():
    # 1. Intentar obtener de Redis
    cached_val = cache.get('data_key')
    if cached_val:
        return jsonify({"source": "Redis (Level 2)", "data": cached_val.decode('utf-8')})

    # 2. Simular proceso lento (2-3 segundos) si no está en Redis
    time.sleep(2.5)
    result = "Información procesada a las " + time.strftime("%H:%M:%S")

    # 3. Guardar en Redis para la próxima vez
    cache.setex('data_key', 300, result) # Expira en 5 min en Redis

    return jsonify({"source": "API Engine", "data": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
