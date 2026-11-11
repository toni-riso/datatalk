EVENT_ALIASES = {
    "own_goal": "goal_own",
    "goal_rival": "rival_goal",
    "corner_against": "rival_corner"
}

PHASE_GROUPS = {
    "recoveries": {
        "title": "Recuperaciones",
        "phases": (
            ("recovery_buildout", "recovery_buildout", "Salida"),
            ("recovery_build", "recovery_build", "Construcción"),
            ("recovery_finish", "recovery_finish", "Finalización"),
            ("recovery", "recovery_unspecified", "Sin especificar")
        )
    },
    "losses": {
        "title": "Pérdidas",
        "phases": (
            ("loss_buildout", "loss_buildout", "Salida"),
            ("loss_build", "loss_build", "Construcción"),
            ("loss_finish", "loss_finish", "Finalización"),
            ("loss", "loss_unspecified", "Sin especificar")
        )
    }
}

EVENT_DEFINITIONS = {
    "buildout_success": {
        "team_side": "own",
        "team_metric": "buildout_success",
        "team_detail": ("buildouts", "Salida exitosa"),
        "player_label": "Salida exitosa"
    },
    "buildout_fail": {
        "team_side": "own",
        "team_metric": "buildout_fail",
        "team_detail": ("buildouts", "Salida fallida"),
        "player_label": "Salida fallida"
    },
    "dribble_ok": {
        "team_side": "own",
        "team_metric": "dribble_ok",
        "player_label": "Regate completado",
        "player_metrics": ("dribbles_ok",)
    },
    "dribble_bad": {
        "team_side": "own",
        "team_metric": "dribble_bad",
        "player_label": "Regate fallido",
        "player_metrics": ("dribbles_bad",)
    },
    "shot_off": {
        "team_side": "own",
        "team_metric": "shots_off",
        "team_detail": ("shots", "Tiro fuera"),
        "player_label": "Tiro fuera",
        "player_metrics": ("shots_off_target",)
    },
    "shot_target": {
        "team_side": "own",
        "team_metric": "shots_target",
        "team_detail": ("shots", "Tiro a puerta"),
        "player_label": "Tiro a puerta",
        "player_metrics": ("shots_target",)
    },
    "goal_own": {
        "team_side": "own",
        "team_metric": "goals",
        "team_detail": ("shots", "Gol"),
        "player_label": "Gol",
        "player_metrics": ("goals", "shots_target"),
        "team_bonus_metrics": ("shots_target",),
        "timeline": ("⚽ Gol", "Nuestro equipo")
    },
    "assist": {
        "team_side": "own",
        "team_metric": "assists",
        "player_label": "Asistencia",
        "player_metrics": ("assists",),
        "timeline": ("🅰️ Asistencia", "Nuestro equipo")
    },
    "foul_committed": {
        "team_side": "own",
        "team_metric": "fouls_committed",
        "player_label": "Falta cometida",
        "player_metrics": ("fouls_committed",)
    },
    "foul_received": {
        "team_side": "own",
        "team_metric": "fouls_received",
        "player_label": "Falta recibida",
        "player_metrics": ("fouls_received",)
    },
    "yellow": {
        "team_side": "own",
        "team_metric": "yellow",
        "player_label": "Tarjeta amarilla",
        "player_metrics": ("yellow_cards",),
        "timeline": ("🟨 Tarjeta amarilla", "Nuestro equipo")
    },
    "corner_for": {
        "team_side": "own",
        "team_metric": "corners_for",
        "timeline": ("🚩 Córner a favor", "Nuestro equipo")
    },
    "rival_buildout_success": {
        "team_side": "opponent",
        "team_metric": "buildout_success",
        "team_detail": ("buildouts", "Salida exitosa")
    },
    "rival_buildout_fail": {
        "team_side": "opponent",
        "team_metric": "buildout_fail",
        "team_detail": ("buildouts", "Salida fallida")
    },
    "rival_shot_off": {
        "team_side": "opponent",
        "team_metric": "shots_off",
        "team_detail": ("shots", "Tiro fuera"),
        "timeline": ("Tiro fuera", "Rival")
    },
    "rival_shot_target": {
        "team_side": "opponent",
        "team_metric": "shots_target",
        "team_detail": ("shots", "Tiro a puerta"),
        "timeline": ("🎯 Tiro a puerta", "Rival")
    },
    "rival_goal": {
        "team_side": "opponent",
        "team_metric": "goals",
        "team_detail": ("shots", "Gol"),
        "team_bonus_metrics": ("shots_target",),
        "timeline": ("⚽ Gol rival", "Rival")
    },
    "rival_corner": {
        "team_side": "opponent",
        "team_metric": "corners_for",
        "timeline": ("🚩 Córner en contra", "Rival")
    },
    "rival_yellow": {
        "team_side": "opponent",
        "timeline": ("🟨 Tarjeta amarilla", "Rival")
    },
    "substitution": {
        "team_side": "own",
        "timeline": ("🔄 Cambio", "Nuestro equipo")
    },
    "shot": {
        "player_label": "Tiro",
        "player_metrics": ("legacy_shots",)
    }
}

for group_name, group in PHASE_GROUPS.items():
    for event_type, metric, label in group["phases"]:
        is_recovery = group_name == "recoveries"
        event_label = (
            f"Recuperación · {label}"
            if is_recovery
            else f"Pérdida · {label}"
        )
        EVENT_DEFINITIONS[event_type] = {
            "team_side": "own",
            "team_metric": metric,
            "player_label": event_label
        }
        if is_recovery:
            EVENT_DEFINITIONS[event_type]["team_detail"] = (
                "recoveries",
                event_label
            )

PLAYER_EVENT_LABELS = {
    event_type: definition["player_label"]
    for event_type, definition in EVENT_DEFINITIONS.items()
    if "player_label" in definition
}

PLAYER_METRIC_EVENT_TYPES = {}
for event_type, definition in EVENT_DEFINITIONS.items():
    for metric in definition.get("player_metrics", ()):
        PLAYER_METRIC_EVENT_TYPES.setdefault(metric, []).append(event_type)
PLAYER_METRIC_EVENT_TYPES = {
    metric: tuple(event_types)
    for metric, event_types in PLAYER_METRIC_EVENT_TYPES.items()
}

OWN_EVENT_TYPES = {
    event_type: definition.get("team_metric")
    for event_type, definition in EVENT_DEFINITIONS.items()
    if definition.get("team_side") == "own"
}
OPPONENT_EVENT_TYPES = {
    event_type: definition.get("team_metric")
    for event_type, definition in EVENT_DEFINITIONS.items()
    if definition.get("team_side") == "opponent"
}
TEAM_EVENT_DETAILS = {
    event_type: (
        definition["team_side"],
        definition["team_detail"][0],
        definition["team_detail"][1]
    )
    for event_type, definition in EVENT_DEFINITIONS.items()
    if "team_detail" in definition
}
TEAM_METRIC_KEYS = tuple(dict.fromkeys(
    definition["team_metric"]
    for definition in EVENT_DEFINITIONS.values()
    if definition.get("team_metric") is not None
))
TEAM_BONUS_METRICS = {
    event_type: definition["team_bonus_metrics"]
    for event_type, definition in EVENT_DEFINITIONS.items()
    if "team_bonus_metrics" in definition
}
TIMELINE_EVENTS = {
    event_type: definition["timeline"]
    for event_type, definition in EVENT_DEFINITIONS.items()
    if "timeline" in definition
}
SEASON_EVENT_CATEGORIES = {
    "Goles": {
        "labels": ("Goles a favor", "Goles en contra"),
        "keys": ("goals_for", "goals_against")
    },
    "Tiros": {
        "labels": ("Tiros a puerta", "Tiros fuera"),
        "keys": ("shots_target", "shots_off")
    },
    "Salidas": {
        "labels": ("Exitosas", "Fallidas"),
        "keys": ("buildout_success", "buildout_fail")
    },
    "Recuperaciones": {
        "labels": tuple(
            phase[2] for phase in PHASE_GROUPS["recoveries"]["phases"]
        ),
        "keys": tuple(
            phase[1] for phase in PHASE_GROUPS["recoveries"]["phases"]
        )
    },
    "Pérdidas": {
        "labels": tuple(
            phase[2] for phase in PHASE_GROUPS["losses"]["phases"]
        ),
        "keys": tuple(
            phase[1] for phase in PHASE_GROUPS["losses"]["phases"]
        )
    },
    "Faltas": {
        "labels": ("Cometidas", "Recibidas"),
        "keys": ("fouls_committed", "fouls_received")
    }
}

def _detail_label(event_type):
    return EVENT_DEFINITIONS[event_type]["team_detail"][1]


TEAM_EVENT_CHARTS = {
    "shots": {
        "labels": ("A puerta (incl. goles)", "Fuera"),
        "count_groups": tuple(
            tuple(_detail_label(event_type) for event_type in group)
            for group in (
                ("shot_target", "goal_own"),
                ("shot_off",)
            )
        )
    },
    "buildouts": {
        "labels": ("Exitosas", "Fallidas"),
        "count_groups": tuple(
            (_detail_label(event_type),)
            for event_type in ("buildout_success", "buildout_fail")
        )
    },
    "recoveries": {
        "labels": tuple(
            phase[2] for phase in PHASE_GROUPS["recoveries"]["phases"]
        ),
        "count_groups": tuple(
            (_detail_label(phase[0]),)
            for phase in PHASE_GROUPS["recoveries"]["phases"]
        )
    }
}

PLAYER_EVENT_CHARTS = {
    "shots": ("A puerta", "Fuera"),
    "dribbles": ("Completados", "Fallidos")
}


def canonical_event_type(event_type):
    """Return the current event name for a known historical alias."""
    return EVENT_ALIASES.get(event_type, event_type)


def phase_event_types(group):
    """Return event names for the ordered phases in a recovery/loss group."""
    return tuple(
        phase[0]
        for phase in PHASE_GROUPS[group]["phases"]
    )


def phase_metric_keys(group):
    """Return aggregate metric keys for the ordered phases in a group."""
    return tuple(
        phase[1]
        for phase in PHASE_GROUPS[group]["phases"]
    )


def phase_labels(group):
    """Return display labels for the ordered phases in a group."""
    return tuple(
        phase[2]
        for phase in PHASE_GROUPS[group]["phases"]
    )
