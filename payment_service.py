import requests
import json
import random
import time
from datetime import datetime

# Simulación de API externa de pagos (no existe realmente)
PAYMENT_API_URL = "https://api.webpay-simulation.cl"

class PaymentService:
    @staticmethod
    def process_payment(orden_id, monto, metodo_pago):
        """
        Simula el consumo de un servicio web externo para procesar pagos.
        En un entorno real, esto haría una llamada a la API de Webpay.
        """
        print(f"Procesando pago de ${monto} para la orden #{orden_id} con {metodo_pago}")
        
        # Simulamos la estructura de datos que enviaríamos a una API externa
        payment_data = {
            "orden_id": str(orden_id),
            "monto": monto,
            "metodo_pago": metodo_pago,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "moneda": "CLP"
        }
        
        # Simulamos la llamada a la API (en realidad no se ejecuta)
        # En un caso real sería algo como:
        # response = requests.post(f"{PAYMENT_API_URL}/transactions", json=payment_data)
        
        # Simulamos el tiempo de respuesta de una API externa
        time.sleep(1)
        
        # Generamos una respuesta simulada
        transaction_id = ''.join(random.choices('0123456789ABCDEF', k=10))
        
        response_data = {
            "status": "success",
            "transaction_id": transaction_id,
            "order_id": orden_id,
            "amount": monto,
            "currency": "CLP",
            "payment_method": metodo_pago,
            "timestamp": datetime.now().isoformat(),
            "authorization_code": random.randint(100000, 999999)
        }
        
        print(f"Respuesta del servicio de pago: {json.dumps(response_data, indent=2)}")
        return response_data
    
    @staticmethod
    def verify_payment(transaction_id):
        """
        Simula la verificación de un pago con la API externa.
        """
        print(f"Verificando estado del pago con ID de transacción: {transaction_id}")
        
        # Simulamos tiempo de respuesta
        time.sleep(0.5)
        
        # Estado aleatorio con mayor probabilidad de éxito
        statuses = ["approved", "approved", "approved", "declined", "pending"]
        status = random.choice(statuses)
        
        response_data = {
            "status": status,
            "transaction_id": transaction_id,
            "verification_timestamp": datetime.now().isoformat()
        }
        
        print(f"Estado del pago: {status}")
        return response_data

# Ejemplo de uso:
if __name__ == "__main__":
    # Probar el servicio
    orden_id = random.randint(10000, 99999)
    monto = random.randint(10000, 100000)
    
    payment_result = PaymentService.process_payment(orden_id, monto, "webpay")
    
    if payment_result["status"] == "success":
        verification = PaymentService.verify_payment(payment_result["transaction_id"])
        print(f"Verificación final: {verification['status']}")