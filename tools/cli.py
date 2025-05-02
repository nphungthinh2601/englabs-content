import click
from extract_phrase import translate_extract_phrase

@click.command()
@click.option('--raw', required=True, help='Input string for phrase extraction')
def cli(raw):
    result = translate_extract_phrase(raw)
    print(result)

if __name__ == '__main__':
    cli()