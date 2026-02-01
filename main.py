from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=os.getenv("MYSQLPORT"),
    )

@app.get("/api/profile")
def get_profile():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
                SELECT
                    display_name,
                    date_of_birth,
                    address,
                    phone_number,
                    hobbies,
                    favorite_foods 
                FROM user_profiles
                WHERE deleted_at IS NULL
                ORDER BY id
                """)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    profiles = []

    # DBカラム名 → 表示ラベル の対応表
    fields = {
        "display_name": "名前",
        "date_of_birth": "生年月日",
        "address": "住所",
        "phone_number": "電話番号",
        "hobbies": "趣味",
        "favorite_foods": "好きな食べ物"
    }

    for row in rows:
        for key, label in fields.items():
            value = row.get(key)

            if value:
                profiles.append({
                    "label": label,
                    "value": str(value)
                })

    return {
        "note": "",
        "profiles": profiles
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
