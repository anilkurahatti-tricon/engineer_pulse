// Business layer: React hook wrapping the Employee Feedback data-service.
import { useCallback, useEffect, useState } from "react";
import { employeeFeedbackDataService } from "../dataservice/employeeFeedbackDataService";

export function useEmployeeFeedback() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setItems(await employeeFeedbackDataService.getAll());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const createItem = useCallback(
    async (payload) => {
      await employeeFeedbackDataService.create(payload);
      await refresh();
    },
    [refresh]
  );

  const deleteItem = useCallback(
    async (id) => {
      await employeeFeedbackDataService.remove(id);
      await refresh();
    },
    [refresh]
  );

  return { items, loading, error, refresh, createItem, deleteItem };
}
