from bot.dialogs.flows.start.dialog import start_dialog
from bot.dialogs.flows.start.handlers import start_router

DIALOGS = [
    start_dialog,
]

ROUTERS = [
    start_router,
]

__all__ = [
    'DIALOGS',
    'ROUTERS',
    'start_router',
    'start_dialog',
]
