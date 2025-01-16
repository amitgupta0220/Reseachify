/* eslint-disable react/prop-types */
import axios from "axios";
import { useState } from "react";

const ChatDialog = ({ file, onClose }) => {
  const [query, setQuery] = useState("");
  const [responses, setResponses] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleChat = async () => {
    if (!query) return;

    setLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:5000/retrieve", {
        query,
        user_id: file.userId,
        file_id: file.fileId,
      });
      setResponses((prev) => [
        ...prev,
        { type: "user", message: query },
        {
          type: "ai",
          message: response.data.results.map((r) => r.content).join("\n"),
        },
      ]);
      setQuery("");
    } catch (error) {
      setResponses((prev) => [
        ...prev,
        {
          type: "error",
          message: "An error occurred while retrieving results." + error,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-dialog fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div className="bg-white rounded shadow-lg p-4 max-w-lg w-full">
        <h2 className="text-xl font-bold mb-4">Chat with AI</h2>
        <div className="chat-messages overflow-y-auto h-64 border p-2 mb-4">
          {responses.map((res, index) => (
            <div
              key={index}
              className={`p-2 rounded ${
                res.type === "user"
                  ? "bg-blue-100 text-blue-800"
                  : res.type === "ai"
                  ? "bg-green-100 text-green-800"
                  : "bg-red-100 text-red-800"
              }`}
            >
              {res.message}
            </div>
          ))}
        </div>
        <div className="flex items-center mb-4">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type your query..."
            className="flex-grow border rounded p-2 mr-2"
          />
          <button
            onClick={handleChat}
            disabled={loading}
            className="bg-blue-500 text-white px-4 py-2 rounded"
          >
            {loading ? "Loading..." : "Send"}
          </button>
        </div>
        <button
          onClick={onClose}
          className="bg-red-500 text-white px-4 py-2 rounded"
        >
          Close
        </button>
      </div>
    </div>
  );
};

export default ChatDialog;
