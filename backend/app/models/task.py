"""
任务状态管理
用于跟踪长时间运行的任务（如图谱构建）
"""

import uuid
import threading
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


class TaskStatus(str, Enum):
    """任务状态枚举"""
    PENDING = "pending"          # 等待中
    PROCESSING = "processing"    # 处理中
    COMPLETED = "completed"      # 已完成
    FAILED = "failed"            # 失败


@dataclass
class Task:
    """任务数据类"""
    task_id: str
    task_type: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    progress: int = 0              # 总进度百分比 0-100
    message: str = ""              # 状态消息
    result: Optional[Dict] = None  # 任务结果
    error: Optional[str] = None    # 错误信息
    metadata: Dict = field(default_factory=dict)  # 额外元数据
    progress_detail: Dict = field(default_factory=dict)  # 详细进度信息
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "progress": self.progress,
            "message": self.message,
            "progress_detail": self.progress_detail,
            "result": self.result,
            "error": self.error,
            "metadata": self.metadata,
        }


class _InMemoryTaskManager:
    """
    原始内存任务管理器（保留作为 PersistentTaskManager 的降级后备）。
    线程安全的任务状态管理
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._tasks: Dict[str, Task] = {}
                    cls._instance._task_lock = threading.Lock()
        return cls._instance
    
    def create_task(self, task_type: str, metadata: Optional[Dict] = None) -> str:
        """
        创建新任务
        
        Args:
            task_type: 任务类型
            metadata: 额外元数据
            
        Returns:
            任务ID
        """
        task_id = str(uuid.uuid4())
        now = datetime.now()
        
        task = Task(
            task_id=task_id,
            task_type=task_type,
            status=TaskStatus.PENDING,
            created_at=now,
            updated_at=now,
            metadata=metadata or {}
        )
        
        with self._task_lock:
            self._tasks[task_id] = task
        
        return task_id
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务"""
        with self._task_lock:
            return self._tasks.get(task_id)
    
    def update_task(
        self,
        task_id: str,
        status: Optional[TaskStatus] = None,
        progress: Optional[int] = None,
        message: Optional[str] = None,
        result: Optional[Dict] = None,
        error: Optional[str] = None,
        progress_detail: Optional[Dict] = None
    ):
        """
        更新任务状态
        
        Args:
            task_id: 任务ID
            status: 新状态
            progress: 进度
            message: 消息
            result: 结果
            error: 错误信息
            progress_detail: 详细进度信息
        """
        with self._task_lock:
            task = self._tasks.get(task_id)
            if task:
                task.updated_at = datetime.now()
                if status is not None:
                    task.status = status
                if progress is not None:
                    task.progress = progress
                if message is not None:
                    task.message = message
                if result is not None:
                    task.result = result
                if error is not None:
                    task.error = error
                if progress_detail is not None:
                    task.progress_detail = progress_detail
    
    def complete_task(self, task_id: str, result: Dict):
        """标记任务完成"""
        self.update_task(
            task_id,
            status=TaskStatus.COMPLETED,
            progress=100,
            message="任务完成",
            result=result
        )
    
    def fail_task(self, task_id: str, error: str):
        """标记任务失败"""
        self.update_task(
            task_id,
            status=TaskStatus.FAILED,
            message="任务失败",
            error=error
        )
    
    def list_tasks(self, task_type: Optional[str] = None) -> list:
        """列出任务"""
        with self._task_lock:
            tasks = list(self._tasks.values())
            if task_type:
                tasks = [t for t in tasks if t.task_type == task_type]
            return [t.to_dict() for t in sorted(tasks, key=lambda x: x.created_at, reverse=True)]
    
    def cleanup_old_tasks(self, max_age_hours: int = 24):
        """清理旧任务"""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(hours=max_age_hours)

        with self._task_lock:
            old_ids = [
                tid for tid, task in self._tasks.items()
                if task.created_at < cutoff and task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]
            ]
            for tid in old_ids:
                del self._tasks[tid]


class PersistentTaskManager:
    """
    Drop-in replacement for TaskManager that persists tasks to SQLite.

    Maintains the exact same public API so callers do not need to change.
    Falls back to the in-memory TaskManager if the SQLite store cannot be
    initialised (e.g. read-only filesystem).
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    inst = super().__new__(cls)
                    try:
                        from ..services.task_store import SQLiteTaskStore
                        inst._store = SQLiteTaskStore()
                        inst._use_sqlite = True
                    except Exception:
                        # Fallback to in-memory
                        inst._store = None
                        inst._use_sqlite = False
                        inst._fallback = _InMemoryTaskManager()
                    cls._instance = inst
        return cls._instance

    # ------------------------------------------------------------------
    # Delegate to SQLiteTaskStore (dict-based rows) and wrap results back
    # into Task dataclass objects where the old callers expect them.
    # ------------------------------------------------------------------

    def _row_to_task(self, row: dict) -> Task:
        return Task(
            task_id=row["task_id"],
            task_type=row["task_type"],
            status=TaskStatus(row["status"]) if row["status"] in [s.value for s in TaskStatus] else TaskStatus.FAILED,
            created_at=datetime.fromisoformat(row["created_at"]) if isinstance(row["created_at"], str) else row["created_at"],
            updated_at=datetime.fromisoformat(row["updated_at"]) if isinstance(row["updated_at"], str) else row["updated_at"],
            progress=int(row.get("progress", 0)),
            message=row.get("message", ""),
            result=row.get("result"),
            error=row.get("error"),
            metadata=row.get("metadata", {}),
            progress_detail=row.get("progress_detail", {}),
        )

    def create_task(self, task_type: str, metadata: Optional[Dict] = None) -> str:
        if not self._use_sqlite:
            return self._fallback.create_task(task_type, metadata)
        task_id = str(uuid.uuid4())
        self._store.create_task(task_id, task_type, metadata)
        return task_id

    def get_task(self, task_id: str) -> Optional[Task]:
        if not self._use_sqlite:
            return self._fallback.get_task(task_id)
        row = self._store.get_task(task_id)
        if row is None:
            return None
        return self._row_to_task(row)

    def update_task(
        self,
        task_id: str,
        status: Optional[TaskStatus] = None,
        progress: Optional[int] = None,
        message: Optional[str] = None,
        result: Optional[Dict] = None,
        error: Optional[str] = None,
        progress_detail: Optional[Dict] = None,
    ):
        if not self._use_sqlite:
            return self._fallback.update_task(
                task_id, status=status, progress=progress, message=message,
                result=result, error=error, progress_detail=progress_detail,
            )
        kwargs: Dict[str, Any] = {}
        if status is not None:
            kwargs["status"] = status.value if isinstance(status, TaskStatus) else status
        if progress is not None:
            kwargs["progress"] = progress
        if message is not None:
            kwargs["message"] = message
        if result is not None:
            kwargs["result"] = result
        if error is not None:
            kwargs["error"] = error
        if progress_detail is not None:
            kwargs["progress_detail"] = progress_detail
        self._store.update_task(task_id, **kwargs)

    def complete_task(self, task_id: str, result: Dict):
        if not self._use_sqlite:
            return self._fallback.complete_task(task_id, result)
        self._store.complete_task(task_id, result)

    def fail_task(self, task_id: str, error: str):
        if not self._use_sqlite:
            return self._fallback.fail_task(task_id, error)
        self._store.fail_task(task_id, error)

    def list_tasks(self, task_type: Optional[str] = None) -> list:
        if not self._use_sqlite:
            return self._fallback.list_tasks(task_type)
        return self._store.get_all_tasks(task_type)

    def cleanup_old_tasks(self, max_age_hours: int = 24):
        if not self._use_sqlite:
            return self._fallback.cleanup_old_tasks(max_age_hours)
        self._store.cleanup_old_tasks(max_age_hours)


# Alias: all existing code imports TaskManager — point it to the persistent version.
TaskManager = PersistentTaskManager

