//timeline js

function renderTimeline() {
    const timeline =
        document.getElementById("timeline");
    if (!timeline) return;
    timeline.innerHTML = "";
    const recentEvents =
        [...state.events]
        .sort((a, b) => b.matchSecond - a.matchSecond)
        .slice(0, 10);
    recentEvents.forEach(event => {
        const item =
            createTimelineItem(event);
        timeline.appendChild(item);
    });
}

function createTimelineItem(event) {
    const item =
        document.createElement("div");
    item.className =
        "timeline-item";
    item.textContent =
        buildTimelineText(event);
    return item;
}

function buildTimelineText(event) {
    const teamIcon =
        event.team === "home"
        ? "🟢"
        : "🔴";
    const playerLabel =
        event.dorsal
        ? ` D${event.dorsal}`
        : "";
    return `${event.minute}' ${teamIcon}${playerLabel} ${eventLabel(event.eventType)}`;
}

function addTimelineEvent(event) {
    const timeline =
        document.getElementById("timeline");
    if (!timeline) return;
    const item =
        createTimelineItem(event);
    timeline.prepend(item);
    trimTimeline();
}
function trimTimeline() {
    const timeline =
        document.getElementById("timeline");
    if (!timeline) return;
    const items =
        timeline.querySelectorAll(
            ".timeline-item"
        );
    while (items.length > 10) {
        items[
            items.length - 1
        ].remove();
        return trimTimeline();
    }
}

function clearTimeline() {
    const timeline =
        document.getElementById("timeline");
    if (!timeline) return;
    timeline.innerHTML = "";
}

function buildTimelineText(event) {
    // Cambios
    if (
        event.eventType ===
        "substitution"
    ) {
        return (
            event.minute +
            "' 🔄 " +
            event.playerOutDorsal +
            " → " +
            event.playerInDorsal
        );
    }
    // Eventos normales
    const playerLabel =
        event.dorsal
            ? "D" + event.dorsal
            : "";
    return (
        event.minute +
        "' " +
        playerLabel +
        " " +
        eventLabel(
            event.eventType
        )
    );
}