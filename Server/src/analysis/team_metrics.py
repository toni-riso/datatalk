OWN_EVENT_TYPES = {
    "buildout_success": "buildout_success",
    "buildout_fail": "buildout_fail",
    "loss_buildout": "loss_buildout",
    "dribble_ok": "dribble_ok",
    "dribble_bad": "dribble_bad",
    "loss_build": "loss_build",
    "shot_off": "shots_off",
    "shot_target": "shots_target",
    "goal_own": "goals",
    "assist": "assists",
    "recovery_buildout": "recovery_buildout",
    "recovery_build": "recovery_build",
    "recovery_finish": "recovery_finish",
    "loss_finish": "loss_finish",
    "foul_committed": "fouls_committed",
    "foul_received": "fouls_received",
    "yellow": "yellow",
    "corner_for": "corners_for",
    "recovery": "recoveries",
    "loss": "losses",
    "substitution": None
}

OPPONENT_EVENT_TYPES = {
    "rival_buildout_success": "buildout_success",
    "rival_buildout_fail": "buildout_fail",
    "rival_shot_off": "shots_off",
    "rival_shot_target": "shots_target",
    "rival_goal": "goals",
    "rival_corner": "corners_for"
}

LEGACY_EVENT_TYPES = {
    "goal_rival": "rival_goal",
    "corner_against": "rival_corner"
}


def _empty_team_stats():
    return {
        "buildout_success": 0,
        "buildout_fail": 0,
        "dribble_ok": 0,
        "dribble_bad": 0,
        "shots_off": 0,
        "shots_target": 0,
        "goals": 0,
        "assists": 0,
        "recovery_buildout": 0,
        "recovery_build": 0,
        "recovery_finish": 0,
        "recoveries": 0,
        "loss_buildout": 0,
        "loss_build": 0,
        "loss_finish": 0,
        "losses": 0,
        "fouls_committed": 0,
        "fouls_received": 0,
        "yellow": 0,
        "corners_for": 0,
        "events": 0
    }


def build_team_stats(events_df, our_venue="home"):
    """
    Separate stats into actual home and away sides.

    Event types from the client's perspective (``rival_`` prefix)
    are authoritative. The event's ``team`` field is used for unknown types
    and checked for inconsistencies, supporting older exports with stale
    team labels. Historical ``goal_rival`` and ``corner_against`` values are
    normalized to the current rival-prefixed names.
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
        event_type = LEGACY_EVENT_TYPES.get(
            original_event_type,
            original_event_type
        )
        declared_team = event.get("team")

        if event_type in OWN_EVENT_TYPES:
            side = our_venue
            metric = OWN_EVENT_TYPES[event_type]
        elif event_type in OPPONENT_EVENT_TYPES or (
            isinstance(event_type, str) and event_type.startswith("rival_")
        ):
            side = opponent_venue
            metric = OPPONENT_EVENT_TYPES.get(event_type)
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

        if event_type in ("goal_own", "shot_target"):
            team_stats["shots_target"] += 1 if event_type == "goal_own" else 0
        elif event_type in ("rival_goal", "rival_shot_target"):
            team_stats["shots_target"] += 1 if event_type == "rival_goal" else 0

    for side_stats in teams.values():
        side_stats["recoveries"] = sum(
            side_stats[key]
            for key in (
                "recovery_buildout",
                "recovery_build",
                "recovery_finish"
            )
        ) or side_stats["recoveries"]
        side_stats["losses"] = sum(
            side_stats[key]
            for key in ("loss_buildout", "loss_build", "loss_finish")
        ) or side_stats["losses"]

    return {
        **teams,
        "our_venue": our_venue,
        "opponent_venue": opponent_venue,
        "mismatched_team_labels": mismatched_team_labels,
        "unassigned_events": unassigned_events,
        "unknown_event_types": sorted(unknown_event_types)
    }
