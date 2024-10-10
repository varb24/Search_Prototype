import streamlit as st
import logging

# Import your neo4j client and any other necessary modules
# from your_project import neo4j_client, just_search

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

    # Optional: Get the ID from the user
    id = st.text_input("Enter ID", value='')

    # Get the 'question' from the user
    question = st.text_input("Enter your question")

    if st.button("Submit"):
        if not question:
            st.error("Please enter a question.")
            return

        data = {'parameters': question}

        # Ensure 'parameters' is in data
        if 'parameters' not in data:
            st.error("Missing 'parameters' in data.")
            return

        # Perform the query
        try:
            results = neo4j_client.query(just_search, data['parameters'])
            logging.info(results)

            # Display the results
            st.write("Results:")
            st.write(results)
        except Exception as e:
            logging.error(f"Error performing query: {e}")
            st.error("An error occurred while performing the query.")

if __name__ == "__main__":
    main()
