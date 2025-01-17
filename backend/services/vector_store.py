import uuid
from langchain_chroma import Chroma
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
import shutil

# Load environment variables from .env file
load_dotenv()

# Initialize the vector store and in-memory document store
vectorstore = Chroma(
    collection_name="multi_modal_rag",
    embedding_function=OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY")),
    persist_directory="./vector_store"
)
docstore = InMemoryStore()


def add_to_vectorstore(texts, text_summaries, tables, table_summaries, images, image_summaries, metadata):
    """
    Adds all data (text, tables, images) and their summaries to the vector store with metadata.
    """
    user_id = metadata.get("user_id")
    file_id = metadata.get("file_id")

    if not user_id or not file_id:
        raise ValueError("User ID and File ID must be provided in metadata.")

    try:
        # Add text summaries
        for text, summary in zip(texts, text_summaries):
            vectorstore.add_documents([
                Document(
                    page_content=str(summary),
                    metadata={
                        "type": "text",
                        "user_id": user_id,
                        "file_id": file_id
                    }
                )
            ])
            docstore.mset([(str(uuid.uuid4()), text)])

        # Add table summaries
        for table, summary in zip(tables, table_summaries):
            vectorstore.add_documents([
                Document(
                    page_content=str(summary),
                    metadata={
                        "type": "table",
                        "user_id": user_id,
                        "file_id": file_id
                    }
                )
            ])
            docstore.mset([(str(uuid.uuid4()), table)])

        # Add image summaries
        for image, summary in zip(images, image_summaries):
            vectorstore.add_documents([
                Document(
                    page_content=str(summary),
                    metadata={
                        "type": "image",
                        "user_id": user_id,
                        "file_id": file_id
                    }
                )
            ])
            docstore.mset([(str(uuid.uuid4()), image)])

    except Exception as e:
        raise RuntimeError(f"Error adding data to vector store: {str(e)}")


def retrieve_documents(query, user_id, file_id, top_k=5):
    """
    Retrieves relevant documents from the vector store based on a query, user ID, and file ID.
    """
    try:
        docs = vectorstore.similarity_search(query, k=top_k)
        filtered_docs = [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in docs
            if doc.metadata.get("user_id") == user_id and doc.metadata.get("file_id") == file_id
        ]
        return filtered_docs
    except Exception as e:
        raise RuntimeError(f"Error retrieving documents: {str(e)}")


def list_documents(user_id):
    """
    Lists all documents for a given user ID from the vector store.
    """
    try:
        # Perform a broad similarity search with a dummy query (e.g., empty string or generic term)
        dummy_query = "list_documents_placeholder"
        docs = vectorstore.similarity_search(dummy_query, k=1000)  # Adjust k as needed for the dataset size
        
        # Filter results by user_id and organize by file_id
        unique_files = {}
        for doc in docs:
            metadata = doc.metadata
            if metadata.get("user_id") == user_id:
                file_id = metadata.get("file_id")
                if file_id not in unique_files:
                    unique_files[file_id] = {"file_id": file_id, "types": set()}
                unique_files[file_id]["types"].add(metadata.get("type"))

        # Convert sets to lists for frontend compatibility
        return [
            {"file_id": file_id, "types": list(info["types"])}
            for file_id, info in unique_files.items()
        ]
    except Exception as e:
        raise RuntimeError(f"Error listing documents: {str(e)}")

def delete_file(file_id, user_id=None):
    """
    Deletes all documents associated with a specific file_id (and optionally a user_id) from the vector store.
    """
    try:
        # Construct the filter based on file_id and optionally user_id
        filter_criteria = {"file_id": file_id}
        if user_id:
            filter_criteria["user_id"] = user_id

        # Use the delete method with the filter
        vectorstore._collection.delete(where=filter_criteria)
        # Delete local folder
        data_dir = "./data"
        file_dir = os.path.join(data_dir, file_id)
        if os.path.exists(file_dir):
            shutil.rmtree(file_dir)  # Delete the entire directory
            return {"message": f"Documents and files with file_id '{file_id}' deleted successfully."}
        else:
            return {"message": f"Documents deleted successfully, but no local files found for file_id '{file_id}'."}
    except Exception as e:
        raise RuntimeError(f"Error deleting file: {str(e)}")
