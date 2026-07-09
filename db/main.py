import sqlite3
import json
import os

def migrate_json_to_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # .../db
    PROJECT_ROOT = os.path.dirname(BASE_DIR)                        # .../Job application assistant
    db_path = os.path.join(PROJECT_ROOT, "DATA", "resume.db")


    resumes_to_migrate = {
        "Power Platfrom Resume" : "resume_pp.json",
        "DevOps Resume": "resume_devops.json"
    }

    DEFAULT_USER_ID = 1

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    print("started migrating to database")

    for resume_name,file_name in resumes_to_migrate.items():
        if not os.path.exists(file_name):
            print(f"{file_name} not found skipping")
            continue
        try:
            with open(file_name,) as f:
                resume_data = json.load(f)
            serialized_json = json.dumps(resume_data)

            query = """
                    INSERT INTO resumes (user_id,name,resume_json,updated_at) 
                    VALUES (?,?,?,datetime('now'))
                    """
            cursor.execute(query,(DEFAULT_USER_ID,resume_name,serialized_json))
            print(f"sucessfully migrated {file_name}")
        except Exception as e:
            print(f"failed to migrate {file_name} : {e}")
    conn.commit()
    conn.close()
    print("Migration complete!")

if __name__ == "__main__":
    migrate_json_to_db()

    