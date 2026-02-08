import re
from typing import Dict, Any, Optional, Tuple
from enum import Enum
from ..schemas.chat_schemas import ChatAction
from .cohere_client import CohereClient
from .error_handler import ErrorHandler


class IntentParser:
    """
    Parser for extracting intent and parameters from natural language input.
    Uses both rule-based parsing and AI classification.
    """

    def __init__(self):
        self.cohere_client = CohereClient()
        self.error_handler = ErrorHandler()

    def parse_intent(self, user_input: str, conversation_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Parse the user's input to determine intent and extract parameters.
        """
        # First try AI classification
        try:
            classification_result = self.cohere_client.classify_intent(user_input)
            intent = classification_result["intent"].upper()

            # Extract parameters based on intent and conversation context
            parameters = self._extract_parameters(user_input, intent, conversation_context)

            return {
                "action": self._map_intent_to_action(intent),
                "parameters": parameters,
                "confidence": classification_result.get("confidence", 0.0),
                "original_text": user_input
            }
        except Exception:
            # Fallback to rule-based parsing if AI fails
            return self._rule_based_parse(user_input, conversation_context)

    def extract_context_reference(self, user_input: str, conversation_context: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Extract references to previous conversation items (e.g., 'it', 'that', 'first one', etc.).
        """
        if not conversation_context:
            return None

        user_lower = user_input.lower().strip()

        # Look for references to previous items
        if 'it' in user_lower or 'that' in user_lower:
            # Find the most recent relevant item
            if conversation_context.get('recent_items'):
                # Return the most recent item
                return conversation_context['recent_items'][-1] if conversation_context['recent_items'] else None

        # Look for ordinal references like 'first', 'second', 'last', etc.
        ordinals = ['first', 'second', 'third', 'last']
        for ordinal in ordinals:
            if ordinal in user_lower:
                # In a full implementation, this would map to specific items
                # For now, return the ordinal as a reference
                return ordinal

        return None

    def _rule_based_parse(self, user_input: str, conversation_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Fallback rule-based parsing when AI classification fails.
        """
        user_lower = user_input.lower().strip()

        # Check for PROFILE intent (name, email, etc.)
        profile_patterns = [
            r"(?:add|set|update|change|my)\s+(?:my\s+)?name\s+(?:is\s+)?(?:to\s+)?(.+)",
            r"(?:my\s+name\s+is\s+)(.+)",
            r"(?:i'm|im)\s+(.+)",
            r"(?:call\s+me\s+)(.+)",
        ]

        for pattern in profile_patterns:
            match = re.search(pattern, user_lower)
            if match:
                name = match.group(1).strip()
                if name:
                    return {
                        "action": ChatAction.PROFILE,
                        "parameters": {"name": name},
                        "confidence": 0.8,
                        "original_text": user_input
                    }

        # Check for ADD intent
        add_patterns = [
            r"(?:add|create|make|new)\s+(?:a\s+)?(?:todo|task|item|thing)\s+(?:to\s+)?(.+)",
            r"(?:add|create|make|new)\s+(?:a\s+)?(.+)",
            r"(.+)\s+(?:please|now|today)"
        ]

        for pattern in add_patterns:
            match = re.search(pattern, user_lower)
            if match:
                title = match.group(1).strip()
                if title:
                    return {
                        "action": ChatAction.ADD,
                        "parameters": {"title": title},
                        "confidence": 0.7,
                        "original_text": user_input
                    }

        # Check for LIST intent
        list_patterns = [
            r"(?:show|list|display|see|view)\s+(?:my\s+)?(?:todos|tasks|items|things)",
            r"(?:what|whats)\s+(?:do\s+i\s+have|is\s+on\s+my\s+list|are\s+my\s+todos)",
            r"my\s+list"
        ]

        for pattern in list_patterns:
            if re.search(pattern, user_lower):
                return {
                    "action": ChatAction.LIST,
                    "parameters": {},
                    "confidence": 0.7,
                    "original_text": user_input
                }

        # Check for COMPLETE intent
        complete_patterns = [
            r"(?:complete|finish|done|mark.*as.*done)\s+(?:the\s+)?(.+?)\s+(?:todo|task|item)",
            r"(?:complete|finish|done|mark.*as.*done)\s+(?:the\s+)?(.+)",
            r"(?:complete|finish|done|mark.*as.*done)\s+(?:it|that)"
        ]

        for pattern in complete_patterns:
            match = re.search(pattern, user_lower)
            if match:
                todo_ref = match.group(1).strip()
                return {
                    "action": ChatAction.COMPLETE,
                    "parameters": {"reference": todo_ref if todo_ref != "it" and todo_ref != "that" else None},
                    "confidence": 0.7,
                    "original_text": user_input
                }

        # Check for DELETE intent
        delete_patterns = [
            r"(?:delete|remove|cancel|drop)\s+(?:the\s+)?(.+?)\s+(?:todo|task|item)",
            r"(?:delete|remove|cancel|drop)\s+(?:it|that)",
        ]

        for pattern in delete_patterns:
            match = re.search(pattern, user_lower)
            if match:
                todo_ref = match.group(1).strip()
                return {
                    "action": ChatAction.DELETE,
                    "parameters": {"reference": todo_ref if todo_ref != "it" and todo_ref != "that" else None},
                    "confidence": 0.7,
                    "original_text": user_input
                }

        # Check for UPDATE intent
        update_patterns = [
            r"(?:update|change|modify|edit)\s+(?:the\s+)?(.+?)\s+(?:todo|task|item)",
            r"(?:update|change|modify|edit)\s+(?:it|that)",
        ]

        for pattern in update_patterns:
            match = re.search(pattern, user_lower)
            if match:
                todo_ref = match.group(1).strip()
                return {
                    "action": ChatAction.UPDATE,
                    "parameters": {"reference": todo_ref if todo_ref != "it" and todo_ref != "that" else None},
                    "confidence": 0.7,
                    "original_text": user_input
                }

        # Check for natural language that looks like a todo/task without explicit action words
        # This handles cases like "lunch at 2:00", "meeting with John", "buy milk", etc.
        # Patterns: contains time expressions, activity words, or common todo formats
        # Order matters - check more specific patterns first

        # First check for time expressions
        if re.search(r'\b\d{1,2}:\d{2}\b|\b\d{1,2}(?:am|pm)\b|\b\d{1,2}\s*(?:am|pm)\b', user_lower):
            return {
                "action": ChatAction.ADD,
                "parameters": {"title": user_input.strip()},
                "confidence": 0.65,  # Higher confidence for time-based tasks
                "original_text": user_input
            }

        # Check for common activity words (but not in question contexts)
        activity_words = r'\b(meeting|appointment|lunch|dinner|breakfast|call|talk|chat|hangout|event|work|study|exercise|gym|doctor|dentist|shopping|grocery|errand|clean|wash|laundry|cook|prepare|buy|purchase|order|send|mail|email|text|message|remind|remember|plan|schedule)\b'
        if re.search(activity_words, user_lower):
            # Avoid false positives for questions like "what to do"
            if not re.search(r'\b(what|whats|how|why|when|where|who|which)\b.*\b(to|do|have)\b', user_lower):
                return {
                    "action": ChatAction.ADD,
                    "parameters": {"title": user_input.strip()},
                    "confidence": 0.6,
                    "original_text": user_input
                }

        # Check for action phrases with time/activity indicators
        action_phrases = r'.*\b(for|with|at|after|before|during|by)\s+(?:the\s+)?(?:morning|evening|afternoon|night|day|week|month|year|tomorrow|yesterday|today|tonight|monday|tuesday|wednesday|thursday|friday|saturday|sunday|january|february|march|april|may|june|july|august|september|october|november|december)\b.*'
        if re.search(action_phrases, user_lower):
            return {
                "action": ChatAction.ADD,
                "parameters": {"title": user_input.strip()},
                "confidence": 0.6,
                "original_text": user_input
            }

        # If no specific pattern matches, return no action
        return {
            "action": ChatAction.NONE,
            "parameters": {},
            "confidence": 0.5,
            "original_text": user_input
        }

    def _extract_parameters(self, user_input: str, intent: str, conversation_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extract specific parameters based on the identified intent.
        """
        if intent == "ADD":
            # Extract the title for a new todo
            # Look for common patterns like "add a todo to [title]" or "add [title]"
            add_patterns = [
                r"(?:add|create|make|new)\s+(?:a\s+)?(?:todo|task|item|thing)\s+(?:to\s+)?(.+)",
                r"(?:add|create|make|new)\s+(?:a\s+)?(.+)",
            ]

            for pattern in add_patterns:
                match = re.search(pattern, user_input.lower())
                if match:
                    title = match.group(1).strip()
                    if title:
                        return {"title": title}

            # If no match, return the entire input as title
            return {"title": user_input.strip()}

        elif intent == "UPDATE":
            # Extract todo reference and potential new details
            return {"reference": user_input.strip()}

        elif intent in ["COMPLETE", "DELETE"]:
            # Extract todo reference
            return {"reference": user_input.strip()}

        else:
            return {}

    def _map_intent_to_action(self, intent: str) -> ChatAction:
        """
        Map string intent to ChatAction enum.
        """
        intent_map = {
            "ADD": ChatAction.ADD,
            "LIST": ChatAction.LIST,
            "UPDATE": ChatAction.UPDATE,
            "DELETE": ChatAction.DELETE,
            "COMPLETE": ChatAction.COMPLETE,
            "PROFILE": ChatAction.PROFILE
        }

        return intent_map.get(intent.upper(), ChatAction.NONE)