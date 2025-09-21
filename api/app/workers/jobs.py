from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from uuid import UUID
from datetime import timedelta, datetime
from rapidfuzz import fuzz
from app.core.config import settings
from app.models.models import Issue, ActionLog

engine = create_engine(
    f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def severity_from_text(text: str, category: str | None) -> int:
    text_l = (text or "").lower()
    score = 0
    for kw, pts in [
        ("accident", 3), ("fire", 5), ("flood", 5), ("overflow", 2),
        ("blocked", 2), ("leak", 2), ("electric", 4), ("gas", 5), ("school", 1)
    ]:
        if kw in text_l: score += pts
    if category:
        score += {"Sanitation":1, "Roads":2, "Electricity":3, "Water":3}.get(category, 0)
    return max(0, min(5, round(score/2)))

def triage_issue(issue_id: str):
    db = SessionLocal()
    try:
        issue = db.get(Issue, UUID(issue_id))
        if not issue: return
        sev = severity_from_text(issue.description, issue.category)
        issue.severity = sev

        # naive duplicate (same reporter, ~100m, similar text)
        lat = issue.lat/1e6; lng = issue.lng/1e6
        candidates = db.query(Issue).filter(Issue.reporter_id==issue.reporter_id).order_by(Issue.created_at.desc()).limit(20).all()
        for c in candidates:
            if c.id == issue.id: continue
            dlat = abs((c.lat or 0)/1e6 - lat); dlng = abs((c.lng or 0)/1e6 - lng)
            if dlat < 0.001 and dlng < 0.001:  # ~100m
                sim = fuzz.token_sort_ratio(issue.description or "", c.description or "")
                if sim > 85:
                    issue.duplicate_group_id = c.duplicate_group_id or c.id
                    db.add(ActionLog(issue_id=issue.id, actor_role="system", type="system_dedupe",
                                     payload={"like": str(c.id), "similarity": sim}))
                    break

        db.add(issue); db.commit()
    finally:
        db.close()

def compute_sla(issue_id: str):
    db = SessionLocal()
    try:
        issue = db.get(Issue, UUID(issue_id))
        if not issue: return
        base = 24  # hours
        mult = {0:1.0,1:1.0,2:0.8,3:0.6,4:0.4,5:0.3}.get(issue.severity or 0, 1.0)
        due = (issue.created_at or datetime.utcnow()) + timedelta(hours=base*mult)
        issue.sla_due_at = due
        db.add(issue); db.commit()
    finally:
        db.close()
