from utils.debug import Debug, catch_exceptions
from utils.misc import copy_to_clipboard
from .context import Context

try:
    import EDMCHotkeys as hotkeys #type: ignore
except ImportError:
    Debug.logger.warning(f"EDMC Hotkeys not installed")
    hotkeys = None


class Hotkeys:        
    # Singleton pattern
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # Only initialize if it's the first time
        if hasattr(self, '_initialized'): return

        if not hotkeys: return
        
        for cmd in ["next", "previous", "copy"]:
            if not hotkeys.register_action(
                hotkeys.Action(id=f"{Context.plugin_name}-{cmd}",
                            label=cmd,
                            plugin=Context.plugin_name,
                            callback=self.callback,
                            thread_policy="main",
                            cardinality="single",
                            payload={"cmd": cmd}
                            )):
                Debug.logger.debug(f"Error registering {cmd} hotkey")
        self._initialized = True

    @staticmethod
    def callback(*, payload:dict|None = None, source:str = "hotkey", hotkey:str|None = None) -> None:    
        match (payload or {}).get('cmd', ''):
            case 'next':
                Context.ui.goto_next_waypoint()
            case 'previous':
                Context.ui.goto_prev_waypoint()
            case _:
                copy_to_clipboard(Context.ui.parent, Context.route.next_stop())
