# import os
# import uuid
# from flask import Flask, request, jsonify, send_from_directory
# from services.pdf_processing import process_pdf
# from services.summarization import summarize_text_and_tables, summarize_images
# from services.vector_store import add_to_vectorstore, retrieve_documents

# # Initialize Flask app and set data directory
# app = Flask(__name__)
# DATA_DIR = "./data"
# os.makedirs(DATA_DIR, exist_ok=True)

# @app.route('/upload', methods=['POST'])
# def upload_pdf():
#     """
#     Endpoint to upload a PDF, process it, generate summaries, and store in the vector database.
#     """
#     if 'file' not in request.files:
#         return jsonify({"error": "No file provided"}), 400

#     # Save uploaded file and assign a unique document ID
#     pdf_file = request.files['file']
#     doc_id = str(uuid.uuid4())  # Generate a unique document ID
#     output_dir = os.path.join(DATA_DIR, doc_id)

#     os.makedirs(output_dir, exist_ok=True)
#     file_path = os.path.join(output_dir, "uploaded.pdf")
#     pdf_file.save(file_path)

#     try:
#         # Process the PDF to extract text, tables, and images
#         texts, tables, images = process_pdf(file_path, output_dir)

#         # Generate summaries for text, tables, and images
#         text_summaries, table_summaries = summarize_text_and_tables(texts, tables)
#         image_summaries = summarize_images(images)

#         # Add data and summaries to the vector store
#         add_to_vectorstore(
#             texts, text_summaries, 
#             tables, table_summaries, 
#             images, image_summaries
#         )

#         return jsonify({
#             "message": "Document processed and stored successfully.",
#             "doc_id": doc_id
#         }), 200
#     except Exception as e:
#         return jsonify({"error": f"Error processing PDF: {str(e)}"}), 500

# @app.route('/retrieve', methods=['POST'])
# def retrieve():
#     """
#     Endpoint to retrieve documents based on a query.
#     """
#     query = request.json.get("query")
#     if not query:
#         return jsonify({"error": "Query not provided"}), 400

#     try:
#         results = retrieve_documents(query)
#         return jsonify({"results": results}), 200
#     except Exception as e:
#         return jsonify({"error": f"Error retrieving documents: {str(e)}"}), 500

# if __name__ == '__main__':
#     app.run(debug=True)

import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from services.pdf_processing import process_pdf
from services.summarization import summarize_text_and_tables, summarize_images
from services.vector_store import add_to_vectorstore, retrieve_documents, list_documents, delete_file

app = Flask(__name__)
DATA_DIR = "./data"
os.makedirs(DATA_DIR, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    pdf_file = request.files['file']
    user_id = request.form.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    file_id = str(uuid.uuid4())  # Generate a unique document ID
    output_dir = os.path.join(DATA_DIR, file_id)

    # Save the uploaded PDF
    file_path = os.path.join(output_dir, "uploaded.pdf")
    os.makedirs(output_dir, exist_ok=True)
    pdf_file.save(file_path)

    try:
        # Process the PDF
        texts, tables, images = process_pdf(file_path, output_dir)

        # Generate summaries
        text_summaries, table_summaries = summarize_text_and_tables(texts, tables, user_id, file_id)
        image_summaries = summarize_images(images, user_id, file_id)

        # Add to vector store with metadata
        add_to_vectorstore(
            texts=texts, 
            text_summaries=text_summaries, 
            tables=tables, 
            table_summaries=table_summaries, 
            images=images, 
            image_summaries=image_summaries, 
            metadata={"user_id": user_id, "file_id": file_id}
        )

        return jsonify({"message": "Document processed and stored successfully.", "file_id": file_id}), 200
    except Exception as e:
        return jsonify({"error": f"Error processing PDF: {str(e)}"}), 500

@app.route('/documents', methods=['GET'])
def list_user_documents():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        documents = list_documents(user_id)
        return jsonify({"documents": documents}), 200
    except Exception as e:
        return jsonify({"error": f"Error fetching documents: {str(e)}"}), 500

@app.route('/retrieve', methods=['POST'])
def retrieve():
    query = request.json.get("query")
    user_id = request.json.get("user_id")
    file_id = request.json.get("file_id")

    if not query or not user_id or not file_id:
        return jsonify({"error": "Query, User ID, and File ID are required"}), 400

    try:
        results = retrieve_documents(query, user_id, file_id)
        return jsonify({"results": results}), 200
    except Exception as e:
        return jsonify({"error": f"Error retrieving documents: {str(e)}"}), 500

@app.route('/data/<file_id>/<filename>', methods=['GET'])
def download_file(file_id, filename):
    return send_from_directory(os.path.join(DATA_DIR, file_id), filename)

@app.route('/delete_file', methods=['DELETE'])
def delete_file_endpoint():
    data = request.json
    file_id = data.get("file_id")
    user_id = data.get("user_id")  # Optional

    if not file_id:
        return jsonify({"error": "File ID is required"}), 400

    try:
        result = delete_file(file_id, user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"Error deleting file: {str(e)}"}), 500



if __name__ == '__main__':
    app.run(debug=True)
