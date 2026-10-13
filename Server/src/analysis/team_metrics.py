# src/analysis/team_metrics.py

def build_team_stats(events_df):

    passes_ok = len(
        events_df[
            events_df["eventType"] == "pass_ok"
        ]
    )

    passes_bad = len(
        events_df[
            events_df["eventType"] == "pass_bad"
        ]
    )

    recoveries = len(
        events_df[
            events_df["eventType"] == "recovery"
        ]
    )

    losses = len(
        events_df[
            events_df["eventType"] == "loss"
        ]
    )

    total_passes = passes_ok + passes_bad

    pass_accuracy = (
        round(passes_ok / total_passes * 100, 1)
        if total_passes > 0
        else 0
    )

    return {
        "passes_ok": passes_ok,
        "passes_bad": passes_bad,
        "pass_accuracy": pass_accuracy,
        "recoveries": recoveries,
        "losses": losses
    }