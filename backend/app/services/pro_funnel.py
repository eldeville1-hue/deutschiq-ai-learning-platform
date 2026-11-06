def pro_interest_funnel(events) -> dict:
    """Count unique users who expressed interest after viewing Pro in this window."""
    first_view = {}
    interested = set()
    converted = set()
    preview_events = 0
    interest_events = 0

    # Callers provide ascending event timestamps. Sorting also makes this helper
    # correct for unsorted inputs, and the original index breaks timestamp ties.
    ordered = sorted(enumerate(events), key=lambda item: (item[1].created_at, item[0]))
    for _, event in ordered:
        if event.event_name == "pro_preview_viewed":
            preview_events += 1
            first_view.setdefault(event.user_id, event.created_at)
        elif event.event_name == "pro_interest_clicked":
            interest_events += 1
            interested.add(event.user_id)
            if event.user_id in first_view:
                converted.add(event.user_id)

    return {
        "preview_users": len(first_view),
        "interest_users": len(interested),
        "preview_to_interest_users": len(converted),
        "conversion_percent": round(len(converted) / len(first_view) * 100, 1) if first_view else 0,
        "preview_events": preview_events,
        "interest_events": interest_events,
    }
