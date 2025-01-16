import axios from "axios";
import { useState } from "react";
import "../styles/uploadForm.css";

const UploadForm = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage(""); // Reset message on file change
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("user_id", "guest_user");

    setLoading(true);
    setMessage(""); // Clear previous messages

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/upload",
        formData
      );
      setMessage(`Upload successful: ${response.data.message}`);
    } catch (error) {
      setMessage(
        `Upload failed: ${error.response?.data?.error || error.message}`
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-form-container">
      <h2 className="upload-title">Upload a Document</h2>
      <div className="upload-form">
        <input
          type="file"
          onChange={handleFileChange}
          className="file-input"
          accept=".pdf"
        />
        <button
          className="upload-button"
          onClick={handleUpload}
          disabled={loading}
        >
          {loading ? <div className="loading-spinner"></div> : "Upload File"}
        </button>
      </div>
      {message && <p className="upload-message">{message}</p>}
    </div>
  );
};

export default UploadForm;
