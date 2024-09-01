import click
import ollama
import os
import sys
import logging
from PIL import Image

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB

def validate_image(image_path):
    if not os.path.exists(image_path):
        raise click.BadParameter(f"Image file does not exist: {image_path}")
    
    if os.path.getsize(image_path) > MAX_IMAGE_SIZE:
        logger.warning(f"Image file is larger than 10MB. This may cause performance issues.")
    
    try:
        with Image.open(image_path) as img:
            img.verify()
    except Exception as e:
        raise click.BadParameter(f"Invalid or corrupted image file: {e}")

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--image', type=click.Path(exists=True), help='Path to the image file')
@click.option('--prompt', default='Describe this image:', help='Prompt for the model')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
@click.pass_context
def analyze_image(ctx, image, prompt, verbose):
    """Analyze an image using the llava-phi3 model.

    Example usage:
    python main.py --image path/to/your/image.jpg --prompt "What objects are in this image?"
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    if not image:
        click.echo(ctx.get_help())
        ctx.exit()

    try:
        validate_image(image)
        
        logger.debug(f"Reading image file: {image}")
        with open(image, 'rb') as image_file:
            image_content = image_file.read()

        logger.debug("Sending request to Ollama service")
        response = ollama.chat(
            model='llava-phi3',
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                    'images': [image_content]
                }
            ]
        )
        click.echo(response['message']['content'])

    except click.BadParameter as e:
        logger.error(f"Input error: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except ollama.ResponseError as e:
        logger.error(f"Ollama service error: {e.error}")
        if e.status_code == 404:
            click.echo("Error: Model 'llava-phi3' not found. Try pulling the model first:", err=True)
            click.echo("  ollama pull llava-phi3", err=True)
        else:
            click.echo(f"Error communicating with Ollama service: {e.error}", err=True)
        sys.exit(1)
    except ollama.RequestError as e:
        logger.error(f"Network error: {e}")
        click.echo(f"Error connecting to Ollama service. Please check your network connection and ensure the service is running.", err=True)
        sys.exit(1)
    except IOError as e:
        logger.error(f"I/O error: {e}")
        click.echo(f"Error reading image file: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        click.echo(f"An unexpected error occurred: {e}", err=True)
        if verbose:
            click.echo("For more information, run the command with the --verbose flag.", err=True)
        sys.exit(1)

if __name__ == '__main__':
    analyze_image()