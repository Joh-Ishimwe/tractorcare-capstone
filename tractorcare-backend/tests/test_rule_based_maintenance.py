"""Unit tests for the manual-driven maintenance rule engine."""
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rule_based_maintenance import (  # noqa: E402
    MAINTENANCE_SCHEDULES,
    MaintenancePredictor,
    MaintenanceStatus,
    Tractor,
    UnifiedMaintenanceEngine,
    UsageIntensity,
)


def make_tractor(days_ago=0, hours=0.0, intensity=UsageIntensity.MODERATE, model="MF_240"):
    purchase = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    return Tractor("t1", model, "Massey Ferguson", purchase, initial_engine_hours=0.0,
                   usage_intensity=intensity), hours


def test_schedules_cite_their_manual_source():
    for model, tasks in MAINTENANCE_SCHEDULES.items():
        for name, task in tasks.items():
            assert task.source, f"{model}/{name} has no manual reference"
            assert task.interval_hours > 0 and task.interval_days > 0


def test_new_tractor_has_no_alerts():
    tractor, _ = make_tractor()
    assert MaintenancePredictor(tractor).predict_all_maintenance() == []


def test_alert_fires_at_90_percent_of_hours_interval():
    tractor, _ = make_tractor()
    interval = MAINTENANCE_SCHEDULES["MF_240"]["engine_oil_change"].interval_hours
    tractor.update_engine_hours(interval * 0.95)
    alert = MaintenancePredictor(tractor).predict_maintenance("engine_oil_change")
    assert alert is not None and alert.status == MaintenanceStatus.DUE


def test_no_alert_below_90_percent():
    tractor, _ = make_tractor()
    interval = MAINTENANCE_SCHEDULES["MF_240"]["engine_oil_change"].interval_hours
    tractor.update_engine_hours(interval * 0.5)
    assert MaintenancePredictor(tractor).predict_maintenance("engine_oil_change") is None


def test_overdue_beyond_100_percent():
    tractor, _ = make_tractor()
    interval = MAINTENANCE_SCHEDULES["MF_240"]["engine_oil_change"].interval_hours
    tractor.update_engine_hours(interval * 1.05)
    alert = MaintenancePredictor(tractor).predict_maintenance("engine_oil_change")
    assert alert.status == MaintenanceStatus.OVERDUE


def test_calendar_trigger_fires_even_with_zero_hours():
    """Dual trigger: whichever of hours/calendar comes first."""
    interval_days = MAINTENANCE_SCHEDULES["MF_240"]["engine_oil_change"].interval_days
    tractor, _ = make_tractor(days_ago=int(interval_days * 1.2))
    alert = MaintenancePredictor(tractor).predict_maintenance("engine_oil_change")
    assert alert is not None and alert.status == MaintenanceStatus.OVERDUE


def test_heavy_usage_shortens_interval():
    interval = MAINTENANCE_SCHEDULES["MF_240"]["engine_oil_change"].interval_hours
    hours = interval * 0.8  # below threshold when moderate, above when heavy (0.8*1.2 = 0.96)
    moderate, _ = make_tractor(intensity=UsageIntensity.MODERATE)
    heavy, _ = make_tractor(intensity=UsageIntensity.HEAVY)
    moderate.update_engine_hours(hours)
    heavy.update_engine_hours(hours)
    assert MaintenancePredictor(moderate).predict_maintenance("engine_oil_change") is None
    assert MaintenancePredictor(heavy).predict_maintenance("engine_oil_change") is not None


def test_engine_hours_cannot_decrease():
    tractor, _ = make_tractor()
    assert tractor.update_engine_hours(100) is True
    assert tractor.update_engine_hours(50) is False
    assert tractor.engine_hours == 100


def test_unknown_model_is_rejected():
    tractor, _ = make_tractor(model="NOT_A_MODEL")
    with pytest.raises(ValueError):
        MaintenancePredictor(tractor)


def test_health_score_drops_with_recent_anomalies():
    tractor, _ = make_tractor()
    engine = UnifiedMaintenanceEngine(tractor)
    engine.generate_all_alerts()
    healthy = engine._calculate_health_score()
    for _ in range(3):
        tractor.add_anomaly({"score": 0.9})
    assert engine._calculate_health_score() < healthy


@pytest.mark.parametrize("score,label", [(95, "excellent"), (80, "good"), (65, "fair"),
                                         (50, "poor"), (10, "critical")])
def test_health_status_bands(score, label):
    tractor, _ = make_tractor()
    assert UnifiedMaintenanceEngine(tractor)._get_health_status(score) == label
