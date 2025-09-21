from redis import Redis
import redis as redislib
from rq import Queue
from app.core.config import settings

_redis = redislib.Redis.from_url(settings.REDIS_URL)
triage_q = Queue("triage", connection=_redis)
notifications_q = Queue("notifications", connection=_redis)
maintenance_q = Queue("maintenance", connection=_redis)

def enqueue_triage(issue_id):
    triage_q.enqueue("app.workers.jobs.triage_issue", str(issue_id), job_timeout=120)

def enqueue_sla_compute(issue_id):
    triage_q.enqueue("app.workers.jobs.compute_sla", str(issue_id), job_timeout=60)
