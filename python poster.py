from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

# --- CONFIG ---
poster_width, poster_height = 800, 1000
main_slogan = "Code. Compete. Conquer!"  # Main slogan for CS4 Intramurals
extra_slogans = [
    "Where Logic Meets Legacy!",
    "Debugging the Competition!",
    "Hack the Game, Win the Glory!"
]
accent_color = (255, 215, 0)  # Gold
glow_color = (255, 20, 147, 120)  # Neon pink glow with transparency
background_top = (15, 15, 20)     # Very dark gray/black
background_bottom = (180, 30, 90) # Pinkish-magenta

# --- CREATE BASE IMAGE (Gradient Background to match logo) ---
poster = Image.new("RGB", (poster_width, poster_height), background_top)
draw = ImageDraw.Draw(poster)

for y in range(poster_height):
    r = int(background_top[0] + (background_bottom[0] - background_top[0]) * (y/poster_height))
    g = int(background_top[1] + (background_bottom[1] - background_top[1]) * (y/poster_height))
    b = int(background_top[2] + (background_bottom[2] - background_top[2]) * (y/poster_height))
    draw.line([(0, y), (poster_width, y)], fill=(r, g, b))

# --- LOAD FONTS ---
try:
    slogan_font = ImageFont.truetype("arialbd.ttf", 50)  # Main slogan
    extra_font = ImageFont.truetype("arial.ttf", 42)     # Extra slogans
    footer_font = ImageFont.truetype("arial.ttf", 30)    # Footer
except:
    slogan_font = ImageFont.load_default()
    extra_font = ImageFont.load_default()
    footer_font = ImageFont.load_default()

# --- BORDER ---
draw.rectangle([0, 0, poster_width-1, poster_height-1], outline=(255, 255, 255), width=10)

# --- HELPER FUNCTION: Centered Text ---
def draw_centered_text(draw, text, y, font, fill="white", bg=None, pad=20):
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (poster_width - w) // 2
    if bg:  # optional background box
        draw.rectangle([x-pad, y-10, x+w+pad, y+h+10], fill=bg)
    draw.text((x, y), text, font=font, fill=fill)
    return h

# --- IMAGE (Mascot/Logo with Shadow + Glow) ---
y = 60
try:
    mascot = Image.open("CCIS.png").convert("RGBA")
    mascot.thumbnail((700, 700))  # ⬅️ Bigger logo here
    mx, my = mascot.size
    pos_x = (poster_width - mx) // 2
    pos_y = y

    # Shadow
    shadow = Image.new("RGBA", poster.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rectangle([pos_x+10, pos_y+10, pos_x+mx+10, pos_y+my+10], fill=(0, 0, 0, 180))
    shadow = shadow.filter(ImageFilter.GaussianBlur(20))

    # Glow
    glow = Image.new("RGBA", poster.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.rectangle([pos_x-15, pos_y-15, pos_x+mx+15, pos_y+my+15], fill=glow_color)
    glow = glow.filter(ImageFilter.GaussianBlur(40))

    # Composite
    poster = Image.alpha_composite(poster.convert("RGBA"), shadow)
    poster = Image.alpha_composite(poster, glow)

    # Paste mascot
    poster.paste(mascot, (pos_x, pos_y), mascot)

    y = pos_y + my + 50
except FileNotFoundError:
    print("Mascot/logo file not found! Make sure CCIS.png is in the folder.")
    y += 300

# --- MAIN SLOGAN ---
draw = ImageDraw.Draw(poster)
y += draw_centered_text(draw, main_slogan, y, slogan_font, fill="black", bg=accent_color)

# --- EXTRA SLOGANS ---
y += 50
for slogan in extra_slogans:
    y += draw_centered_text(draw, slogan, y, extra_font)
    y += 20

# --- SAVE POSTER ---
poster = poster.convert("RGB")
poster.save("ProfElec2_ToledoThea_Activity1.png")
poster.show()
