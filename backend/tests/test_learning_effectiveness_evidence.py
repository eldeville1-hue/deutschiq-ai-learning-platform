from app.services.learning_effectiveness_audit import learning_effectiveness_evidence


def test_missing_stages_are_reported():
    result = learning_effectiveness_evidence({'exercises': [{'stage': 'guided', 'type': 'choose'}]})
    assert 'effectiveness:missing_transfer_practice' in result['issues']
    assert 'effectiveness:no_independent_productive_task' in result['issues']


def test_full_progression_is_recognized():
    result = learning_effectiveness_evidence({'can_do': 'Describe your day', 'exercises': [{'stage': 'guided', 'type': 'choose'}, {'stage': 'independent', 'type': 'fill'}, {'stage': 'transfer', 'type': 'production'}]})
    assert result['issues'] == []
