// Business layer: React hook wrapping the Demo data-service.
import { useCallback, useEffect, useState } from "react";
import { demoDataService } from "../dataservice/demoDataService";

function toErrorMessage(err) {
  const detail = err.response?.data?.detail;
  if (typeof detail === "string") return detail;
  return err.message || "Request failed";
}

export function useDemoItems() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setItems(await demoDataService.getAll());
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
      const created = await demoDataService.create(payload);
      setItems(await demoDataService.getAll());
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
      await demoDataService.remove(id);
      await refresh();
    },
    [refresh]
  );

  return { items, loading, submitting, error, refresh, createItem, deleteItem };
}
