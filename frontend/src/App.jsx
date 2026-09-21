import { Box } from "@mui/material";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import NavBar from "./components/NavBar";
import Footer from "./components/Footer";
import WelcomePage from "./pages/WelcomePage";
import DemoPage from "./pages/DemoPage";
import EmployeeFeedbackPage from "./pages/EmployeeFeedbackPage";
import EmployeeSkillsPage from "./pages/EmployeeSkillsPage";
import ChatbotPage from "./pages/ChatbotPage";

function App() {
  return (
    <BrowserRouter>
      <Box sx={{ minHeight: "100svh", display: "flex", flexDirection: "column" }}>
        <NavBar />
        <Box component="main" sx={{ flex: 1, maxWidth: 1100, mx: "auto", px: 2, py: 4, width: "100%" }}>
          <Routes>
            <Route path="/" element={<WelcomePage />} />
            <Route path="/employee-feedback" element={<EmployeeFeedbackPage />} />
            <Route path="/employee-skills" element={<EmployeeSkillsPage />} />
            <Route path="/chatbot" element={<ChatbotPage />} />
            <Route path="/demo" element={<DemoPage />} />
          </Routes>
        </Box>
        <Footer />
      </Box>
    </BrowserRouter>
  );
}

export default App;
