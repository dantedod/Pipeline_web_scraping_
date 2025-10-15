# src/pipeline.py
import logging
from typing import List


class Pipeline:
    def __init__(self, tasks: List):
        self.tasks = tasks

    def run(self, data=None):
        results = {}
        for task in self.tasks:
            logging.info(f" Executando etapa: {task.name}")
            try:
                task_data = task.execute(data)
                results[task.name] = task_data
            except Exception as e:
                logging.error(f" Erro na etapa {task.name}: {e}")
                break
        return results
