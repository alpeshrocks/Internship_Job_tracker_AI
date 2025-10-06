import hashlib, re
from datetime import datetime

def normalize_text(s: str | None) -> str:
    if not s: return ""
    return re.sub(r"\s+", " ", s).strip()

def stable_job_uid(company: str, title: str, location: str | None, posted_date: str | None) -> str:
    c = normalize_text(company).lower()
    t = normalize_text(title).lower()
    l = (normalize_text(location) or "").lower()
    d = posted_date or datetime.utcnow().date().isoformat()
    return hashlib.sha256(f"{c}|{t}|{l}|{d}".encode()).hexdigest()
