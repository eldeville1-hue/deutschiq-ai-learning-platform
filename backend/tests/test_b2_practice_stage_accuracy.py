from seed_30_day_plan import B2_CURRICULUM, build_b2_content


def test_b2_repetition_is_guided_and_dialogue_is_transfer():
    for row in B2_CURRICULUM:
        exercises = build_b2_content(row)['exercises']
        assert all(item['stage'] == 'guided' for item in exercises if item['type'] == 'repeat')
        assert any(item['stage'] == 'transfer' and item['type'] == 'dialogue' for item in exercises)
