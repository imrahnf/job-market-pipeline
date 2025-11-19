# src/cleaning/salary_parser.py
import re
from typing import Optional, Tuple

pattern = re.compile(
    r'(?<=\$)(?P<start>\d(?:,?\d)*(?:\.\d\d)?)(?:\s*-\s*\$?(?P<end>\d(?:,?\d)*(?:\.\d\d)?))?\s+per\s+(?P<period>year|month|day|hour)',
    flags=re.M
)

SALARY_REGEX = re.compile(
    r"\$?\s?(\d{2,3}[,]?\d{0,3})\s?[-to–]+\s?\$?\s?(\d{2,3}[,]?\d{0,3})",
    re.IGNORECASE
)

SINGLE_SALARY_REGEX = re.compile(
    r"\$?\s?(\d{2,3}[,]?\d{0,3})\s?(per year|yearly|annually|/yr)",
    re.IGNORECASE
)

# just remove commans for cnosistent formatting
def clean_number(num_str: str) -> int:
    return int(num_str.replace(",", ""))

def parse_salary(text: str) -> Optional[Tuple[int, int]]:
    if not text:
        return None
    
    # Range ex: "$80,000 - $120,000"
    match = SALARY_REGEX.search(text)
    if match:
        low, high = match.groups()
        return (clean_number(low), clean_number(high))
    
    # Single ex: "$80,000 per year"
    match = SINGLE_SALARY_REGEX.search(text)
    if match:
        value = match.group(1)
        clean = clean_number(value)
        return (clean, clean)
    
    return None