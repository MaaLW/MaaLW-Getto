from .storage import VariableStorage, VarDict
from ..corethread import (CoreThread,
                          logger,
                          Message,
                          Command)

class VarsPool(CoreThread):
    def __init__(self, db_url = None, **kwargs):
        super().__init__(**kwargs)
        self.storage = VariableStorage() if db_url is None else VariableStorage(db_url)
        self.storage.load_all()  # Load from db at init

    def _process(self, msg: Message, priority=100):
        logger.debug("VarsPool processing %s", msg)
        if msg.command == Command.SET_VARIABLE:
            self._handle_set_variable(msg.content)
        # Other commands

    def _handle_set_variable(self, data: dict[str, object]):
        """Handle SET_VARIABLE command"""
        name = data.get("name")
        value = data.get("value")
        try:
            self.storage.update_variable(name, value)
        except Exception as e:
            logger.error(f"Error updating variable: {name}={value}, Exception: {e}")

    def get_variable(self, name: str) -> VarDict[str, object] | None:
        """Unblocking get variable"""
        return self.storage.get_variable(name)