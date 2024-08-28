import streamlit as st
import pandas as pd
from query_executor import create_connection, execute_sql_query, get_query_from_openai

# Database connection details
host = 'localhost'
user = 'root'
password = 'Sweety@17'
database = 'openai'

def main():
    st.title("SQL Query Generator")

    api_key = st.text_input("Enter OpenAI API Key")
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file and api_key:
        # Load data from file
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            data = pd.read_excel(uploaded_file)

        # Display the data
        st.write("Data Preview:", data)

        conn = create_connection(host, user, password, database)

        if conn:
            # Get list of tables in the database
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            table_names = [table[0] for table in tables]

            # Allow the user to select a table name
            selected_table_name = st.selectbox("Select a table name", table_names, index=0)

            text_input = st.text_area("Enter your query")
            submit = st.button("Generate SQL query")

            if submit:
                with st.spinner("Generating SQL Query..."):
                    template = f"""
                    Create a SQL query snippet using the below text:

                        {text_input}

                    I just want a SQL Query.
                    """
                    formatted_template = template
                    sql_query = get_query_from_openai(api_key, formatted_template)

                    # Replace 'your_table_name' with the selected table name
                    sql_query = sql_query.replace("your_table_name", selected_table_name)
                    st.write("Generated SQL Query:", sql_query)

                    # Execute the SQL query and get results
                    result = execute_sql_query(sql_query, conn)
                    st.write("Query Result:", result)

if __name__ == "__main__":
    main()