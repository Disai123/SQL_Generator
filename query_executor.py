import mysql.connector

def create_connection(host, user, password, database):
    """Create a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def execute_sql_query(query, conn):
    """Execute the SQL query and return results."""
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        return str(err)
    finally:
        cursor.close()
        conn.close()

def get_query_from_openai(api_key, text_input):
    """Generate a SQL query from OpenAI based on the provided input text."""
    import openai

    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates SQL queries."},
            {"role": "user", "content": text_input}
        ],
        max_tokens=150
    )
    
    sql_query = response.choices[0].message['content'].strip()

    # Clean the response to remove any markdown formatting
    cleaned_response = sql_query.replace('```sql', '').replace('```', '').strip()
    return cleaned_response
