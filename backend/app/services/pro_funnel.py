def pro_interest_funnel(events) -> dict:
    """Unique-user Pro interest funnel; event totals are kept separately."""
    viewed = {event.user_id for event in events if event.event_name == "pro_preview_viewed"}
    interested = {event.user_id for event in events if event.event_name == "pro_interest_clicked"}
    return {
        "preview_users": len(viewed),
        "interest_users": len(interested),
        "preview_to_interest_users": len(viewed & interested),
        "conversion_percent": round(len(viewed & interested) / len(viewed) * 100, 1) if viewed else 0,
        "preview_events": sum(event.event_name == "pro_preview_viewed" for event in events),
        "interest_events": sum(event.event_name == "pro_interest_clicked" for event in events),
    }
