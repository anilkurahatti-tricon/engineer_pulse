import { useState } from "react";
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Paper,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import { useChatbot } from "../business/useChatbot";

export default function ChatbotPage() {
  const { messages, loading, error, sendMessage } = useChatbot();
  const [text, setText] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!text) return;
    const toSend = text;
    setText("");
    await sendMessage(toSend);
  };

  return (
    <Stack spacing={2}>
      <Typography variant="h4" component="h1">
        Chatbot
      </Typography>

      <Paper
        sx={{
          minHeight: 280,
          maxHeight: 480,
          overflow: "auto",
          p: 2,
          display: "flex",
          flexDirection: "column",
          gap: 1.5,
        }}
      >
        {messages.length === 0 && (
          <Typography color="text.secondary">
            Ask a question about the team, skills, or feedback.
          </Typography>
        )}
        {messages.map((message, idx) => {
          const isUser = message.sender === "user";
          return (
            <Box key={idx} sx={{ display: "flex", justifyContent: isUser ? "flex-end" : "flex-start" }}>
              <Paper
                elevation={0}
                sx={{
                  px: 1.5,
                  py: 1,
                  maxWidth: "80%",
                  bgcolor: isUser ? "primary.main" : "background.default",
                  color: isUser ? "primary.contrastText" : "text.primary",
                }}
              >
                <Typography variant="caption" sx={{ display: "block", opacity: 0.8 }}>
                  {isUser ? "You" : "Bot"}
                </Typography>
                <Typography variant="body2">{message.message}</Typography>
              </Paper>
            </Box>
          );
        })}
      </Paper>

      {loading && (
        <Stack direction="row" spacing={1} sx={{ alignItems: "center" }}>
          <CircularProgress size={18} />
          <Typography variant="body2">Thinking...</Typography>
        </Stack>
      )}
      {error && <Alert severity="error">{error}</Alert>}

      <Stack component="form" onSubmit={handleSubmit} direction="row" spacing={1}>
        <TextField
          fullWidth
          placeholder="Ask the chatbot..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <Button type="submit" endIcon={<SendIcon />} disabled={loading}>
          Send
        </Button>
      </Stack>
    </Stack>
  );
}
