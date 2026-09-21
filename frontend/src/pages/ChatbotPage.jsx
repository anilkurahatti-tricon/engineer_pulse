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

  const handleCancel = () => {
    setText("");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!text.trim()) return;
    const toSend = text.trim();
    setText("");
    await sendMessage(toSend);
  };

  return (
    <Stack spacing={3}>
      <Typography variant="h4" component="h1">
        Chatbot
      </Typography>

      <Paper
        sx={{
          minHeight: 320,
          maxHeight: 480,
          overflow: "auto",
          p: { xs: 2, sm: 3 },
          display: "flex",
          flexDirection: "column",
          gap: 1.5,
        }}
      >
        {messages.length === 0 && (
          <Typography color="text.secondary">Ask a question in plain text.</Typography>
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
                <Typography variant="body2" sx={{ whiteSpace: "pre-wrap" }}>
                  {message.message}
                </Typography>
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

      <Paper component="form" onSubmit={handleSubmit} sx={{ p: { xs: 2, sm: 3 } }}>
        <Stack spacing={2}>
          <TextField
            label="Message"
            value={text}
            onChange={(e) => setText(e.target.value)}
            fullWidth
            multiline
            minRows={3}
            placeholder="Write your question in plain text..."
          />
          <Stack direction="row" spacing={1} sx={{ justifyContent: "flex-end" }}>
            <Button type="button" variant="outlined" onClick={handleCancel} disabled={loading}>
              Cancel
            </Button>
            <Button type="submit" endIcon={<SendIcon />} disabled={loading || !text.trim()}>
              Submit
            </Button>
          </Stack>
        </Stack>
      </Paper>
    </Stack>
  );
}
