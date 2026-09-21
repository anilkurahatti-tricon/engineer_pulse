import { useState } from "react";
import {
  Alert,
  Box,
  Button,
  IconButton,
  LinearProgress,
  Paper,
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
import { useDemoItems } from "../business/useDemoItems";
import { formatSystemDate } from "../utils/formatSystemDate";
import ConfirmDialog from "../components/ConfirmDialog";

const EMPTY_FORM = {
  name: "",
  description: "",
};

export default function DemoPage() {
  const { items, loading, submitting, error, createItem, deleteItem } = useDemoItems();
  const [form, setForm] = useState(EMPTY_FORM);
  const [recordedAt, setRecordedAt] = useState(() => new Date());
  const [success, setSuccess] = useState("");
  const [confirm, setConfirm] = useState(null);

  const isFormDirty = Boolean(form.name.trim()) || Boolean(form.description.trim());

  const resetForm = () => {
    setForm(EMPTY_FORM);
    setRecordedAt(new Date());
    setSuccess("");
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!form.name.trim() || !form.description.trim()) return;
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
        name: form.name.trim(),
        description: form.description.trim(),
      });
      resetForm();
      setSuccess("Demo item submitted.");
      setConfirm(null);
    } catch {
      setConfirm(null);
    }
  };

  return (
    <Stack spacing={3}>
      <Typography variant="h4" component="h1">
        Demo
      </Typography>

      <Paper component="form" onSubmit={handleSubmit} sx={{ p: { xs: 2, sm: 3 } }}>
        <Stack spacing={2.5}>
          <TextField
            label="Name"
            value={form.name}
            onChange={(e) => setForm((prev) => ({ ...prev, name: e.target.value }))}
            required
            fullWidth
          />
          <TextField
            label="Description"
            value={form.description}
            onChange={(e) => setForm((prev) => ({ ...prev, description: e.target.value }))}
            required
            fullWidth
            multiline
            minRows={4}
            placeholder="Write a description in plain text..."
          />
          <TextField
            label="Recorded date"
            value={formatSystemDate(recordedAt)}
            fullWidth
            disabled
            helperText="Filled automatically from this computer."
          />
          <Stack direction="row" spacing={1} sx={{ justifyContent: "flex-end" }}>
            <Button type="button" variant="outlined" onClick={handleCancelClick} disabled={submitting}>
              Cancel
            </Button>
            <Button type="submit" disabled={submitting}>
              {submitting ? "Submitting..." : "Submit"}
            </Button>
          </Stack>
        </Stack>
      </Paper>

      {loading && <LinearProgress />}
      {error && <Alert severity="error">{error}</Alert>}
      {success && <Alert severity="success">{success}</Alert>}

      <Paper>
        <Box sx={{ px: { xs: 2, sm: 3 }, pt: { xs: 2, sm: 3 }, pb: 1 }}>
          <Typography variant="h6">Submitted items</Typography>
        </Box>
        <TableContainer>
          <Table sx={{ minWidth: 640 }}>
            <TableHead>
              <TableRow>
                <TableCell sx={{ width: 200 }}>Name</TableCell>
                <TableCell>Description</TableCell>
                <TableCell sx={{ width: 180 }}>Date</TableCell>
                <TableCell align="right" sx={{ width: 72 }} />
              </TableRow>
            </TableHead>
            <TableBody>
              {items.length === 0 && (
                <TableRow>
                  <TableCell colSpan={4}>
                    <Typography color="text.secondary">No demo items yet.</Typography>
                  </TableCell>
                </TableRow>
              )}
              {items.map((item) => (
                <TableRow key={item.id} hover>
                  <TableCell>{item.name}</TableCell>
                  <TableCell sx={{ whiteSpace: "pre-wrap", wordBreak: "break-word" }}>
                    {item.description}
                  </TableCell>
                  <TableCell>
                    {item.created_at ? formatSystemDate(new Date(item.created_at)) : "—"}
                  </TableCell>
                  <TableCell align="right">
                    <IconButton
                      aria-label={`Delete ${item.name}`}
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
            ? "Delete this item?"
            : confirm?.type === "cancel"
              ? "Clear this form?"
              : "Submit this item?"
        }
        message={
          confirm?.type === "delete"
            ? `${confirm.item?.name || "This item"} will be removed.`
            : confirm?.type === "cancel"
              ? "Unsaved text will be lost."
              : "This will send the item to the server."
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
