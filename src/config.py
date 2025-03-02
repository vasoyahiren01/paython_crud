import json
import os
from typing import Dict, Any

def load_config(file_path: str) -> Dict[str, Any]:
    """Load configuration from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

# Load database configuration
config = load_config('db_config.json')

# Login expiration time in seconds
LOGIN_EXPIRE: int = int(os.getenv('LOGIN_EXPIRE', 3600))  # Use environment variable if available