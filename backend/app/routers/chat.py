from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ChatMessage, Material
from app.schemas import ChatMessageOut, ChatReplyOut, CreateChatMessage
from app.services.ai import generate_chat_reply

router = APIRouter(prefix="/api/chat", tags=["chat"])


def _to_out(msg: ChatMessage) -> ChatMessageOut:
    return ChatMessageOut(
        id=msg.id,
        material_id=msg.material_id,
        role=msg.role,
        content=msg.content,
        generated_by=msg.generated_by,
        language=msg.language,
        created_at=msg.created_at,
    )


def _history(db: Session, material_id: int) -> list[dict]:
    """Conversation as plain dicts, oldest first (ends with latest question)."""
    return [
        {"role": m.role, "content": m.content}
        for m in (
            db.query(ChatMessage)
            .filter(ChatMessage.material_id == material_id)
            .order_by(ChatMessage.id.asc())
            .all()
        )
    ]


@router.get("", response_model=list[ChatMessageOut])
def get_chat_messages(
    material_id: int = Query(...), db: Session = Depends(get_db)
):
    material = db.get(Material, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found.")

    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.material_id == material_id)
        .order_by(ChatMessage.id.asc())
        .all()
    )
    return [_to_out(m) for m in messages]


@router.post("", response_model=ChatReplyOut, status_code=201)
def create_chat_message(payload: CreateChatMessage, db: Session = Depends(get_db)):
    material = db.get(Material, payload.material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found.")

    user_msg = ChatMessage(
        material_id=material.id,
        role="user",
        content=payload.content,
        generated_by="",
        language=payload.language,
    )
    db.add(user_msg)
    db.flush()

    history = _history(db, material.id)

    generated_by, reply, warning = generate_chat_reply(
        material.content,
        history,
        provider=payload.provider,
        model_name=payload.model_name,
        language=payload.language,
    )

    assistant_msg = ChatMessage(
        material_id=material.id,
        role="assistant",
        content=reply,
        generated_by=generated_by,
        language=payload.language,
    )
    db.add(assistant_msg)
    db.commit()
    db.refresh(user_msg)
    db.refresh(assistant_msg)

    return ChatReplyOut(
        user_message=_to_out(user_msg),
        assistant_message=_to_out(assistant_msg),
        warning=warning or None,
    )


@router.delete("", status_code=204)
def clear_chat(material_id: int = Query(...), db: Session = Depends(get_db)):
    material = db.get(Material, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found.")

    db.query(ChatMessage).filter(ChatMessage.material_id == material_id).delete()
    db.commit()