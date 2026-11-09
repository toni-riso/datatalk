# src/analysis/team_metrics.py

def build_team_stats(events_df):
    def count(event_type):
        if events_df.empty or "eventType" not in events_df:
            return 0
        return int((events_df["eventType"] == event_type).sum())

    recoveries_by_phase = {
        "recovery_buildout": count("recovery_buildout"),
        "recovery_build": count("recovery_build"),
        "recovery_finish": count("recovery_finish")
    }
    losses_by_phase = {
        "loss_buildout": count("loss_buildout"),
        "loss_build": count("loss_build"),
        "loss_finish": count("loss_finish")
    }
    recoveries = sum(recoveries_by_phase.values())
    losses = sum(losses_by_phase.values())

    if recoveries == 0:
        recoveries = count("recovery")
    if losses == 0:
        losses = count("loss")

    return {
        "buildout_success": count("buildout_success"),
        "buildout_fail": count("buildout_fail"),
        "rival_buildout_success": count("rival_buildout_success"),
        "rival_buildout_fail": count("rival_buildout_fail"),
        **losses_by_phase,
        "dribble_ok": count("dribble_ok"),
        "dribble_bad": count("dribble_bad"),
        "shot_off": count("shot_off"),
        "shot_target": count("shot_target") + count("goal_own"),
        "rival_shot_target": (
            count("rival_shot_target") + count("goal_rival")
        ),
        "goal_own": count("goal_own"),
        "goal_rival": count("goal_rival"),
        **recoveries_by_phase,
        "foul_committed": count("foul_committed"),
        "foul_received": count("foul_received"),
        "yellow": count("yellow"),
        "assist": count("assist"),
        "corner_for": count("corner_for"),
        "corner_against": count("corner_against"),
        "recoveries": recoveries,
        "losses": losses
    }