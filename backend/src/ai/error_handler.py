from typing import Dict, Any, Optional
from ..schemas.chat_schemas import ChatAction


class ErrorHandler:
    """
    Handler for AI errors and ambiguous requests.
    Provides appropriate responses when requests are unclear or fail.
    """

    def __init__(self):
        pass

    def handle_ambiguous_request(self, user_input: str, available_actions: Optional[list] = None) -> Dict[str, Any]:
        """
        Handle requests that are ambiguous or unclear.
        """
        if available_actions is None:
            available_actions = ["add", "list", "update", "delete", "complete"]

        # Determine the type of ambiguity
        ambiguity_type = self._identify_ambiguity_type(user_input)

        if ambiguity_type == "multiple_targets":
            return {
                "action": ChatAction.NONE,
                "clarification_needed": True,
                "message": f"I found multiple items that match your request. Could you be more specific? For example: 'complete the grocery todo' instead of just 'complete the todo'.",
                "suggestions": self._generate_suggestions(user_input, available_actions)
            }
        elif ambiguity_type == "unclear_action":
            return {
                "action": ChatAction.NONE,
                "clarification_needed": True,
                "message": f"I'm not sure what you'd like me to do with '{user_input}'. Could you clarify?",
                "suggestions": self._generate_suggestions(user_input, available_actions)
            }
        else:
            return {
                "action": ChatAction.NONE,
                "clarification_needed": True,
                "message": f"I'm not quite sure how to handle '{user_input}'. Could you rephrase or be more specific?",
                "suggestions": self._generate_suggestions(user_input, available_actions)
            }

    def handle_invalid_request(self, user_input: str, error_details: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle requests that are invalid or cannot be processed.
        """
        return {
            "action": ChatAction.NONE,
            "error": True,
            "message": f"I couldn't process your request '{user_input}'. {error_details or 'Please try rephrasing.'}",
            "suggestions": self._generate_suggestions(user_input)
        }

    def handle_missing_context(self, user_input: str, required_context: str) -> Dict[str, Any]:
        """
        Handle requests that lack necessary context.
        """
        return {
            "action": ChatAction.NONE,
            "clarification_needed": True,
            "message": f"To {required_context}, I need more information. Could you provide more details about '{user_input}'?",
            "suggestions": self._generate_suggestions(user_input)
        }

    def _identify_ambiguity_type(self, user_input: str) -> str:
        """
        Identify the type of ambiguity in the user input.
        """
        user_lower = user_input.lower()

        # Check for ambiguous references like "it", "that", "the first one", etc.
        ambiguous_refs = ["it", "that", "the first", "the last", "one", "thing"]
        for ref in ambiguous_refs:
            if ref in user_lower:
                return "multiple_targets"

        # Check for unclear action requests
        unclear_phrases = ["something", "stuff", "anything", "whatever"]
        for phrase in unclear_phrases:
            if phrase in user_lower:
                return "unclear_action"

        return "other"

    def _generate_suggestions(self, user_input: str, available_actions: Optional[list] = None) -> list:
        """
        Generate helpful suggestions based on the user input.
        """
        if available_actions is None:
            available_actions = ["add", "list", "update", "delete", "complete"]

        suggestions = []

        # Add general suggestions based on available actions
        for action in available_actions:
            if action == "add":
                suggestions.append(f"Add a todo: 'Add a todo to buy groceries'")
            elif action == "list":
                suggestions.append(f"List todos: 'Show me my todos'")
            elif action == "update":
                suggestions.append(f"Update a todo: 'Update my meeting todo to tomorrow'")
            elif action == "delete":
                suggestions.append(f"Delete a todo: 'Delete the grocery shopping todo'")
            elif action == "complete":
                suggestions.append(f"Complete a todo: 'Mark the first todo as complete'")

        return suggestions[:3]  # Return only the first 3 suggestions