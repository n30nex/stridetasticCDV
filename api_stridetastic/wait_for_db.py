import os
import sys
import time

import psycopg2


def main() -> int:
    host = os.getenv("DB_HOST", "timescale_stridetastic")
    port = int(os.getenv("DB_PORT", "5432"))
    name = os.getenv("DB_NAME", "postgres")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "postgres")
    timeout = int(os.getenv("DB_WAIT_TIMEOUT", "60"))

    start = time.time()
    while True:
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                dbname=name,
                user=user,
                password=password,
                connect_timeout=3,
            )
            conn.close()
            print("Database is available.")
            return 0
        except psycopg2.OperationalError as exc:
            elapsed = time.time() - start
            if elapsed >= timeout:
                print(f"Timed out waiting for database after {timeout}s: {exc}", file=sys.stderr)
                return 1
            print("Waiting for database...", file=sys.stderr)
            time.sleep(2)


if __name__ == "__main__":
    raise SystemExit(main())
