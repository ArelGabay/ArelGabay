import requests
from flask import Flask, send_file, make_response
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

API_KEY = os.getenv("API_NINJAS_API_KEY")  # Set this in your environment or deployment

@app.route('/fun-fact.png')
def generate_fun_fact_image():
    # Fetch a random fact from API Ninjas
    response = requests.get(
        'https://api.api-ninjas.com/v1/facts',
        headers={'X-Api-Key': API_KEY}
    )
    fact = response.json()[0]['fact']

    # Create an image
    width, height = 800, 200
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Use a font
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    # Wrap text if it's too long
    def wrap_text(text, font, max_width):
        lines = []
        words = text.split()
        line = ''
        for word in words:
            test_line = f"{line} {word}".strip()
            if draw.textlength(test_line, font=font) <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        lines.append(line)
        return lines

    lines = wrap_text(fact, font, width - 40)
    y = 20
    for line in lines:
        draw.text((20, y), line, fill=(0, 0, 0), font=font)
        y += 30

    # Save image to memory
    img_io = BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)

    # Return image with no caching
    response = make_response(send_file(img_io, mimetype='image/png'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

if __name__ == "__main__":
    app.run(debug=True)
