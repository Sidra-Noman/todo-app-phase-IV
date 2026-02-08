import cohere
from typing import Dict, Any, List, Optional
from ..core.cohere_config import cohere_config


class CohereClient:
    """
    Client for interacting with the Cohere API.
    Handles authentication and provides methods for various AI operations.
    """

    def __init__(self):
        self.client = cohere.Client(cohere_config.cohere_api_key)
        self.model = cohere_config.cohere_model
        self.timeout = cohere_config.cohere_timeout

    def chat(self, message: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Send a chat message to Cohere and return the response.
        """
        try:
            # Prepare the chat history if available
            chat_history = []
            if conversation_history:
                for msg in conversation_history:
                    chat_history.append({
                        "role": msg.get("role", "user"),
                        "message": msg.get("content", "")
                    })

            # Call the Cohere chat endpoint
            response = self.client.chat(
                message=message,
                model=self.model,
                chat_history=chat_history if chat_history else None,
                temperature=0.7
            )

            return response.text
        except Exception as e:
            raise Exception(f"Cohere API error: {str(e)}")

    def classify_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Classify the user's intent from their input.
        """
        try:
            # Define possible intents for our todo app
            examples = [
                cohere.Example(text="Add a todo to buy groceries", label="ADD"),
                cohere.Example(text="Create a task to call mom", label="ADD"),
                cohere.Example(text="Lunch at 2:00", label="ADD"),
                cohere.Example(text="Meeting with John tomorrow", label="ADD"),
                cohere.Example(text="Call dentist afternoon", label="ADD"),
                cohere.Example(text="Buy milk after work", label="ADD"),
                cohere.Example(text="Workout at 6am", label="ADD"),
                cohere.Example(text="Show me my todos", label="LIST"),
                cohere.Example(text="What do I need to do?", label="LIST"),
                cohere.Example(text="Update my meeting todo to tomorrow", label="UPDATE"),
                cohere.Example(text="Change the deadline on my work task", label="UPDATE"),
                cohere.Example(text="Delete the grocery shopping todo", label="DELETE"),
                cohere.Example(text="Remove the old task", label="DELETE"),
                cohere.Example(text="Mark the first todo as complete", label="COMPLETE"),
                cohere.Example(text="Complete my workout task", label="COMPLETE"),
            ]

            response = self.client.classify(
                model=self.model,
                inputs=[user_input],
                examples=examples
            )

            # Get the predicted intent
            predicted_intent = response.classifications[0].prediction
            confidence = response.classifications[0].confidence

            return {
                "intent": predicted_intent.lower(),
                "confidence": confidence,
                "original_text": user_input
            }
        except Exception as e:
            raise Exception(f"Cohere classification error: {str(e)}")