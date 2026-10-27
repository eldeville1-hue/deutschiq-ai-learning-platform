from seed_30_day_plan import B2_CURRICULUM, build_b2_content


def test_b2_transfer_prompts_request_own_examples():
    for row in B2_CURRICULUM:
        lesson = build_b2_content(row)
        dialogue = next(item for item in lesson['exercises'] if item['type'] == 'dialogue')
        for language in ('ru', 'de', 'en'):
            prompt = dialogue['i18n'][language]['question']
            assert prompt.strip()
            assert {'ru': 'Приведи собственный пример.', 'de': 'Nenne ein eigenes Beispiel.', 'en': 'Add your own example.'}[language] in prompt
