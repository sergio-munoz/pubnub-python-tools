from ..app.main_app import main as main_app_run
import click


@click.command()
@click.option("--subscribe-key", help="PubNub SubscribeKey")
@click.option("--publish-key", help="PubNub PublishKey.")
def main(subscribe_key, publish_key):
    """Simple program that greets NAME for a total of COUNT times."""
    click.echo(f"SK: {subscribe_key}\nPK: {publish_key}")


if __name__ == '__main__':
    main()
    main_app_run()
