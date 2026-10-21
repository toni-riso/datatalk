// ui.js
//Usado principalmente para colapsar las secciones de datos de partido y de convocatoria

function initializeCollapsibles() {
    const buttons =
        document.querySelectorAll(
            ".collapse-btn"
        );
    buttons.forEach(button => {
        button.addEventListener(
            "click",
            () => {
                const targetId =
                    button.dataset.target;
                const content =
                    document.getElementById(
                        targetId
                    );
                if (!content) return;
                content.classList.toggle(
                    "collapsed"
                );
                const collapsed =
                    content.classList.contains(
                        "collapsed"
                    );
                button.textContent =
                    collapsed
                        ? "▶"
                        : "▼";
          }
        );
    });
}

function collapseSection(contentId, buttonSelector) {
    const content =
        document.getElementById(contentId);
    if (!content) return;
    content.classList.add("collapsed");
    const button =
        document.querySelector(buttonSelector);
    if (button) {
        button.textContent = "▶";
    }
}

function collapseMatchAndSquad() {
    collapseSection(
        "matchContent",
        '.collapse-btn[data-target="matchContent"]'
    );
    collapseSection(
        "squadContent",
        '.collapse-btn[data-target="squadContent"]'
    );
}