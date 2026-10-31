"""Unit tests for Production Security (HMAC, Idempotency) and Telematics Simulator.
Skills: security-and-hardening | wrangler-automation | poteto-mode
"""
import time
import json
import pytest
from src.security.middleware import (
    generate_hmac_signature,
    verify_hmac_signature,
    idempotency_store,
    DEFAULT_HMAC_SECRET
)
from src.telematics.simulator import TelematicsSimulator

def test_hmac_signature_generation_and_validation():
    payload = json.dumps({"order_id": "ORD-TEST-99", "weight_kg": 20.0})
    ts = str(int(time.time()))

    # 1. Generate valid signature
    sig = generate_hmac_signature(payload, ts, DEFAULT_HMAC_SECRET)
    assert len(sig) == 64, "SHA-256 signature must be 64 hex characters"

    # 2. Verify valid signature passes
    assert verify_hmac_signature(payload, sig, ts, DEFAULT_HMAC_SECRET) is True

    # 3. Tampered payload fails
    tampered_payload = json.dumps({"order_id": "ORD-TEST-99", "weight_kg": 999.0})
    with pytest.raises(Exception):
        verify_hmac_signature(tampered_payload, sig, ts, DEFAULT_HMAC_SECRET)

def test_hmac_timestamp_expiration():
    payload = json.dumps({"order_id": "ORD-TEST-99"})
    expired_ts = str(int(time.time()) - 400)  # >300s drift
    sig = generate_hmac_signature(payload, expired_ts, DEFAULT_HMAC_SECRET)

    with pytest.raises(Exception):
        verify_hmac_signature(payload, sig, expired_ts, DEFAULT_HMAC_SECRET, tolerance_sec=300)

def test_idempotency_store_lifecycle():
    key = f"IDEM-TEST-{time.time()}"
    data = {"status": "SUCCESS", "allocated_driver": "D01"}

    assert idempotency_store.get(key) is None
    idempotency_store.set(key, data)

    retrieved = idempotency_store.get(key)
    assert retrieved is not None
    assert retrieved["allocated_driver"] == "D01"

def test_telematics_simulator_tick_and_movement():
    sim = TelematicsSimulator()
    snapshot_1 = sim.get_snapshot()
    assert len(snapshot_1) == 10, "Fleet must have 10 vehicles"

    # Tick simulation forward
    snapshot_2 = sim.tick()
    assert len(snapshot_2) == 10

    # Check driver D01 moved
    d01_initial = [v for v in snapshot_1 if v["driver_id"] == "D01"][0]
    d01_ticked = [v for v in snapshot_2 if v["driver_id"] == "D01"][0]
    assert d01_ticked["odometer_km"] >= d01_initial["odometer_km"]

    # Check driver D09 is shift limit blocked
    d09 = [v for v in snapshot_2 if v["driver_id"] == "D09"][0]
    assert d09["status"] == "SHIFT_LIMIT_BLOCKED"
    assert d09["speed_kmh"] == 0.0

