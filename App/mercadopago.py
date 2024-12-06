from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import mercadopago
import json
from dotenv import load_dotenv
from os import getenv
load_dotenv()
@csrf_exempt
def create_preference(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        mp = mercadopago.SDK(getenv("ACCESS_TOKEN"))
        
        preference_data = {
            "items": [{
                "title": item["nom_producto"],
                "quantity": item['quantity'],
                "unit_price": item['precio_producto']
            } for item in data['products']],
            "back_urls": {
                "success": "https://www.stanley.mayola.net.ar/success.html",
                "failure": "https://www.stanley.mayola.net.ar/failure.html",
                "pending": "https://www.stanley.mayola.net.ar/pending.html"
            },
            "auto_return": "approved"
        }
        
        preference_response = mp.preference().create(preference_data)
        
        return JsonResponse({"init_point": preference_response["response"]["init_point"]})