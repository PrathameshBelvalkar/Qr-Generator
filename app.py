from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageOps
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer,
    CircleModuleDrawer,
    VerticalBarsDrawer,
    RoundedModuleDrawer,
)
from qrcode.image.styles.colormasks import SolidFillColorMask
from io import BytesIO
import requests

app = Flask(__name__)


def hex_to_rgb(hex_color):
    return tuple(int(hex_color.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))


def style_eye(img, inner_color, outer_color, position):
    img_size = img.size[0]
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)

    if position == "top_left":
        draw.rectangle((40, 40, 110, 110), fill=255)
        draw.rectangle((60, 60, 90, 90), fill=0)
    elif position == "top_right":
        draw.rectangle((img_size - 110, 40, img_size - 40, 110), fill=255)
        draw.rectangle((img_size - 90, 60, img_size - 60, 90), fill=0)
    elif position == "bottom_left":
        draw.rectangle((40, img_size - 110, 110, img_size - 40), fill=255)
        draw.rectangle((60, img_size - 90, 90, img_size - 60), fill=0)

    return mask


@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    data = request.json

    # Required fields
    qr_code_text = data.get("qr_code_text", "")
    image_format = data.get("image_format", "PNG").upper()

    # Optional color fields
    background_color = hex_to_rgb(data.get("background_color", "#ffffff"))
    foreground_color = hex_to_rgb(data.get("foreground_color", "#000000"))
    marker_right_inner_color = hex_to_rgb(
        data.get("marker_right_inner_color", "#000000")
    )
    marker_right_outer_color = hex_to_rgb(
        data.get("marker_right_outer_color", "#000000")
    )
    marker_left_inner_color = hex_to_rgb(data.get("marker_left_inner_color", "#000000"))
    marker_left_outer_color = hex_to_rgb(data.get("marker_left_outer_color", "#000000"))
    marker_bottom_inner_color = hex_to_rgb(
        data.get("marker_bottom_inner_color", "#000000")
    )
    marker_bottom_outer_color = hex_to_rgb(
        data.get("marker_bottom_outer_color", "#000000")
    )

    # Optional customization fields
    marker_shape = data.get("marker_shape", "square").lower()
    module_shape = data.get("module_shape", "square").lower()
    logo_image_url = data.get("logo_image_url", "")
    logo_scale = float(data.get("logo_scale", 0.2))
    error_correction_level = data.get("error_correction_level", "H").upper()
    quiet_zone = int(data.get("quiet_zone", 4))
    border = int(data.get("border", 4))
    version = int(data.get("version", 1))
    style = data.get("style", "classic").lower()

    # Adjust shapes based on style
    if style == "rounded":
        module_shape = "rounded"
        marker_shape = "rounded"
    elif style == "thin":
        module_shape = "vertical bars"
        marker_shape = "square"
    elif style == "smooth":
        module_shape = "rounded"
        marker_shape = "square"
    elif style == "circles":
        module_shape = "circle"
        marker_shape = "rounded"

    # Set error correction level
    error_correction_map = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }
    error_correction = error_correction_map.get(
        error_correction_level, qrcode.constants.ERROR_CORRECT_H
    )

    # Create QR code object
    qr = qrcode.QRCode(
        version=version, error_correction=error_correction, box_size=10, border=border
    )
    qr.add_data(qr_code_text)

    # Set module drawer shape
    module_drawer_map = {
        "square": SquareModuleDrawer(),
        "circle": CircleModuleDrawer(),
        "vertical bars": VerticalBarsDrawer(),
        "rounded": RoundedModuleDrawer(),
    }
    module_drawer = module_drawer_map.get(module_shape, SquareModuleDrawer())

    # Generate QR code image
    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=module_drawer,
        color_mask=SolidFillColorMask(
            back_color=background_color, front_color=foreground_color
        ),
    )

    # Apply custom styles to markers (eyes)
    qr_right_inner = qr.make_image(
        image_factory=StyledPilImage,
        eye_drawer=module_drawer_map.get(marker_shape, SquareModuleDrawer()),
        color_mask=SolidFillColorMask(front_color=marker_right_inner_color),
    )
    qr_right_outer = qr.make_image(
        image_factory=StyledPilImage,
        eye_drawer=module_drawer_map.get(marker_shape, SquareModuleDrawer()),
        color_mask=SolidFillColorMask(front_color=marker_right_outer_color),
    )

    qr_left_inner = qr.make_image(
        image_factory=StyledPilImage,
        eye_drawer=module_drawer_map.get(marker_shape, SquareModuleDrawer()),
        color_mask=SolidFillColorMask(front_color=marker_left_inner_color),
    )
    qr_left_outer = qr.make_image(
        image_factory=StyledPilImage,
        eye_drawer=module_drawer_map.get(marker_shape, SquareModuleDrawer()),
        color_mask=SolidFillColorMask(front_color=marker_left_outer_color),
    )

    qr_bottom_inner = qr.make_image(
        image_factory=StyledPilImage,
        eye_drawer=module_drawer_map.get(marker_shape, SquareModuleDrawer()),
        color_mask=SolidFillColorMask(front_color=marker_bottom_inner_color),
    )
    qr_bottom_outer = qr.make_image(
        image_factory=StyledPilImage,
        eye_drawer=module_drawer_map.get(marker_shape, SquareModuleDrawer()),
        color_mask=SolidFillColorMask(front_color=marker_bottom_outer_color),
    )

    right_inner_mask = style_eye(
        qr_img, marker_right_inner_color, marker_right_outer_color, "top_right"
    )
    right_outer_mask = style_eye(
        qr_img, marker_right_outer_color, marker_right_inner_color, "top_right"
    )
    left_inner_mask = style_eye(
        qr_img, marker_left_inner_color, marker_left_outer_color, "top_left"
    )
    left_outer_mask = style_eye(
        qr_img, marker_left_outer_color, marker_left_inner_color, "top_left"
    )
    bottom_inner_mask = style_eye(
        qr_img, marker_bottom_inner_color, marker_bottom_outer_color, "bottom_left"
    )
    bottom_outer_mask = style_eye(
        qr_img, marker_bottom_outer_color, marker_bottom_inner_color, "bottom_left"
    )

    intermediate_img = Image.composite(qr_right_inner, qr_img, right_inner_mask)
    intermediate_img = Image.composite(
        qr_right_outer, intermediate_img, right_outer_mask
    )
    intermediate_img = Image.composite(qr_left_inner, intermediate_img, left_inner_mask)
    intermediate_img = Image.composite(qr_left_outer, intermediate_img, left_outer_mask)
    final_image = Image.composite(qr_bottom_inner, intermediate_img, bottom_inner_mask)
    final_image = Image.composite(qr_bottom_outer, final_image, bottom_outer_mask)

    # Add logo if provided
    if logo_image_url:
        response = requests.get(logo_image_url)
        logo = Image.open(BytesIO(response.content)).convert("RGBA")

        # Ensure logo is high resolution
        logo = logo.resize((logo.width * 2, logo.height * 2), Image.LANCZOS)

        # Resize logo according to logo_scale
        logo_size = int(min(final_image.size) * logo_scale)
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

        # Add white background with 50% border radius
        logo_bg_size = logo_size + int(logo_size * 0.2)
        logo_bg = Image.new("RGBA", (logo_bg_size, logo_bg_size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(logo_bg)
        draw.ellipse((0, 0, logo_bg_size, logo_bg_size), fill=(255, 255, 255, 255))

        # Center the logo within the white background
        logo_position = (
            (logo_bg_size - logo_size) // 2,
            (logo_bg_size - logo_size) // 2,
        )
        logo_bg.paste(logo, logo_position, logo)

        # Calculate position to center the logo with right padding
        final_logo_position = (
            (final_image.size[0] - logo_bg_size) // 2
            + int(logo_bg_size * 0.1),  # Add padding to the right
            (final_image.size[1] - logo_bg_size) // 2,
        )

        # Paste the logo with white background onto the QR code
        final_image.paste(logo_bg, final_logo_position, logo_bg)

    # Save the final image to a BytesIO object
    img_io = BytesIO()
    final_image.save(img_io, image_format)
    img_io.seek(0)

    # Return the image as a response
    return send_file(img_io, mimetype=f"image/{image_format.lower()}")


if __name__ == "__main__":
    app.run(debug=True)
