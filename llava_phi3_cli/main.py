import click
import ollama

@click.command()
@click.option('--image', type=click.Path(exists=True), help='Path to the image file')
@click.option('--prompt', default='Describe this image:', help='Prompt for the model')
def analyze_image(image, prompt):
    """Analyze an image using the llava-phi3 model."""
    try:
        response = ollama.chat(
            model='llava-phi3',
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                    'images': [image]
                }
            ]
        )
        click.echo(response['message']['content'])
    except ollama.ResponseError as e:
        click.echo(f"Error: {e.error}", err=True)
        if e.status_code == 404:
            click.echo("Model not found. Try pulling the model first.", err=True)

if __name__ == '__main__':
    analyze_image()