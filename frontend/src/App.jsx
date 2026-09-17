import { BrowserRouter, Route, Routes } from "react-router-dom";
import NavBar from "./components/NavBar";
import WelcomePage from "./pages/WelcomePage";
import DemoPage from "./pages/DemoPage";
import EmployeeFeedbackPage from "./pages/EmployeeFeedbackPage";
import EmployeeSkillsPage from "./pages/EmployeeSkillsPage";
import ChatbotPage from "./pages/ChatbotPage";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <main className="app-content">
        <Routes>
          <Route path="/" element={<WelcomePage />} />
          <Route path="/demo" element={<DemoPage />} />
          <Route path="/employee-feedback" element={<EmployeeFeedbackPage />} />
          <Route path="/employee-skills" element={<EmployeeSkillsPage />} />
          <Route path="/chatbot" element={<ChatbotPage />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;
