"""
Basic load test for the Telemetry Service.

This is not a performance-engineering exercise -- it exists to show the
service behaves sanely under a burst of repeated requests (no crashes, no
runaway latency), not to characterize production capacity.

Usage:
    python tests/load/basic_load_test.py --count 1000 --url http://localhost:8001
"""
import argparse
import statistics
import time

import httpx


def run(url: str, count: int) -> int:
    payload_template = {
        "vehicle_id": "VIN-LOAD-{i}",
        "speed": 80,
        "battery_level": 70,
        "temperature": 38.0,
        "software_version": "1.0.0",
    }

    durations = []
    successes = 0
    failures = 0

    with httpx.Client(timeout=5.0) as client:
        for i in range(count):
            payload = dict(payload_template)
            payload["vehicle_id"] = f"VIN-LOAD-{i}"
            start = time.perf_counter()
            try:
                resp = client.post(f"{url}/telemetry", json=payload)
                elapsed_ms = (time.perf_counter() - start) * 1000
                durations.append(elapsed_ms)
                if resp.status_code == 201:
                    successes += 1
                else:
                    failures += 1
            except httpx.HTTPError:
                failures += 1

    print(f"Sent {count} telemetry events")
    print(f"Successful requests: {successes}")
    print(f"Failed requests: {failures}")
    if durations:
        print(f"Average response time: {statistics.mean(durations):.1f} ms")
        print(f"p95 response time: {sorted(durations)[int(len(durations) * 0.95) - 1]:.1f} ms")

    return 0 if failures == 0 else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8001")
    parser.add_argument("--count", type=int, default=1000)
    args = parser.parse_args()
    raise SystemExit(run(args.url, args.count))
