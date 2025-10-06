from sqlalchemy import select, desc, func
from sqlalchemy.orm import Session
from typing import Optional
from services.api.models import Job, Application

def _parse_skills(s: str | None) -> list[str]:
    if not s: return []
    return [x.strip() for x in s.split(",") if x.strip()]

def upsert_jobs(db: Session, jobs: list[dict]) -> int:
    inserted = 0
    for j in jobs:
        existing = db.execute(select(Job).where(Job.job_uid == j["job_uid"])).scalar_one_or_none()
        if existing:
            existing.link = j.get("link", existing.link)
            if j.get("description"): existing.description = j["description"]
            if j.get("skills"): existing.skills = ", ".join(j["skills"])
        else:
            obj = Job(
                job_uid=j["job_uid"],
                source=j["source"],
                title=j["title"],
                company=j["company"],
                location=j.get("location"),
                employment_type=j.get("employment_type","Internship"),
                remote_ok=j.get("remote_ok"),
                visa_friendly=j.get("visa_friendly"),
                posted_date=j.get("posted_date"),
                link=j["link"],
                skills=(", ".join(j.get("skills")) if j.get("skills") else None),
                description=j.get("description"),
            )
            db.add(obj); inserted += 1
    db.commit()
    return inserted

def search_jobs(db: Session, q: Optional[str], source: Optional[str], applied: Optional[bool], limit:int, offset:int):
    stmt = select(Job).order_by(desc(Job.posted_date), desc(Job.scraped_at)).limit(limit).offset(offset)
    if q:
        like = f"%{q.lower()}%"
        stmt = stmt.where((func.lower(Job.title).like(like)) | (func.lower(Job.company).like(like)) | (func.lower(Job.description).like(like)))
    if source:
        stmt = stmt.where(Job.source == source)

    rows = db.execute(stmt).scalars().all()
    out = []
    for r in rows:
        app = db.execute(select(Application).where(Application.job_id == r.id).order_by(desc(Application.updated_at)).limit(1)).scalar_one_or_none()
        out.append({
            "id": r.id,
            "job_uid": r.job_uid,
            "source": r.source,
            "title": r.title,
            "company": r.company,
            "location": r.location,
            "employment_type": r.employment_type,
            "remote_ok": r.remote_ok,
            "visa_friendly": r.visa_friendly,
            "posted_date": r.posted_date.isoformat() if r.posted_date else None,
            "scraped_at": r.scraped_at.isoformat() if r.scraped_at else None,
            "link": r.link,
            "skills": _parse_skills(r.skills),
            "description": r.description,
            "applied": bool(app.applied) if app else False,
            "saved": bool(app.saved) if app else False,
            "notes": app.notes if app else None,
        })
    if applied is not None:
        out = [x for x in out if x["applied"] == applied]
    return out

def update_application(db: Session, job_id: int, patch: dict) -> dict:
    j = db.get(Job, job_id)
    if not j: return {"ok": False, "error":"job not found"}
    app = db.execute(select(Application).where(Application.job_id == job_id).order_by(desc(Application.updated_at)).limit(1)).scalar_one_or_none()
    if not app:
        app = Application(job_id=job_id)
        db.add(app)
    if "applied" in patch and patch["applied"] is not None: app.applied = bool(patch["applied"])
    if "saved" in patch and patch["saved"] is not None: app.saved = bool(patch["saved"])
    if "notes" in patch and patch["notes"] is not None: app.notes = str(patch["notes"])
    if "cold_email_sent" in patch and patch["cold_email_sent"] is not None: app.cold_email_sent = bool(patch["cold_email_sent"])
    db.commit()
    return {"ok": True}
