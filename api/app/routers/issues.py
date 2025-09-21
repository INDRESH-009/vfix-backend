from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.core.db import get_db
from app.models.models import Issue, Media, ActionLog, User
from app.routers.me import get_current_user
from app.schemas.schemas import IssueCreateIn, IssueOut, IssueListOut
from app.utils.media import strip_exif, compute_phash, get_mime_from_bytes
from app.utils.s3 import upload_bytes
from app.workers.enqueue import enqueue_triage, enqueue_sla_compute

router = APIRouter()

def issue_to_out(i: Issue) -> IssueOut:
    return IssueOut(
        id=i.id,
        status=i.status,
        severity=i.severity,
        category=i.category,
        sla_due_at=i.sla_due_at,
        lat=(i.lat or 0)/1e6,
        lng=(i.lng or 0)/1e6,
        address=i.address,
        title=i.title,
        description=i.description,
        media=[
            {"id": m.id, "role": m.role, "url": m.url, "created_at": m.created_at}
            for m in sorted(i.media, key=lambda x: x.created_at or 0, reverse=False)
        ],
        created_at=i.created_at
    )

@router.post("")
async def create_issue(
    json_str: str = Form(...),
    # Accept BOTH `photos` and `photos[]` field names
    photos: Optional[List[UploadFile]] = File(None),
    photos_brackets: Optional[List[UploadFile]] = File(None, alias="photos[]"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        data = IssueCreateIn.model_validate_json(json_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON in 'json' field")

    if not data.consent:
        raise HTTPException(status_code=400, detail="Consent required")

    issue = Issue(
        reporter_id=user.id,
        title=data.title,
        description=data.description,
        category=data.category,
        status="new",
        lat=int(data.lat * 1e6),
        lng=int(data.lng * 1e6),
        address=data.address,
        public_visibility=data.public_visibility,
    )
    db.add(issue)
    db.commit()
    db.refresh(issue)

    # merge both possible photo lists
    all_photos: List[UploadFile] = []
    if photos:
        all_photos.extend(photos)
    if photos_brackets:
        all_photos.extend(photos_brackets)

    if all_photos:
        for f in all_photos:
            raw = await f.read()
            clean = strip_exif(raw)
            mime = get_mime_from_bytes(clean)
            url = upload_bytes(clean, mime)
            phash = compute_phash(clean)
            m = Media(issue_id=issue.id, role="before", url=url, phash=phash, exif_json={})
            db.add(m)

    db.add(ActionLog(
        issue_id=issue.id,
        actor_id=user.id,
        actor_role="citizen",
        type="created",
        payload={"category": data.category}
    ))
    db.commit()
    db.refresh(issue)  # ensure media relationship is visible in response

    enqueue_triage(issue.id)
    enqueue_sla_compute(issue.id)

    return issue_to_out(issue)

@router.get("/mine", response_model=IssueListOut)
def list_my_issues(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    q = db.query(Issue).filter(Issue.reporter_id == user.id).order_by(Issue.created_at.desc()).limit(50)
    items = [issue_to_out(i) for i in q.all()]
    return {"items": items, "next_cursor": None}

@router.get("/{issue_id}", response_model=IssueOut)
def get_issue(issue_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    i = db.get(Issue, issue_id)
    if not i or i.reporter_id != user.id:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue_to_out(i)
