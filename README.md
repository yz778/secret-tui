# SecretTUI

SecretTUI is a Terminal User Interface (TUI) application built with Textual that allows you to view and manage secrets stored in your system's keyring. It provides a convenient way to browse your stored credentials directly from your terminal.

This is a vibe coding experiment using [Goose](https://block.github.io/goose/) and [KiloCode](https://kilocode.ai) with [Gemini 2.5 Flash](https://aistudio.google.com/prompts/new_chat?model=gemini-2.5-flash).

## Features

*   **List Secrets**: Displays a list of all secrets accessible via the system's keyring.
*   **Search Functionality**: Filter secrets by identifier (label, description, application, app_id) or username using a search input.
*   **View Secret Details**: Select a secret from the list to view its full label, the secret content, and associated attributes in a modal popup.
*   **Keyboard Navigation**: Navigate the TUI using keyboard shortcuts for efficient interaction.

## Installation

To run SecretTUI, you need Python installed on your system. It also relies on `keyring` and `secretstorage` for interacting with the system's secret service, and `textual` for the TUI.

1.  **Clone the repository (if applicable):**
    ```bash
    git clone https://github.com/yz778/secret-tui.git
    cd secret-tui
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

## Usage

To start the application, run the `main.py` script:

```bash
python main.py
```

### Key Bindings

*   `q` or `^q` (Ctrl+Q): Quit the application.
*   `/`: Search secrets.
*   `v`: View details and toggle secret reveal.

## How it Works

SecretTUI uses the `keyring` library to interface with the operating system's secret service (e.g., GNOME Keyring, macOS Keychain, Windows Credential Manager). It retrieves a list of available secret items and allows the user to view their details, including the secret content itself and any associated attributes. The `textual` framework is used to render the interactive terminal interface.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.