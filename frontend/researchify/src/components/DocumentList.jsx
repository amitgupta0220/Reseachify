import axios from "axios";
import { useState, useEffect } from "react";
import "../styles/documentList.css";
import ChatDialog from "./ChatDialog"; // Import ChatDialog Component

const DocumentsList = () => {
  const [documents, setDocuments] = useState([]);
  const [userId] = useState("guest_user"); // Hardcoded for now, you can dynamically fetch or generate this.
  const [selectedFile, setSelectedFile] = useState(null); // For Chat Modal
  const [isChatOpen, setIsChatOpen] = useState(false); // Modal visibility

  // Fetch documents
  const fetchDocuments = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/documents", {
        params: { user_id: userId },
      });
      setDocuments(response.data.documents);
    } catch (error) {
      console.error("Error fetching documents:", error.message);
    }
  };

  // Delete a document
  const handleDelete = async (fileId) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this document?"
    );
    if (!confirmDelete) return;

    try {
      const response = await axios.delete("http://127.0.0.1:5000/delete_file", {
        data: { file_id: fileId, filename: "uploaded.pdf" },
      });
      alert(response.data.message);
      // Refresh the document list
      fetchDocuments();
    } catch (error) {
      alert("Failed to delete file: " + error.message);
    }
  };

  // Download a document
  const handleDownload = (fileId, fileName) => {
    const url = `http://127.0.0.1:5000/data/${fileId}/${fileName}`;
    window.open(url, "_blank"); // Opens the file in a new tab for download
  };

  // Open Chat Modal
  const handleChat = (fileId) => {
    setSelectedFile({ fileId, userId });
    setIsChatOpen(true);
  };

  useEffect(() => {
    fetchDocuments();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="documents-list">
      <h2 className="text-xl font-bold mb-4">Your Documents</h2>
      {documents.length === 0 ? (
        <p>No documents found.</p>
      ) : (
        <ul>
          {documents.map((doc) => (
            <li key={doc.file_id} className="flex items-center mb-4">
              <span className="flex-grow">{doc.file_id}</span>
              <button
                onClick={() => handleDownload(doc.file_id, "uploaded.pdf")}
                className="bg-blue-500 text-white px-3 py-1 rounded mr-2"
              >
                Download
              </button>
              <button
                onClick={() => handleDelete(doc.file_id)}
                className="bg-red-500 text-white px-3 py-1 rounded mr-2"
              >
                Delete
              </button>
              <button
                onClick={() => handleChat(doc.file_id)}
                className="bg-green-500 text-white px-3 py-1 rounded"
              >
                Chat
              </button>
            </li>
          ))}
        </ul>
      )}
      {isChatOpen && (
        <ChatDialog file={selectedFile} onClose={() => setIsChatOpen(false)} />
      )}
    </div>
  );
};

export default DocumentsList;
