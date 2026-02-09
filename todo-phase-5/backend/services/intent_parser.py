import re
from typing import Dict, List, Optional, Tuple
from enum import Enum

class IntentType(Enum):
    ADD_TASK = "ADD_TASK"
    DELETE_TASK = "DELETE_TASK"
    COMPLETE_TASK = "COMPLETE_TASK"
    LIST_TASKS = "LIST_TASKS"
    UPDATE_TASK = "UPDATE_TASK"
    CLARIFICATION_NEEDED = "CLARIFICATION_NEEDED"

class IntentParser:
    def __init__(self):
        self.rules = {
            IntentType.ADD_TASK: [
                r'\b(add|create|make|new)\s+(?:task\s+)?(.+)$',
                r'\b(create|add)\s+(.+)$'
            ],
            IntentType.DELETE_TASK: [
                r'\b(delete|remove|kill)\s+task\s+(\d+)$',
                r'\b(delete|remove)\s+task\s+[\'"]([^\'"]+)[\'"]$',
                r'\b(delete|remove)\s+(.+)$'
            ],
            IntentType.COMPLETE_TASK: [
                r'\b(mark|complete|finish)\s+task\s+(\d+)\s+(?:as\s+)?(done|completed)$',
                r'\b(mark|complete|finish)\s+(.+\d+)\s+(?:as\s+)?(done|completed)$',
                r'\b(done|complete|finish)\s+task\s+(\d+)$',
                r'\b(done|complete|finish)\s+(.+)$'
            ],
            IntentType.LIST_TASKS: [
                r'\b(show|list|display|view|see)\s+(?:my\s+)?tasks?\b',
                r'\b(what|whats)\s+(?:do\s+i\s+have|are\s+my)\s+(?:to\s+do|tasks?)\b',
                r'\btasks?\b'
            ],
            IntentType.UPDATE_TASK: [
                r'\b(update|change|modify|edit)\s+task\s+(\d+)\s+(?:to|with)\s+(.+)$',
                r'\b(update|change|modify|edit)\s+(.+)\s+to\s+(.+)$'
            ]
        }

    def parse(self, message: str) -> Tuple[IntentType, Dict[str, str]]:
        """
        Parse user message and return intent with extracted parameters.

        Args:
            message: User input message

        Returns:
            Tuple of (IntentType, parameters_dict)
        """
        message = message.strip().lower()

        # Check each intent type
        for intent_type, patterns in self.rules.items():
            for pattern in patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    params = self._extract_parameters(intent_type, match.groups())

                    # Validate required parameters
                    if self._validate_intent_params(intent_type, params):
                        return intent_type, params

        # No clear intent found
        return IntentType.CLARIFICATION_NEEDED, {
            "original_message": message,
            "suggestions": [
                "To add a task: 'add buy groceries'",
                "To delete a task: 'delete task 2'",
                "To complete a task: 'mark task 1 as done'",
                "To see tasks: 'show my tasks'"
            ]
        }

    def _extract_parameters(self, intent_type: IntentType, groups: tuple) -> Dict[str, str]:
        """
        Extract parameters based on intent type and regex groups.
        """
        params = {}

        if intent_type == IntentType.ADD_TASK:
            # groups[0] = full match, groups[1] = title
            if len(groups) > 1 and groups[1]:
                params['title'] = groups[1].strip()
        elif intent_type in [IntentType.DELETE_TASK, IntentType.COMPLETE_TASK]:
            # Could be ID (groups[1]) or title (groups[2] or groups[0])
            if len(groups) > 1 and groups[1] and groups[1].isdigit():
                params['task_id'] = int(groups[1])
            elif len(groups) > 2 and groups[2]:  # quoted title
                params['title'] = groups[2].strip()
            elif len(groups) > 0 and groups[0]:
                params['title'] = groups[0].strip()
        elif intent_type == IntentType.LIST_TASKS:
            # No parameters needed
            pass
        elif intent_type == IntentType.UPDATE_TASK:
            if len(groups) > 2:
                if groups[1] and groups[1].isdigit():
                    params['task_id'] = int(groups[1])
                    params['new_title'] = groups[2].strip()
                else:
                    params['title'] = groups[1].strip()
                    params['new_title'] = groups[2].strip()

        return params

    def _validate_intent_params(self, intent_type: IntentType, params: Dict[str, str]) -> bool:
        """
        Validate that required parameters are present for the intent.
        """
        if intent_type == IntentType.ADD_TASK:
            return 'title' in params and bool(params['title'].strip())
        elif intent_type in [IntentType.DELETE_TASK, IntentType.COMPLETE_TASK]:
            return 'task_id' in params or 'title' in params
        elif intent_type == IntentType.UPDATE_TASK:
            return ('task_id' in params or 'title' in params) and 'new_title' in params
        # LIST_TASKS doesn't require parameters
        return True

    def validate_strict_execution(self, intent_type: IntentType, params: Dict[str, str]) -> Tuple[bool, str]:
        """
        Validate that the intent execution follows strict rules.

        Returns:
            Tuple of (is_valid, error_message_if_invalid)
        """
        if intent_type == IntentType.DELETE_TASK or intent_type == IntentType.COMPLETE_TASK:
            if 'title' in params and params['title']:
                # If using title, we'll need to resolve it to an ID later
                return True, ""
            elif 'task_id' in params and params['task_id']:
                # If using ID, validate it's a number
                if isinstance(params['task_id'], int) or (isinstance(params['task_id'], str) and params['task_id'].isdigit()):
                    return True, ""
                else:
                    return False, f"Task ID must be a number, got: {params['task_id']}"
            else:
                return False, "Either task ID or title must be provided for deletion/completion"

        elif intent_type == IntentType.ADD_TASK:
            if 'title' not in params or not params['title'].strip():
                return False, "Task title is required for adding a task"
            return True, ""

        return True, ""