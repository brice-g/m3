"""
Collecte rapide des emails support FastIA depuis un fichier mbox.

TODO (Tom, avant depart):
  - tester sur les vieux mails exportes depuis Outlook (encodages bizarres)
  - voir avec l'equipe data si on doit gerer les doublons cote script ou cote SQL
  - ajouter un mode --dry-run un jour
"""

import mailbox
import os
import sys
from datetime import datetime
from email.utils import parsedate

import psycopg2


DB_DSN = os.environ.get(
    "FASTIA_DB_DSN",
    "postgresql://fastia:fastia@localhost:5432/fastia",
)


def extract_body(msg):
    """Recupere le corps texte d'un message (best effort)."""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode("utf-8")
        return ""
    payload = msg.get_payload(decode=True)
    if payload:
        return payload.decode("utf-8")
    return ""


def collect(mbox_path):
    box = mailbox.mbox(mbox_path)
    conn = psycopg2.connect(DB_DSN)
    cur = conn.cursor()

    inserted = 0
    skipped = 0
    for msg in box:
        message_id = (msg.get("Message-ID") or "").strip()
        sender = msg.get("From", "")
        subject = msg.get("Subject", "")
        date_raw = msg.get("Date", "")

        parsed = parsedate(date_raw)
        if parsed is None:
            skipped += 1
            continue
        received_at = datetime(*parsed[:6])

        body = extract_body(msg)
        if not body.strip():
            skipped += 1
            continue

        cur.execute(
            """
            INSERT INTO demandes
                (canal, external_id, received_at, sender, subject, body)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            ("email", message_id, received_at, sender, subject, body),
        )
        inserted += 1

    conn.commit()
    cur.close()
    conn.close()

    print(f"Inserted: {inserted}, skipped: {skipped}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python legacy_collect.py <path/to/file.mbox>")
        sys.exit(1)
    collect(sys.argv[1])
