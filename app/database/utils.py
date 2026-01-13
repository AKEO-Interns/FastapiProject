from sqlalchemy.orm import Session

def soft_delete(db: Session, obj):
    obj.is_deleted = True
    db.add(obj)
    db.commit()
    db.refresh(obj)
