// Business layer: React hook wrapping the Employee Feedback data-service.
import { useCallback, useEffect, useState } from "react";
import { employeeFeedbackDataService } from "../dataservice/employeeFeedbackDataService";

function toErrorMessage(err) {
  const detail = err.response?.data?.detail;
  if (typeof detail === "string") return detail;
  return err.message || "Request failed";
}

export function useEmployeeFeedback() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setItems(await employeeFeedbackDataService.getAll());
    } catch (err) {
      setError(toErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const createItem = useCallback(async (payload) => {
    setSubmitting(true);
    setError(null);
    try {
      const created = await employeeFeedbackDataService.create(payload);
      setItems(await employeeFeedbackDataService.getAll());
      return created;
    } catch (err) {
      setError(toErrorMessage(err));
      throw err;
    } finally {
      setSubmitting(false);
    }
  }, []);

  const deleteItem = useCallback(
    async (id) => {
      await employeeFeedbackDataService.remove(id);
      await refresh();
    },
    [refresh]
  );

  return { items, loading, submitting, error, refresh, createItem, deleteItem };
}
