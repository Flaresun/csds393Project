import bcrypt 
from prisma import Prisma
from prisma.models import User

def hash_password(password : str) -> str:
    """Hashes the password using bcrypt"""
    bytes_password : bytes = password.encode()
    hashed_password : bytes = bcrypt.hashpw(bytes_password, bcrypt.gensalt())
    return hashed_password.decode("utf-8")
def compare_password(password : bytes, user_password : bytes) -> bool:
    """Compares the given password with the hashed user_password"""
    if bcrypt.checkpw(password, user_password):
        return True 
    return False
async def get_all_users(db):
    try:
        users = await db.user.find_many()
        return users
    except Exception as e:
        return {}
    
async def get_user_by_email(db,email : str) -> dict:
    await db.disconnect()
    await db.connect()
    try:
        users = await db.user.find_many(
            where={
                "OR":[
                    {"email":{"contains":email}}
                ]
            }
        )
        
        return dict(users[0])
    except Exception as e:
        print(e)
        return {}

async def get_notes_by_class_name(db, class_name: str) -> list[dict]:
    await db.disconnect()
    await db.connect()
    try:
        notes = await db.note.find_many(
            where={"className": class_name}  # only gets exact matches
        )
        return [dict(note) for note in notes]
    except Exception as e:
        print(e)
        return []
