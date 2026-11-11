from src.analysis.event_catalog import (
    EVENT_DEFINITIONS,
    PHASE_GROUPS,
    TEAM_BONUS_METRICS,
    TEAM_METRIC_KEYS,
    canonical_event_type,
    phase_metric_keys
)


def _empty_team_stats():
    return {
        **{metric: 0 for metric in TEAM_METRIC_KEYS},
        **{
            phase_metric: 0
            for group in PHASE_GROUPS
            for phase_metric in phase_metric_keys(group)
        },
        "recoveries": 0,
        "losses": 0,
        "events": 0
    }


def build_team_stats(events_df, our_venue="home"):
    """
    Separate stats into actual home and away sides.

    Event types from the client's perspective (``rival_`` prefix)
    are authoritative. The event's ``team`` field is used for unknown types
    and checked for inconsistencies, supporting older exports with stale
    team labels. Historical ``own_goal``, ``goal_rival``, and
    ``corner_against`` values are normalized to the current event names.
    """
    if our_venue not in ("home", "away"):
        raise ValueError("our_venue must be 'home' or 'away'")

    teams = {
        "home": _empty_team_stats(),
        "away": _empty_team_stats()
    }
    opponent_venue = "away" if our_venue == "home" else "home"
    mismatched_team_labels = 0
    unassigned_events = 0
    unknown_event_types = set()

    if events_df.empty:
        return {
            **teams,
            "our_venue": our_venue,
            "opponent_venue": opponent_venue,
            "mismatched_team_labels": 0,
            "unassigned_events": 0,
            "unknown_event_types": []
        }

    for event in events_df.to_dict("records"):
        original_event_type = event.get("eventType")
        event_type = canonical_event_type(original_event_type)
        declared_team = event.get("team")
        definition = EVENT_DEFINITIONS.get(event_type, {})
        event_side = definition.get("team_side")

        if event_side == "own":
            side = our_venue
            metric = definition.get("team_metric")
        elif event_side == "opponent" or (
            isinstance(event_type, str) and event_type.startswith("rival_")
        ):
            side = opponent_venue
            metric = definition.get("team_metric")
            if metric is None:
                unknown_event_types.add(event_type)
        elif declared_team in teams:
            side = declared_team
            metric = None
            if event_type is not None:
                unknown_event_types.add(event_type)
        else:
            unassigned_events += 1
            if event_type is not None:
                unknown_event_types.add(event_type)
            continue

        if declared_team in teams and declared_team != side:
            mismatched_team_labels += 1

        team_stats = teams[side]
        team_stats["events"] += 1
        if metric is not None:
            team_stats[metric] += 1
        for bonus_metric in TEAM_BONUS_METRICS.get(event_type, ()):
            team_stats[bonus_metric] += 1

    for side_stats in teams.values():
        for group, total_key in (("recoveries", "recoveries"), ("losses", "losses")):
            side_stats[total_key] = sum(
                side_stats[key]
                for key in phase_metric_keys(group)
            )

    return {
        **teams,
        "our_venue": our_venue,
        "opponent_venue": opponent_venue,
        "mismatched_team_labels": mismatched_team_labels,
        "unassigned_events": unassigned_events,
        "unknown_event_types": sorted(unknown_event_types)
    }
