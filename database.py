import psycopg2
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def connect_to_retool():
    return psycopg2.connect(
        host=os.getenv("host_1"),
        database=os.getenv("database"),
        user=os.getenv("user"),
        password=os.getenv("password_1"),
        sslmode=os.getenv("sslmode", "require")
    )

def get_candidates_db():
    try:
        conn = connect_to_retool()
        # print("=============")
        # print(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bench;")
        candidates = cursor.fetchall()
        print(candidates)
        dict_candidates=[]
        for candidate in candidates:
            values={
                "vamid": candidate[1] if len(candidate) > 1 else None,
                "name": candidate[2] if len(candidate) > 2 else None,
                "joining_date": candidate[3] if len(candidate) > 3 else None,
                "grade": candidate[4] if len(candidate) > 4 else None,
                "tsc": candidate[5] if len(candidate) > 5 else None,
                "account": candidate[6] if len(candidate) > 6 else None,
                "project": candidate[7] if len(candidate) > 7 else None,
                "allocation_status": candidate[8] if len(candidate) > 8 else None,
                "allocation_start_date": candidate[9] if len(candidate) > 9 else None,
                "allocation_end_date": candidate[10] if len(candidate) > 10 else None,
                "first_level_manager": candidate[11] if len(candidate) > 11 else None,
                "designation": candidate[12] if len(candidate) > 12 else None,
                "email": candidate[13] if len(candidate) > 13 else None,
                "sub_dept": candidate[14] if len(candidate) > 14 else None,
                "relieving_date": candidate[15] if len(candidate) > 15 else None,
                "resigned_on": candidate[16] if len(candidate) > 16 else None,
                "resignation_status": candidate[17] if len(candidate) > 17 else None,
                "second_level_manager": candidate[18] if len(candidate) > 18 else None,
                "current_skill": candidate[19] if len(candidate) > 19 else None,
                "primary_skill": candidate[20] if len(candidate) > 20 else None,
                "vam_exp": candidate[21] if len(candidate) > 21 else None,
                "total_exp": candidate[22] if len(candidate) > 22 else None,
                "account_summary": candidate[23] if len(candidate) > 23 else None,
                "resourcing_unit": candidate[24] if len(candidate) > 24 else None,
                "workspace": candidate[25] if len(candidate) > 25 else None,
            }
            dict_candidates.append(values)
        cursor.close()
        conn.close()
        return dict_candidates
    except Exception as e:
        print(f"Error retrieving candidates: {e}")
        if 'conn' in locals():
            conn.close()
        return {}
    

def list_retool_tables():
    try:
        conn = connect_to_retool()
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        print(tables)
        return tables
    except Exception as e:
        print(f"Error listing tables: {e}")
        if 'conn' in locals():
            if 'cursor' in locals():
                cursor.close()
            conn.close()
        return []
    
def get_dashboard():
    conn = None
    try:
        conn = connect_to_retool()
        cursor = conn.cursor()

        # Bench count
        cursor.execute("SELECT COUNT(name) FROM bench;")
        bench_count = cursor.fetchone()[0]
        # print("===")
        # print(f"Bench count: {bench_count}")

        # Distinct RRF count
        cursor.execute("SELECT COUNT(rrf_id) FROM rrf;")
        rrf_count = cursor.fetchone()[0]
        # print(f"RRF count: {rrf_count}")

        return {
            "bench_count": bench_count,
            "rrf_count": rrf_count
        }

    except Exception as e:
        print(f"Error retrieving dashboard data: {e}")
        return {
            "bench_count": 0,
            "rrf_count": 0,
            "error": str(e)
        }

    finally:
        if conn:
            conn.close()

def get_rrf_details():
    conn = None
    try:
        conn = connect_to_retool()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM rrf;")
        rrf_details = cursor.fetchall()

        return [
            {
                "account": detail[1] if len(detail) > 1 else None,
                "rrf_id": detail[2] if len(detail) > 2 else None,
                "created_on": detail[3] if len(detail) > 3 else None,
                "required_by": detail[4] if len(detail) > 4 else None,
                "pos_title": detail[5] if len(detail) > 5 else None,
                "role": detail[6] if len(detail) > 6 else None,
                "status": detail[7] if len(detail) > 7 else None,
                "tag_comments": detail[8] if len(detail) > 8 else None,
                "type": detail[9] if len(detail) > 9 else None,
                "project_name": detail[10] if len(detail) > 10 else None
            }
            for detail in rrf_details
        ]

    except Exception as e:
        print(f"Error retrieving RRF details: {e}")
        return []

    finally:
        if conn:
            conn.close()


def update_pos_id(id):
    try:
        conn = connect_to_retool()
        cursor = conn.cursor()
        cursor.execute("UPDATE rrf SET status = 'closed' WHERE rrf_id = %s;", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Position ID updated for RRF ID: {id}")
    except Exception as e:
        print(f"Error updating position ID: {e}")
        if 'conn' in locals():
            conn.rollback()
            cursor.close()
            conn.close()

if __name__ == "__main__":
    # Only run this when the script is executed directly, not when imported
    get_candidates_db()