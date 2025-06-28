from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Static, Label, Input
from textual import keys
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from secret_manager import SecretManager


class SecretViewScreen(ModalScreen):
    BINDINGS = [
        ("v", "toggle_secret_visibility", "Toggle Secret Visibility"),
        ("escape", "quit_modal", "Close"),
    ]

    SECRET_MASK = "****"

    def __init__(self, secret_details, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.secret_details = secret_details
        self.revealed = False

    def compose(self) -> ComposeResult:
        container_contents = []

        label_value = self.secret_details.get("label")
        if label_value:
            container_contents.append(Label(f"Label: {label_value}"))

        secret_value = self.secret_details.get("secret")
        if secret_value:
            secret_display = secret_value if self.revealed else self.SECRET_MASK
            container_contents.append(
                Label(f"Secret: {secret_display}", id="secret-label")
            )

        attributes = self.secret_details.get("attributes", {})
        if attributes:
            attributes_list = "\n".join(
                [f"- {key}: {value}" for key, value in attributes.items()]
            )
            container_contents.append(Label("Attributes:"))
            container_contents.append(Static(attributes_list))

        yield Vertical(
            *container_contents,
            id="secret-view-container",
            classes="popup-modal",
        )

    def action_toggle_secret_visibility(self) -> None:
        self.revealed = not self.revealed
        secret_label = self.query_one("#secret-label", Label)
        secret_label.update(
            f"Secret: {self.secret_details['secret'] if self.revealed else self.SECRET_MASK}"
        )

    def action_quit_modal(self) -> None:
        self.app.pop_screen()


class SecretTUI(App):
    BINDINGS = [
        ("^q", "quit", "Quit"),
        ("q", "quit", "Quit"),
        ("v", "view_secret", "View Secret"),
        ("enter", "view_secret", "View Secret"),
        ("/", "focus_search", "Search"),
    ]
    CSS = """
    Screen {
        align: center middle;
    }

    #secret-view-container {
        width: 70%;
        height: 10;
        border: thick $accent;
        padding: 1 2;
    }

    #search-input {
        width: 100%;
        margin-bottom: 1;
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.secret_manager = SecretManager()
        self.all_items = self._prepare_items(self.secret_manager.list_keys())
        self.filtered_items_indices = []  # Store indices of currently filtered items

    def _prepare_items(self, items):
        prepared_items = []
        for item in items:
            attributes = item.get_attributes()
            identifier = item.get_label()
            application = attributes.get("application", "")

            if application:
                identifier += (": " if identifier else "") + application

            if not identifier:
                identifier = attributes.get("app_id", "")
            if not identifier:
                identifier = attributes.get("description", "")
            if not identifier:
                identifier = "Unknown Item"

            username = attributes.get("username", "")
            prepared_items.append(
                {"original_item": item, "identifier": identifier, "username": username}
            )
        # Sort prepared_items alphabetically by identifier
        prepared_items.sort(key=lambda x: x["identifier"].lower())
        return prepared_items

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Search...", id="search-input")
        yield Container(DataTable())
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Identifier", "Username")
        self.filter_table("")

    def action_view_secret(self) -> None:
        table = self.query_one(DataTable)
        if table.cursor_row < len(self.filtered_items_indices):
            original_index = self.filtered_items_indices[table.cursor_row]
            original_item = self.all_items[original_index]["original_item"]
            details = self.secret_manager.get_item_details_by_index(original_item)
            if details:
                if not any(
                    isinstance(screen, SecretViewScreen)
                    for screen in self.app.screen_stack
                ):
                    self.push_screen(SecretViewScreen(details))

    def action_focus_search(self) -> None:
        self.query_one("#search-input", Input).focus()

    def on_input_changed(self, event: Input.Changed) -> None:
        self.filter_table(event.value)

    def on_key(self, event: keys.Keys) -> None:
        if self.query_one("#search-input", Input).has_focus and (
            event.key == "escape" or event.key == "down"
        ):
            self.query_one(DataTable).focus()
        elif self.query_one(DataTable).has_focus and event.key == "enter":
            self.action_view_secret()

    def filter_table(self, query: str) -> None:
        table = self.query_one(DataTable)
        table.clear()
        lower_query = query.lower()
        self.filtered_items_indices = []

        for i, item_data in enumerate(self.all_items):
            identifier = item_data["identifier"]
            username = item_data["username"]

            if (
                query == ""
                or lower_query in identifier.lower()
                or lower_query in username.lower()
            ):
                table.add_row(identifier, username)
                self.filtered_items_indices.append(i)


if __name__ == "__main__":
    app = SecretTUI()
    app.run()
