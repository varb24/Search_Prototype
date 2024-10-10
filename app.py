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
    # Corrected Neo4j query with parameterized token
    just_search = '''
        WITH genai.vector.encode(
            $question,
            "OpenAI",
            { token: st.secrets['AI'],
              model: "text-embedding-3-small" }
        ) AS userEmbedding
        CALL db.index.vector.queryNodes('courseDescription', 10, userEmbedding)
        YIELD node, score
        RETURN node.title, node.description, node.course_id, score
    '''
    st.title("Search App")

    # Get the 'question' from the user
    question = st.text_input("Enter your question")

    if st.button("Submit"):
        if not question:
            st.error("Please enter a question.")
            return

        # Perform the query
        try:
            # Access Neo4j credentials from secrets
            neo4j_uri = st.secrets["NEO4J_URI"]
            neo4j_user = st.secrets["NEO4J_USER"]
            neo4j_password = st.secrets["NEO4J_PASSWORD"]

            # Access OpenAI token from secrets
            openai_token = st.secrets["OPENAI_TOKEN"]

            driver = get_neo4j_driver(neo4j_uri, neo4j_user, neo4j_password)

            # Prepare parameters
            data = {
                'question': question,
                'token': openai_token
            }

            # Your Neo4j query logic here
            with driver.session() as session:
                results = session.run(just_search, data)
                results = [record.data() for record in results]

            logging.info(results)

            # Display the results
            st.write("Results:")
            for result in results:
                st.write(f"**Title:** {result['node.title']}")
                st.write(f"**Description:** {result['node.description']}")
                st.write(f"**Course ID:** {result['node.course_id']}")
                st.write(f"**Score:** {result['score']}")
                st.write("---")
        except Exception as e:
            logging.error(f"Error performing query: {e}")
            st.error(f"An error occurred while performing the query: {e}")

if __name__ == "__main__":
    main()
