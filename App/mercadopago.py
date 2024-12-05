import mercadopago
from dotenv import load_dotenv
import os 
load_dotenv()
# Agrega credenciales
PROD_ACCESS_TOKEN = os.getenv("PROD_ACCESS_TOKEN")
sdk = mercadopago.SDK(PROD_ACCESS_TOKEN)

# Crea un ítem en la preferencia
def gePreferenceId(items):
    # [
    #         {
    #             "title": "Mi producto",
    #             "quantity": 1,
    #             "unit_price": 75.76,
    #         }
    #     ]
    preference_data = {
        "items": items
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    return preference
