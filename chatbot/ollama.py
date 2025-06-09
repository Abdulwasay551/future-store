import json
from ollama import chat, ChatResponse
from typing import Dict, List

class Ollama:
    def __init__(self, model: str = "llama3.2:3b"):
        self.model = model
        self.context = []
        
    def _generate_system_prompt(self) -> str:
        return """You are a friendly and knowledgeable phone advisor helping customers find the perfect mobile phone. 
        When asking questions, be concise and give specific options when possible. 
        Keep responses brief and friendly. Focus on key phone features like camera, performance, battery, and price."""
    
    def _format_messages(self, user_message: str) -> List[Dict[str, str]]:
        """Format the conversation history into messages format for ollama."""
        messages = [
            {
                'role': 'system',
                'content': self._generate_system_prompt()
            }
        ]
        
        # Add conversation history
        for msg in self.context:
            role, content = msg.split(": ", 1)
            messages.append({
                'role': 'assistant' if role == 'Assistant' else 'user',
                'content': content
            })
            
        # Add current user message
        messages.append({
            'role': 'user',
            'content': user_message
        })
        
        return messages
        
    def generate_response(self, message: str) -> str:
        try:
            # Format messages with context
            messages = self._format_messages(message)
            
            # Get response from Ollama
            response: ChatResponse = chat(
                model=self.model,
                messages=messages
            )
            
            # Extract response content
            bot_response = response.message.content
            
            # Update context
            self.context.append(f"User: {message}")
            self.context.append(f"Assistant: {bot_response}")
            
            # Keep context manageable (last 10 messages)
            if len(self.context) > 10:
                self.context = self.context[-10:]
                
            return bot_response
            
        except Exception as e:
            print(f"Error calling Ollama API: {str(e)}")
            return "I apologize, but I'm having trouble processing your request. Please try again."

    def get_phone_recommendations(self, user_preferences: Dict) -> List[Dict]:
        """
        Generate phone recommendations based on user preferences.
        """
        prompt = f"""Given these user preferences:
        - Camera importance: {user_preferences.get('camera', 'Not specified')}
        - Performance needs: {user_preferences.get('performance', 'Not specified')}
        - Gaming priority: {user_preferences.get('gaming', 'Not specified')}
        - Budget range: {user_preferences.get('budget', 'Not specified')}
        
        Please recommend suitable phones from our catalog."""
        
        response = self.generate_response(prompt)
        return self._parse_recommendations(response)
    
    def _parse_recommendations(self, response: str) -> List[Dict]:
        """
        Parse the bot's response into structured recommendations.
        """
        # For now, return a sample structure
        # This could be enhanced to actually parse the response
        return [
            {
                "name": "Sample Phone 1",
                "reason": "Good match for your camera preferences",
                "score": 0.95
            }
        ]
