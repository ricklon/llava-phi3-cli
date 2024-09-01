# LLaVA-Phi3 CLI

A command-line interface for interacting with the LLaVA-Phi3 vision model.

## Installation

1. Clone this repository
2. Install dependencies: \`poetry install\`

## Usage

Run the CLI with:

\`\`\`
poetry run python llava_phi3_cli/main.py --image path/to/your/image.jpg
\`\`\`

Optional: Specify a custom prompt:

\`\`\`
poetry run python llava_phi3_cli/main.py --image path/to/your/image.jpg --prompt "What objects do you see in this image?"
\`\`\`