import random
import string
from db import code_exists, insert_mapping

def generate_code():
    """
    Generate a unique code with format: AAAA12345Z
    - 4 uppercase letters
    - 5 digits
    - 1 uppercase letter
    """
    # Generate 4 random uppercase letters
    letters_part1 = ''.join(random.choices(string.ascii_uppercase, k=4))
    
    # Generate 5 random digits
    digits_part = ''.join(random.choices(string.digits, k=5))
    
    # Generate 1 random uppercase letter
    letter_part2 = random.choice(string.ascii_uppercase)
    
    # Combine all parts
    code = letters_part1 + digits_part + letter_part2
    
    return code

def generate_unique_code(database_url=None, max_attempts=100):
    """
    Generate a unique code that doesn't exist in the database.

    Uses the configured PostgreSQL DB (temporary by default; set DATABASE_URL for the original db).

    Args:
        database_url: PostgreSQL connection URL (optional). Uses default if None.
        max_attempts: Maximum number of attempts to generate a unique code.

    Returns:
        A unique code string.

    Raises:
        RuntimeError: If unable to generate a unique code after max_attempts
    """
    for _ in range(max_attempts):
        code = generate_code()

        if not code_exists(code, database_url):
            insert_mapping(code, code, database_url)  # no-op; code is stored in products by app
            return code

    raise RuntimeError(f"Failed to generate unique code after {max_attempts} attempts")
