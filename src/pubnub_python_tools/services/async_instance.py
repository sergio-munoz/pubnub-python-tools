import click
from ..config import module_config
from ..app import pubnub_manager_asyncio


class AsyncInstance:
    def __init__(self, subscribe_key=None, publish_key=None, user_id=None):
        self.subscribe_key = module_config.SUBSCRIBE_KEY
        if subscribe_key:
            self.subscribe_key = subscribe_key
        self.publish_key = module_config.PUBLISH_KEY
        if publish_key:
            self.publish_key = publish_key
        self.user_id = module_config.USER_ID
        if user_id:
            self.user_id = user_id
        self.pnmg = pubnub_manager_asyncio.PubNubAsyncioManager(
            self.subscribe_key, self.publish_key, self.user_id
        )

    def get(self):
        return self.pnmg

    @click.option('--publish', help="Channel to publish.")
    @click.option('--message', help="Message to publish.")
    def publish(self, publish, message):
        envelope = self.pnmg.publish(publish, message)
        res = str(envelope.result)
        click.echo(res)

    @click.option('--subscribe', help="Subscribe to a channel")
    def subscribe(self, subscribe):
        res = self.pnmg.subscribe(subscribe)
        click.echo(res)
