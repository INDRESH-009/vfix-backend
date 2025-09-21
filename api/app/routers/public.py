from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.core.db import get_db
from app.models.models import Issue
from app.utils.geo import round_public

router = APIRouter()

@router.get("/issues")
def public_issues(
    bbox: str = Query(..., description="minLng,minLat,maxLng,maxLat"),
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        minLng, minLat, maxLng, maxLat = [float(x) for x in bbox.split(",")]
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid bbox")
    q = db.query(Issue).filter(
        (Issue.lng/1e6 >= minLng) & (Issue.lng/1e6 <= maxLng) &
        (Issue.lat/1e6 >= minLat) & (Issue.lat/1e6 <= maxLat) &
        (Issue.public_visibility == True)
    )
    if category:
        q = q.filter(Issue.category == category)
    out = []
    for i in q.limit(500).all():
        lat, lng = round_public(i.lat/1e6, i.lng/1e6, precision=4)
        out.append({
            "id": str(i.id),
            "status": i.status,
            "category": i.category,
            "severity": i.severity,
            "lat": lat,
            "lng": lng,
            "created_at": i.created_at,
            "thumb": i.media[0].url if i.media else None
        })
    return {"items": out}
