"""
dashboard_writer.py — Agent helper for writing dashboard status JSON files.

Usage from any Python agent:
    from dashboard_writer import DashboardWriter
    writer = DashboardWriter('/path/to/dashboard/data')
    writer.update_system_status(pipelines=..., budget=..., alerts=..., activity=...)
    writer.update_clinic(clinic_id=1, stories_completed=45, reels_completed=6, ...)

All writes are atomic: write to .tmp file, then os.rename() to final path.
This prevents the dashboard from reading partial/corrupt JSON.
"""

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class DashboardWriter:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        (self.data_dir / 'clinics').mkdir(exist_ok=True)

    def _atomic_write(self, filepath: Path, data: dict) -> None:
        """Write JSON atomically via temp file + rename."""
        tmp_fd, tmp_path = tempfile.mkstemp(
            suffix='.tmp',
            dir=filepath.parent,
        )
        try:
            with os.fdopen(tmp_fd, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            os.rename(tmp_path, str(filepath))
        except Exception:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _read_json(self, filepath: Path) -> Optional[dict]:
        try:
            with open(filepath) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    # === System Status ===

    def update_system_status(
        self,
        pipelines: Optional[List[dict]] = None,
        budget: Optional[dict] = None,
        alerts: Optional[List[dict]] = None,
        activity: Optional[List[dict]] = None,
        kpis: Optional[dict] = None,
    ) -> None:
        """Update system-status.json. Pass only the fields you want to change."""
        filepath = self.data_dir / 'system-status.json'
        current = self._read_json(filepath) or {}

        if pipelines is not None:
            current['pipelines'] = pipelines
        if budget is not None:
            current['budget'] = budget
        if alerts is not None:
            current['alerts'] = alerts
        if activity is not None:
            current['activity'] = activity
        if kpis is not None:
            current['kpis'] = kpis

        current['lastUpdated'] = self._now()
        self._atomic_write(filepath, current)

    def add_alert(self, level: str, message: str, pipeline: Optional[str] = None) -> None:
        """Append an alert to system-status.json."""
        filepath = self.data_dir / 'system-status.json'
        current = self._read_json(filepath) or {'alerts': []}
        alerts = current.get('alerts', [])

        alert = {
            'id': f'a{len(alerts) + 1}',
            'level': level,
            'message': message,
            'timestamp': self._now(),
        }
        if pipeline:
            alert['pipeline'] = pipeline

        alerts.insert(0, alert)
        current['alerts'] = alerts[:20]  # Keep last 20
        current['lastUpdated'] = self._now()
        self._atomic_write(filepath, current)

    def add_activity(self, action: str, detail: str, pipeline: str = 'system') -> None:
        """Append an activity item to system-status.json."""
        filepath = self.data_dir / 'system-status.json'
        current = self._read_json(filepath) or {'activity': []}
        activity = current.get('activity', [])

        item = {
            'id': f'act{len(activity) + 1}',
            'action': action,
            'detail': detail,
            'timestamp': self._now(),
            'pipeline': pipeline,
        }

        activity.insert(0, item)
        current['activity'] = activity[:50]  # Keep last 50
        current['lastUpdated'] = self._now()
        self._atomic_write(filepath, current)

    # === Clinic Updates ===

    def update_clinic(self, clinic_id: int, **updates: Any) -> None:
        """Update a specific clinic's detail file. Pass any fields to update."""
        padded = str(clinic_id).zfill(3)
        filepath = self.data_dir / 'clinics' / f'clinic-{padded}.json'
        current = self._read_json(filepath)
        if not current:
            raise FileNotFoundError(f'Clinic file not found: {filepath}')

        for key, value in updates.items():
            current[key] = value

        self._atomic_write(filepath, current)

    def update_clinic_story_status(
        self, clinic_id: int, day: int, slot: int, status: str
    ) -> None:
        """Update a specific story slot's status for a clinic."""
        padded = str(clinic_id).zfill(3)
        filepath = self.data_dir / 'clinics' / f'clinic-{padded}.json'
        current = self._read_json(filepath)
        if not current:
            raise FileNotFoundError(f'Clinic file not found: {filepath}')

        for story in current.get('stories', []):
            if story['day'] == day and story['slot'] == slot:
                story['status'] = status
                break

        self._atomic_write(filepath, current)

    # === Batch Operations ===

    def batch_update_pipeline_stats(
        self,
        pipeline_name: str,
        completed_delta: int = 0,
        in_progress_delta: int = 0,
        failed_delta: int = 0,
    ) -> None:
        """Increment pipeline counters in system-status.json."""
        filepath = self.data_dir / 'system-status.json'
        current = self._read_json(filepath) or {}

        for p in current.get('pipelines', []):
            if p['name'] == pipeline_name:
                p['completed'] = p.get('completed', 0) + completed_delta
                p['inProgress'] = max(0, p.get('inProgress', 0) + in_progress_delta)
                p['failed'] = p.get('failed', 0) + failed_delta
                break

        current['lastUpdated'] = self._now()
        self._atomic_write(filepath, current)

    def update_budget_spend(self, stories: float = 0, reels: float = 0, seo: float = 0) -> None:
        """Update the current budget spent amount."""
        filepath = self.data_dir / 'system-status.json'
        current = self._read_json(filepath) or {}
        budget = current.get('budget', {})
        budget['spent'] = budget.get('spent', 0) + stories + reels + seo
        current['budget'] = budget
        current['lastUpdated'] = self._now()
        self._atomic_write(filepath, current)


if __name__ == '__main__':
    # Quick test
    writer = DashboardWriter(os.path.join(os.path.dirname(__file__), '..', 'data'))
    writer.add_activity('test', 'Dashboard writer test — connection verified', 'system')
    print('Dashboard writer OK — test activity added to system-status.json')
