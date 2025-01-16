import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Upload from "./pages/uploadPage";
import ViewDocuments from "./pages/ViewDocuments";

const App = () => {
  return (
    <Router>
      <Header />
      <main className="p-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/documents" element={<ViewDocuments />} />
        </Routes>
      </main>
      <Footer />
    </Router>
  );
};

export default App;
