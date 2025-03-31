from pathlib import Path

# Application settings
APP_NAME = "User Generator"
APP_VERSION = "1.0.0"
WINDOW_SIZE = (1200, 600)
SPLITTER_RATIO = (60, 40)

# File paths
ROOT_DIR = Path(__file__).parent.parent.parent
RESOURCES_DIR = ROOT_DIR / "resources"
ICON_PATH = RESOURCES_DIR / "icons" / "app_icon.ico"

# User generation settings
MAX_ATTEMPTS_MULTIPLIER = 10
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 20
PASSWORD_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+"