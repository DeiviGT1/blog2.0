# app/python/sosqueue/service.py

from threading import Lock

class QueueService:
    def __init__(self):
        # lista de dicts: { id: int, name: str }
        self._queue = []
        self._lock = Lock()

    def get_queue(self):
        """Devuelve la cola completa en orden."""
        with self._lock:
            return list(self._queue)

    def join(self, user):
        """Añade al usuario al final si no está ya."""
        with self._lock:
            if any(u['id'] == user.id for u in self._queue):
                raise ValueError("Ya estás en la cola")
            self._queue.append({'id': user.id, 'name': user.username})
            return self._queue

    def work(self, user):
        """Si está primero, lo rota al final."""
        with self._lock:
            if not self._queue or self._queue[0]['id'] != user.id:
                raise ValueError("No te toca todavía")
            first = self._queue.pop(0)
            self._queue.append(first)
            return self._queue

    def leave(self, user):
        """El usuario decide salir de la cola: se mueve al final."""
        with self._lock:
            for idx, u in enumerate(self._queue):
                if u['id'] == user.id:
                    usr = self._queue.pop(idx)
                    self._queue.append(usr)
                    return self._queue
            raise ValueError("No estás en la cola")

    def move_all_to(self, other_queue_service):
        """Pasa todos los usuarios a otra cola."""
        with self._lock:
            items = list(self._queue)
            self._queue.clear()
        with other_queue_service._lock:
            other_queue_service._queue.extend(items)

    # ---------- utilidades para administrador ----------
    def _find_idx(self, user_id: int):
        for idx, u in enumerate(self._queue):
            if u['id'] == user_id:
                return idx
        return -1

    def move_up(self, user_id: int):
        with self._lock:
            idx = self._find_idx(user_id)
            if idx > 0:
                self._queue[idx-1], self._queue[idx] = self._queue[idx], self._queue[idx-1]
        return self._queue

    def move_down(self, user_id: int):
        with self._lock:
            idx = self._find_idx(user_id)
            if 0 <= idx < len(self._queue)-1:
                self._queue[idx+1], self._queue[idx] = self._queue[idx], self._queue[idx+1]
        return self._queue