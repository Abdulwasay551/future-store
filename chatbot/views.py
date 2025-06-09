from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import uuid
from .ollama import Ollama
from .models import ChatSession, UserPreference
from store.models import Product

# Initialize Ollama chatbot
chatbot = Ollama(model="llama3.2:3b")

def get_or_create_session(request):
    """Get existing chat session or create a new one."""
    if request.user.is_authenticated:
        session, created = ChatSession.objects.get_or_create(
            user=request.user,
            defaults={'session_id': str(uuid.uuid4())}
        )
    else:
        session_id = request.session.get('chat_session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session['chat_session_id'] = session_id
        
        session, created = ChatSession.objects.get_or_create(
            session_id=session_id
        )
    return session

def get_chat_widget(request):
    """Render the chat widget template."""
    return render(request, 'chatbot/chatbot.html')

@csrf_exempt
@require_http_methods(["POST"])
def chat_message(request):
    """Handle incoming chat messages and return bot responses."""
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        
        if not message:
            return JsonResponse({
                'error': 'No message provided'
            }, status=400)
        
        # Get or create chat session
        session = get_or_create_session(request)
        
        # Generate bot response
        response = chatbot.generate_response(message)
        
        # Check if we need to extract preferences from the conversation
        if any(keyword in message.lower() for keyword in ['price', 'budget', 'spend', 'cost']):
            try:
                # Extract budget from message (simplified example)
                import re
                numbers = re.findall(r'\d+', message)
                if len(numbers) >= 2:
                    budget_min = min(int(numbers[0]), int(numbers[1]))
                    budget_max = max(int(numbers[0]), int(numbers[1]))
                    
                    # Update or create user preferences
                    UserPreference.objects.update_or_create(
                        chat_session=session,
                        defaults={
                            'budget_min': budget_min,
                            'budget_max': budget_max,
                            'camera_importance': 'medium',  # Default values
                            'performance_needs': 'medium',
                            'gaming_priority': 'low'
                        }
                    )
            except Exception as e:
                print(f"Error extracting preferences: {str(e)}")
        
        # If this is a product recommendation request, fetch relevant products
        if any(keyword in message.lower() for keyword in ['recommend', 'suggest', 'phone', 'find']):
            try:
                preference = UserPreference.objects.filter(chat_session=session).first()
                products = Product.objects.filter(is_available=True)
                
                if preference:
                    products = products.filter(
                        price__gte=preference.budget_min,
                        price__lte=preference.budget_max
                    )
                
                products = products[:5]  # Limit to 5 products
                
                product_info = [
                    {                        'name': p.name,
                        'price': str(p.price),
                        'description': p.description,
                        'url': f'/store/product/{p.slug}',
                        'image': p.image.url if p.image else None
                    }
                    for p in products
                ]
                
                return JsonResponse({
                    'response': response,
                    'products': product_info
                })
            
            except Exception as e:
                print(f"Error fetching products: {str(e)}")
        
        return JsonResponse({
            'response': response
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)
