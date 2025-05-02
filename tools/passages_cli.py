import click
from extract_phrase import passage_to_json

@click.command()
@click.option('--raw', required=True, help='File txt')
@click.option('--lang', default="en-vi", help='Language code, e.g., en-vi or en-jp')
def cli(raw, lang):
    passage_to_json(raw, lang)

if __name__ == '__main__':
    cli()