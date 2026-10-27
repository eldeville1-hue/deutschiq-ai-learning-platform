from seed_30_day_plan import A1_CURRICULUM, A2_CURRICULUM, B1_CURRICULUM, build_foundation_content, build_b1_content


def test_repetition_is_guided_across_a1_a2_b1():
    lessons = [*(build_foundation_content(row, 'A1') for row in A1_CURRICULUM), *(build_foundation_content(row, 'A2') for row in A2_CURRICULUM), *(build_b1_content(row) for row in B1_CURRICULUM)]
    for lesson in lessons:
        exercises = lesson['exercises']
        assert all(item['stage'] == 'guided' for item in exercises if item['type'] == 'repeat')
        assert any(item['stage'] == 'transfer' and item['type'] == 'dialogue' for item in exercises)
