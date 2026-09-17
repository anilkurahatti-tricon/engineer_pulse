import { useState } from "react";
import {
  Alert,
  Box,
  Button,
  LinearProgress,
  Paper,
  Rating,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import DeleteOutlinedIcon from "@mui/icons-material/DeleteOutlined";
import { useEmployeeFeedback } from "../business/useEmployeeFeedback";
import FeedbackRatingChart from "../components/FeedbackRatingChart";

export default function EmployeeFeedbackPage() {
  const { items, loading, error, createItem, deleteItem } = useEmployeeFeedback();
  const [employeeName, setEmployeeName] = useState("");
  const [feedbackText, setFeedbackText] = useState("");
  const [rating, setRating] = useState(5);

  const average =
    items.length === 0
      ? 0
      : items.reduce((sum, item) => sum + Number(item.rating || 0), 0) / items.length;

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!employeeName || !feedbackText) return;
    await createItem({
      employee_id: Math.floor(Math.random() * 1000),
      employee_name: employeeName,
      feedback_text: feedbackText,
      rating: Number(rating),
    });
    setEmployeeName("");
    setFeedbackText("");
    setRating(5);
  };

  return (
    <Stack spacing={3}>
      <Box>
        <Typography variant="h4" component="h1">
          Employee Feedback
        </Typography>
        <Typography color="text.secondary">
          {items.length} entries · average rating {average.toFixed(1)} / 5
        </Typography>
      </Box>

      <Paper component="form" onSubmit={handleSubmit} sx={{ p: 2 }}>
        <Stack direction={{ xs: "column", sm: "row" }} spacing={2} sx={{ alignItems: { sm: "center" } }}>
          <TextField
            label="Employee name"
            value={employeeName}
            onChange={(e) => setEmployeeName(e.target.value)}
            required
            fullWidth
          />
          <TextField
            label="Feedback"
            value={feedbackText}
            onChange={(e) => setFeedbackText(e.target.value)}
            required
            fullWidth
          />
          <Rating
            name="feedback-rating"
            value={Number(rating)}
            onChange={(_, value) => setRating(value || 1)}
          />
          <Button type="submit" sx={{ whiteSpace: "nowrap" }}>
            Add
          </Button>
        </Stack>
      </Paper>

      {loading && <LinearProgress />}
      {error && <Alert severity="error">{error}</Alert>}

      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: { xs: "1fr", md: "1fr 1.2fr" },
          gap: 2,
        }}
      >
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Rating distribution
          </Typography>
          <FeedbackRatingChart items={items} />
        </Paper>

        <Paper sx={{ overflow: "auto" }}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Employee</TableCell>
                <TableCell>Feedback</TableCell>
                <TableCell>Rating</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {items.map((item) => (
                <TableRow key={item.id}>
                  <TableCell>{item.employee_name}</TableCell>
                  <TableCell>{item.feedback_text}</TableCell>
                  <TableCell>
                    <Rating value={Number(item.rating)} readOnly size="small" />
                  </TableCell>
                  <TableCell align="right">
                    <Button
                      color="error"
                      variant="text"
                      startIcon={<DeleteOutlinedIcon />}
                      onClick={() => deleteItem(item.id)}
                    >
                      Delete
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      </Box>
    </Stack>
  );
}
