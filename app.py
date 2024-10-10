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
    just_search = '''
        WITH genai.vector.encode(
            $question,
            "OpenAI",
            { token: "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",
        model:"text-embedding-3-small"}) AS userEmbedding
        CALL db.index.vector.queryNodes('courseDescription', 10, userEmbedding)
        YIELD node, score
        RETURN node.title, node.description,node.course_id, score
        '''
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
                results = session.run(just_search, data)
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
