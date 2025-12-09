import argparse
import json
import os
from typing import Optional
import pandas as pd

class TaskManager:
    def __init__(self, path: str):
        self.path = path
        self._ensure_file_exists(self.path)
        self.tasks = self._load_tasks()

    def _ensure_file_exists(self, path: str) -> None:
        """Создаёт файл (и директорию) если его нет."""
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"tasks": []}, f, indent=4, ensure_ascii=False)
            print(f"Создан новый файл: {path}")

    def _load_tasks(self) -> dict:
        """Загружает JSON с задачами. В случае ошибки возвращает пустой список."""
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if "tasks" not in data or not isinstance(data["tasks"], list):
                return {"tasks": []}
            return data
        except (json.JSONDecodeError, FileNotFoundError):
            return {"tasks": []}

    def _save(self) -> None:
        """Сохраняет текущее состояние задач в файл."""
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=4, ensure_ascii=False)

    def _find_index_by_id(self, task_id: int) -> Optional[int]:
        """Возвращает индекс в списке self.tasks['tasks'] по полю id, либо None."""
        for idx, t in enumerate(self.tasks["tasks"]):
            if t.get("id") == task_id:
                return idx
        return None

    def add_task(self, new_task: str, status: bool = False) -> str:
        """Добавляет задачу и возвращает сообщение."""
        # вычисляем новый уникальный id
        existing_ids = [t.get("id", 0) for t in self.tasks["tasks"]]
        new_id = max(existing_ids, default=0) + 1
        self.tasks["tasks"].append({
            "id": new_id,
            "description": new_task,
            "completed": bool(status)
        })
        self._save()
        return f"Задача добавлена (id={new_id})."

    def list_task(self, status: str = 'all'):
        """Возвращает DataFrame с задачами в зависимости от статуса или сообщение, если пусто."""
        if not self.tasks["tasks"]:
            return self._fallback("empty")

        df = pd.DataFrame.from_dict(self.tasks["tasks"])
        if status == 'all':
            return df
        elif status == 'completed':
            return df[df['completed'] == True]
        elif status == 'pending':
            return df[df['completed'] == False]
        else:
            return self._fallback("unknown_status")

    def complete_task(self, task_id: int) -> str:
        """Помечает задачу с данным id как выполненную."""
        idx = self._find_index_by_id(task_id)
        if idx is None:
            return self._fallback("bad_id")
        self.tasks["tasks"][idx]["completed"] = True
        self._save()
        return f"Задача с id={task_id} помечена как выполненная."

    def delete_task(self, task_id: int) -> str:
        """Удаляет задачу с данным id."""
        idx = self._find_index_by_id(task_id)
        if idx is None:
            return self._fallback("bad_id")
        deleted = self.tasks["tasks"].pop(idx)
        self._save()
        return f"Задача с id={task_id} удалена."

    def operation(self, args):
        if args.command == 'add':
            description = " ".join(args.description) if isinstance(args.description, (list, tuple)) else args.description
            return self.add_task(description)
        elif args.command == 'list':
            status = args.status or 'all'
            return self.list_task(status)
        elif args.command == 'complete':
            return self.complete_task(args.task_id)
        elif args.command == 'delete':
            return self.delete_task(args.task_id)
        else:
            return self._fallback("unknown_command")

    def _fallback(self, reason: str = None) -> str:
        if reason == "empty":
            return "Список задач пуст. Добавьте новую задачу."
        elif reason == "bad_id":
            return "Указан неверный ID задачи."
        elif reason == "unknown_status":
            return "Неизвестный статус. Используйте all/completed/pending."
        else:
            return "Произошла неизвестная ошибка."

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Task Manager CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    add_parser = subparsers.add_parser('add', help='Adds a new task')
    list_parser = subparsers.add_parser('list', help='Lists tasks')
    complete_parser = subparsers.add_parser('complete', help='Marks a task as completed')
    delete_parser = subparsers.add_parser('delete', help='Deletes a task')

    add_parser.add_argument('description', type=str, nargs='+',
                            help='Description of the new task')
    list_parser.add_argument('--status', type=str,
                             choices=['all', 'completed', 'pending'],
                             default='all',
                             help='Filter by status')
    complete_parser.add_argument('task_id', type=int, help='ID of the task to mark as completed')
    delete_parser.add_argument('task_id', type=int, help='ID of the task to delete')

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    tm = TaskManager('tasks.json')
    result = tm.operation(args)

    if isinstance(result, pd.DataFrame):
        print(result.to_string(index=False))
    else:
        print(result)

if __name__ == "__main__":
    main()
