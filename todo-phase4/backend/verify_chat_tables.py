"""
Script to verify that chat-related database tables exist.
"""
from sqlalchemy import text
from db.connection import engine

def verify_chat_tables():
    """Verify that chat-related tables exist in the database."""
    print("Verifying chat-related tables...")

    with engine.connect() as conn:
        # Query to check if tables exist (PostgreSQL specific)
        result = conn.execute(text("""
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public'
            AND tablename IN ('conversations', 'messages')
        """))

        existing_tables = [row[0] for row in result.fetchall()]

        print(f"Found tables: {existing_tables}")

        if 'conversations' in existing_tables:
            print("[OK] Conversations table exists")
        else:
            print("[MISSING] Conversations table missing")

        if 'messages' in existing_tables:
            print("[OK] Messages table exists")
        else:
            print("[MISSING] Messages table missing")

        # Check if the foreign key relationship exists properly
        if 'messages' in existing_tables:
            fk_result = conn.execute(text("""
                SELECT
                    tc.table_name,
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM
                    information_schema.table_constraints AS tc
                    JOIN information_schema.key_column_usage AS kcu
                      ON tc.constraint_name = kcu.constraint_name
                      AND tc.table_schema = kcu.table_schema
                    JOIN information_schema.constraint_column_usage AS ccu
                      ON ccu.constraint_name = tc.constraint_name
                      AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY'
                AND tc.table_name = 'messages'
                AND kcu.column_name = 'conversation_id'
            """))

            fk_exists = fk_result.fetchone()
            if fk_exists:
                print("[OK] Foreign key relationship exists (messages.conversation_id -> conversations.id)")
            else:
                print("[INFO] Foreign key relationship may be missing")

    print("\nVerification complete!")

if __name__ == "__main__":
    verify_chat_tables()