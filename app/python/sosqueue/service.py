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
        """
        El usuario acepta el turno:
        sólo si está primero, se rota al final.
        """
        with self._lock:
            if not self._queue or self._queue[0]['id'] != user.id:
                raise ValueError("No te toca todavía")
            first = self._queue.pop(0)
            self._queue.append(first)
            return self._queue

    def leave(self, user):
        """
        El usuario decide salir de la cola:
        se elimina donde esté y se añade al final.
        """
        with self._lock:
            for idx,u in enumerate(self._queue):
                if u['id'] == user.id:
                    usr = self._queue.pop(idx)
                    self._queue.append(usr)
                    return self._queue
            raise ValueError("No estás en la cola")