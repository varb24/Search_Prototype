import streamlit as st
import logging
from neo4j import GraphDatabase

# Set up logging
logging.basicConfig(level=logging.INFO)

# Function to create a Neo4j driver instance
def get_neo4j_driver(uri, user, password):
    return GraphDatabase.driver(uri, auth=(user, password))

# Main function
def main():
    st.title("Search App")

    # Get the 'question' from the user
    question = st.text_input("Enter your question")

    if st.button("Submit"):
        if not question:
            st.error("Please enter a question.")
            return

        data = {'parameters': question}

        # Perform the query
        try:
            # Access Neo4j credentials from secrets
            neo4j_uri = st.secrets["NEO4J_URI"]
            neo4j_user = st.secrets["NEO4J_USER"]
            neo4j_password = st.secrets["NEO4J_PASSWORD"]

            driver = get_neo4j_driver(neo4j_uri, neo4j_user, neo4j_password)

            # Your Neo4j query logic here
            with driver.session() as session:
                results = session.run("YOUR CYPHER QUERY HERE", data)
                results = [record.data() for record in results]

            logging.info(results)

            # Display the results
            st.write("Results:")
            st.write(results)
        except Exception as e:
            logging.error(f"Error performing query: {e}")
            st.error("An error occurred while performing the query.")

if __name__ == "__main__":
    main()
