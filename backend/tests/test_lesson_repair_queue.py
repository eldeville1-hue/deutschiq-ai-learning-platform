from audit_curriculum import build_report


def test_repair_queue_matches_editorial_evidence():
    report = build_report()
    expected = {(track, item['day']) for track, lessons in report['learning_effectiveness_evidence'].items() for item in lessons if item['issues']}
    actual = {(item['track'], item['day']) for item in report['repair_queue']}
    assert actual == expected
    assert all(item['issues'] for item in report['repair_queue'])
