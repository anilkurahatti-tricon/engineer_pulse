// Business layer: React hook wrapping the Demo data-service with local
// state and simple CRUD orchestration used by the presentation layer.
import { useCallback, useEffect, useState } from "react";
import { demoDataService } from "../dataservice/demoDataService";

export function useDemoItems() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setItems(await demoDataService.getAll());
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
      await demoDataService.create(payload);
      await refresh();
    },
    [refresh]
  );

  const deleteItem = useCallback(
    async (id) => {
      await demoDataService.remove(id);
      await refresh();
    },
    [refresh]
  );

  return { items, loading, error, refresh, createItem, deleteItem };
}
