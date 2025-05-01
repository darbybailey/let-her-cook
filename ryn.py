from tracker.logic.logger import log_new_project

if __name__ == "__main__":
    # Example project input — this will later be automated
    log_new_project(
        name="kanban-scribe",
        url="https://github.com/darbybailey/kanban-scribe",
        visibility="public",
        status="scaffolded"
    )
