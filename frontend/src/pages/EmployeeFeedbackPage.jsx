import { useState } from "react";
import {
  Alert,
  Box,
  Button,
  IconButton,
  LinearProgress,
  Paper,
  Rating,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import DeleteOutlinedIcon from "@mui/icons-material/DeleteOutlined";
import { useEmployeeFeedback } from "../business/useEmployeeFeedback";
import FeedbackRatingChart from "../components/FeedbackRatingChart";
import { formatSystemDate } from "../utils/formatSystemDate";
import ConfirmDialog from "../components/ConfirmDialog";

const EMPTY_FORM = {
  employeeId: "",
  employeeName: "",
  feedbackText: "",
  rating: 5,
};

export default function EmployeeFeedbackPage() {
  const { items, loading, submitting, error, createItem, deleteItem } = useEmployeeFeedback();
  const [form, setForm] = useState(EMPTY_FORM);
  const [feedbackDate, setFeedbackDate] = useState(() => new Date());
  const [success, setSuccess] = useState("");
  const [confirm, setConfirm] = useState(null);

  const isFormDirty =
    Boolean(form.employeeId) || Boolean(form.employeeName.trim()) || Boolean(form.feedbackText.trim());

  const average =
    items.length === 0
      ? 0
      : items.reduce((sum, item) => sum + Number(item.rating || 0), 0) / items.length;

  const resetForm = () => {
    setForm(EMPTY_FORM);
    setFeedbackDate(new Date());
    setSuccess("");
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!form.employeeId || !form.employeeName.trim() || !form.feedbackText.trim()) return;
    setConfirm({ type: "submit" });
  };

  const handleCancelClick = () => {
    if (!isFormDirty) {
      resetForm();
      return;
    }
    setConfirm({ type: "cancel" });
  };

  const handleConfirm = async () => {
    if (!confirm) return;
    if (confirm.type === "cancel") {
      resetForm();
      setConfirm(null);
      return;
    }
    if (confirm.type === "delete") {
      await deleteItem(confirm.item.id);
      setConfirm(null);
      return;
    }
    setSuccess("");
    try {
      await createItem({
        employee_id: Number(form.employeeId),
        employee_name: form.employeeName.trim(),
        feedback_text: form.feedbackText.trim(),
        rating: Number(form.rating),
      });
      resetForm();
      setSuccess("Feedback submitted.");
      setConfirm(null);
    } catch {
      setConfirm(null);
    }
  };

  return (
    <Stack spacing={3}>
      <Typography variant="h4" component="h1">
        Feedback
      </Typography>

      <Paper component="form" onSubmit={handleSubmit} sx={{ p: { xs: 2, sm: 3 } }}>
        <Stack spacing={2.5}>
          <Stack direction={{ xs: "column", sm: "row" }} spacing={2}>
            <TextField
              label="Employee ID"
              type="number"
              value={form.employeeId}
              onChange={(e) => setForm((prev) => ({ ...prev, employeeId: e.target.value }))}
              required
              fullWidth
            />
            <TextField
              label="Employee name"
              value={form.employeeName}
              onChange={(e) => setForm((prev) => ({ ...prev, employeeName: e.target.value }))}
              required
              fullWidth
            />
          </Stack>

          <TextField
            label="Feedback"
            value={form.feedbackText}
            onChange={(e) => setForm((prev) => ({ ...prev, feedbackText: e.target.value }))}
            required
            fullWidth
            multiline
            minRows={6}
            placeholder="Write feedback in plain text..."
          />

          <TextField
            label="Feedback date"
            value={formatSystemDate(feedbackDate)}
            fullWidth
            disabled
            helperText="Filled automatically from this computer."
          />

          <Stack
            direction={{ xs: "column", sm: "row" }}
            spacing={2}
            sx={{ alignItems: { sm: "center" }, justifyContent: "space-between" }}
          >
            <Box>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                Rating
              </Typography>
              <Rating
                name="feedback-rating"
                value={Number(form.rating)}
                onChange={(_, value) => setForm((prev) => ({ ...prev, rating: value || 1 }))}
              />
            </Box>
            <Stack direction="row" spacing={1} sx={{ justifyContent: "flex-end" }}>
              <Button type="button" variant="outlined" onClick={handleCancelClick} disabled={submitting}>
                Cancel
              </Button>
              <Button type="submit" disabled={submitting}>
                {submitting ? "Submitting..." : "Submit"}
              </Button>
            </Stack>
          </Stack>
        </Stack>
      </Paper>

      {loading && <LinearProgress />}
      {error && <Alert severity="error">{error}</Alert>}
      {success && <Alert severity="success">{success}</Alert>}

      <Paper sx={{ p: { xs: 2, sm: 3 } }}>
        <Typography variant="h6" gutterBottom>
          Rating distribution
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          {items.length} entries · average {average.toFixed(1)} / 5
        </Typography>
        <FeedbackRatingChart items={items} height={240} />
      </Paper>

      <Paper>
        <Box sx={{ px: { xs: 2, sm: 3 }, pt: { xs: 2, sm: 3 }, pb: 1 }}>
          <Typography variant="h6">Submitted feedback</Typography>
        </Box>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Employee</TableCell>
                <TableCell>Feedback</TableCell>
                <TableCell>Rating</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {items.length === 0 && (
                <TableRow>
                  <TableCell colSpan={4}>
                    <Typography color="text.secondary">No feedback yet.</Typography>
                  </TableCell>
                </TableRow>
              )}
              {items.map((item) => (
                <TableRow key={item.id} hover>
                  <TableCell>
                    <Typography variant="body2">{item.employee_name}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      ID {item.employee_id}
                    </Typography>
                  </TableCell>
                  <TableCell sx={{ whiteSpace: "pre-wrap", wordBreak: "break-word" }}>
                    {item.feedback_text}
                  </TableCell>
                  <TableCell>
                    <Rating value={Number(item.rating)} readOnly size="small" />
                  </TableCell>
                  <TableCell align="right">
                    <IconButton
                      aria-label={`Delete feedback for ${item.employee_name}`}
                      color="error"
                      onClick={() => setConfirm({ type: "delete", item })}
                    >
                      <DeleteOutlinedIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      <ConfirmDialog
        open={Boolean(confirm)}
        title={
          confirm?.type === "delete"
            ? "Delete this feedback?"
            : confirm?.type === "cancel"
              ? "Clear this form?"
              : "Submit this feedback?"
        }
        message={
          confirm?.type === "delete"
            ? `Feedback for ${confirm.item?.employee_name || "this employee"} will be removed.`
            : confirm?.type === "cancel"
              ? "Unsaved text will be lost."
              : "This will send the feedback to the server."
        }
        confirmLabel={
          confirm?.type === "delete" ? "Delete" : confirm?.type === "cancel" ? "Clear" : "Submit"
        }
        confirmColor={confirm?.type === "submit" ? "primary" : "error"}
        busy={submitting}
        onCancel={() => setConfirm(null)}
        onConfirm={handleConfirm}
      />
    </Stack>
  );
}
