import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Upload from "./pages/uploadPage";
import ViewDocuments from "./pages/ViewDocuments";
import TabBar from "./components/TabBar";

const App = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <Router>
        <TabBar />
        <main className="flex-1 p-4">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/documents" element={<ViewDocuments />} />
          </Routes>
        </main>
        <Footer />
      </Router>
    </div>
  );
};

export default App;
