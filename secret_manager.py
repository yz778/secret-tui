import keyring
from secretstorage import dbus_init
import secretstorage


class SecretManager:
    def __init__(self):
        self.bus = dbus_init()
        self.keyring = keyring.get_keyring()
        self.items = []

    def list_keys(self):
        collection = secretstorage.get_default_collection(self.bus)
        self.items = list(collection.get_all_items())
        return self.items

    def get_item_details_by_index(self, item):
        secret_bytes = item.get_secret()
        secret_display = "<empty>"
        if secret_bytes:
            try:
                secret_display = secret_bytes.decode("utf-8")
            except UnicodeDecodeError:
                secret_display = f"<binary data: {secret_bytes.hex()}>"
        details = {
            "label": item.get_label(),
            "secret": secret_display,
            "attributes": item.get_attributes(),
        }
        return details
