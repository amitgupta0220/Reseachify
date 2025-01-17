import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate(); // Hook to navigate programmatically

  const handleNavigation = () => {
    navigate("/upload"); // Navigate to the upload page
  };

  return (
    <div className="bg-gray-100 min-h-screen flex items-center justify-center">
      <div className="bg-white shadow-lg rounded-lg p-8 max-w-4xl w-full text-center">
        <h1 className="text-4xl font-extrabold text-blue-600 mb-4">
          Welcome to Researchify!
        </h1>
        <p className="text-gray-700 text-lg mb-6">
          Your one-stop platform for efficient document analysis and AI-powered
          insights. Upload your research papers, retrieve key summaries, and
          chat with our intelligent assistant to uncover valuable information
          seamlessly.
        </p>
        <div className="grid gap-6 md:grid-cols-2 text-left">
          <div className="p-4 bg-blue-50 rounded-lg">
            <h3 className="text-xl font-semibold text-blue-600">
              🔍 Document Upload
            </h3>
            <p className="text-gray-700">
              Upload your documents in seconds and let our AI process them for
              summaries, key insights, and seamless analysis.
            </p>
          </div>
          <div className="p-4 bg-blue-50 rounded-lg">
            <h3 className="text-xl font-semibold text-blue-600">
              📄 Intelligent Summaries
            </h3>
            <p className="text-gray-700">
              Get precise and clear summaries for text, tables, and images in
              your documents—saving you hours of manual work.
            </p>
          </div>
          <div className="p-4 bg-blue-50 rounded-lg">
            <h3 className="text-xl font-semibold text-blue-600">
              💬 AI Chat Assistant
            </h3>
            <p className="text-gray-700">
              Chat with our AI assistant for detailed analysis and answers to
              your research questions.
            </p>
          </div>
          <div className="p-4 bg-blue-50 rounded-lg">
            <h3 className="text-xl font-semibold text-blue-600">
              🔗 Easy Access
            </h3>
            <p className="text-gray-700">
              Access your documents and their insights anytime, with seamless
              navigation and secure storage.
            </p>
          </div>
        </div>
        <div className="mt-8">
          <button
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
            onClick={handleNavigation}
          >
            Get Started
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;
