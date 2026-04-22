from fastapi import APIRouter, Depends

from app.api.deps import require_roles
from app.models import Message, UserRole

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get(
    "/",
    dependencies=[Depends(require_roles(UserRole.admin, UserRole.manager))],
    response_model=Message,
)
def read_metrics() -> Message:
    return Message(message="Metrics are available for admin and manager roles.")
