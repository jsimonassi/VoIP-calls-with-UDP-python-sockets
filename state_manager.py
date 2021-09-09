from enum import Enum


class CallState(Enum):
    IN_CALL = 0
    IDLE = 1


class StateManager:
    call_state: CallState

    def __init__(self):
        self.call_state = CallState.IDLE

    def get_current_state(self):
        return self.call_state

    def set_current_state(self, new_state):
        self.call_state = new_state
