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
                raise ValueError("El usuario ya está en esta cola")
            self._queue.append({'id': user.id, 'name': user.username})
            return self._queue

    def remove(self, user_id: int):
        """
        NUEVO: Elimina a un usuario por ID. 
        Devuelve True si se eliminó, False si no se encontró.
        """
        with self._lock:
            initial_len = len(self._queue)
            self._queue = [u for u in self._queue if u['id'] != user_id]
            return initial_len != len(self._queue)

    def pop_first(self):
        """
        NUEVO: Elimina y devuelve el primer elemento de la cola.
        Devuelve None si la cola está vacía.
        """
        with self._lock:
            if not self._queue:
                return None
            return self._queue.pop(0)

    # ---------- utilidades para administrador (sin cambios) ----------
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
    
class JobService:
    """
    Un servicio simple para gestionar una lista de trabajos pendientes.
    """
    def __init__(self):
        self._jobs = []  # Una simple lista, ej: [{'id': 1}, {'id': 2}]
        self._lock = Lock()
        self._next_id = 1

    def add_job(self):
        """Añade un nuevo trabajo a la lista y lo devuelve."""
        with self._lock:
            new_job = {'id': self._next_id}
            self._jobs.append(new_job)
            self._next_id += 1
            return new_job

    def take_job(self):
        """
        Elimina y devuelve el trabajo más antiguo de la lista.
        Devuelve None si la cola está vacía.
        """
        with self._lock:
            if not self._jobs:
                return None
            return self._jobs.pop(0)

    def get_job_count(self):
        """Devuelve el número de trabajos disponibles."""
        with self._lock:
            return len(self._jobs)