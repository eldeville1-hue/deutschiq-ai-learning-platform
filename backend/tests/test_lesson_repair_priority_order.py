from audit_curriculum import build_report


def test_repair_queue_has_deterministic_severity_order():
    queue = build_report()['repair_queue']
    assert queue == sorted(queue, key=lambda item: (-len(item['issues']), item['track'], item['day']))
