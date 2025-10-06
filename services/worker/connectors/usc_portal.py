import json, os
from datetime import datetime
from services.api.utils import stable_job_uid

def fetch():
    path = os.path.join(os.path.dirname(__file__), "../seed/usc.json")
    with open(path) as f: data = json.load(f)
    out=[]
    for r in data.get("results", []):
        uid = stable_job_uid(r["company"], r["title"], r.get("location"), r.get("posted_at","")[:10])
        out.append({
            "job_uid": uid, "source":"usc_portal", "title": r["title"], "company": r["company"],
            "location": r.get("location"), "employment_type": r.get("employment_type","Internship"),
            "remote_ok": bool(r.get("remote")), "visa_friendly": None,
            "posted_date": datetime.fromisoformat(r["posted_at"]) if r.get("posted_at") else None,
            "link": r.get("apply_url"), "skills": r.get("skills", []), "description": r.get("description","")
        })
    return out
