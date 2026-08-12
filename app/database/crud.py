# from app.database.db import get_connection

# def insert_complaint(data: dict):

#     conn = get_connection()
#     cursor = conn.cursor()

#     query = """
#     INSERT INTO complaints
#     (complaint_text, is_junk, drug_type, crime_type, city, location_detail)
#     VALUES (%s, %s, %s, %s, %s, %s)
#     """

#     values = (
#         data.get("complaint_text"),
#         data.get("is_junk"),
#         data.get("drug_type"),
#         data.get("crime_type"),
#         data.get("city"),
#         data.get("location_detail")
#     )

#     cursor.execute(query, values)
#     conn.commit()

#     cursor.close()
#     conn.close()

from app.database.db import get_connection

def insert_complaint(data: dict):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO complaints
    (complaint_text, is_junk, drug_type, crime_type, address, city, location_detail)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        data.get("complaint_text"),
        data.get("is_junk"),
        data.get("drug_type"),
        data.get("crime_type"),
        data.get("address"),
        data.get("city"),
        data.get("location_detail")
    )

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()