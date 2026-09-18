import { Box } from "@mui/material";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import NavBar from "./components/NavBar";
import WelcomePage from "./pages/WelcomePage";
import DemoPage from "./pages/DemoPage";
import EmployeeFeedbackPage from "./pages/EmployeeFeedbackPage";
import EmployeeSkillsPage from "./pages/EmployeeSkillsPage";
import ChatbotPage from "./pages/ChatbotPage";

function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <Box component="main" sx={{ maxWidth: 1100, mx: "auto", px: 2, py: 4, width: "100%" }}>
        <Routes>
          <Route path="/" element={<WelcomePage />} />
          <Route path="/demo" element={<DemoPage />} />
          <Route path="/employee-feedback" element={<EmployeeFeedbackPage />} />
          <Route path="/employee-skills" element={<EmployeeSkillsPage />} />
          <Route path="/chatbot" element={<ChatbotPage />} />
        </Routes>
      </Box>
    </BrowserRouter>
  );
}

export default App;
