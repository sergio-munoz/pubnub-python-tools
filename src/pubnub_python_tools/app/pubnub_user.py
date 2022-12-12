"""SRP PubNub User to interact with PubNub Web Console."""

from . import pubnub_internal_rest_api as api


class PubNubUser:
    """PubNub User Class"""

    def __init__(self):
        """Initialize PubNubUser class."""
        self.user = None
        self.token = None
        self.isLogin = False
        self.accounts = []
        self.apps = {}

    def __repr__(self) -> str:
        """Return string representation of PubNubUser class."""
        if not self.isLogin:
            return "PubNubUser is not logged in."
        msg = ""
        if self.token:
            msg += f"PubNub User id: {self.user}"
        if self.accounts:
            msg += f"\tPubNub User accounts: {self.accounts}"
        if self.apps:
            msg += f"\tPubNub User apps: {self.apps}"
        return msg

    def login(self, email, password):
        try:
            self.user, self.token = api.authenticate(email, password)
            self.isLogin = True
        except Exception as error:
            print(error)
        return self.isLogin

    def load(self):
        """Load user accounts."""
        if not self.isLogin:
            print("User not login")
            return False
        try:
            accounts = api.get_accounts(self.user, self.token)
            self.accounts = api.get_accounts_ids(accounts)

            for account in self.accounts:
                apps = api.get_apps(account, self.token)
                self.apps.update({account: api.get_apps_ids(apps)})
        except Exception as error:
            print(error)
            return False
        return True

    def all_metrics(self):
        metrics = []
        try:
            for _, app_ids in self.apps.items():
                for app_id in app_ids:
                    metrics.append(
                        api.get_app_based_usage(app_id, self.token, "transaction", "2022-12-01", "2022-12-02")
                        )
        except Exception as error:
            print(error)
            return None
        return metrics
