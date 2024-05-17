import pygame
import sys
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BUTTON_RADIUS = 50
TEXT_COLOR = (0, 0, 0)  # Black
FONT_SIZE = 48
SMALL_FONT_SIZE = 24
TITLE_FONT_SIZE = 30
INPUT_BOX_COLOR = (200, 200, 200)  # Light grey
ACTIVE_BOX_COLOR = (255, 255, 255)  # White
BLUE_CIRCLE_COLOR = (0, 0, 255)  # Blue
PURPLE_CIRCLE_COLOR = (128, 0, 128)  # Purple
BACKGROUND_GRADIENT_START = (169, 169, 169)  # Light grey
BACKGROUND_GRADIENT_END = (50, 50, 50)  # Dark grey

GRADIENT_COLORS = {
    "Tile": [(0, 255, 0), (0, 128, 255)],  # Green to Blue
    "Item": [(0, 255, 0), (0, 128, 255)],  # Green to Blue
    "NPC": [(0, 255, 0), (0, 128, 255)],  # Green to Blue
    "Settings": [(0, 128, 255), (0, 255, 0)],  # Blue to Green
    "Option": [(128, 0, 128), (75, 0, 130)],  # Purple to Dark Purple
    "Export": [(0, 128, 255), (0, 255, 0)]  # Blue to Green for Export button
}

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Terraria Mod Maker")

# Load font
font = pygame.font.SysFont("Comic Sans MS", FONT_SIZE)
small_font = pygame.font.SysFont("Comic Sans MS", SMALL_FONT_SIZE)
title_font = pygame.font.SysFont("Comic Sans MS", TITLE_FONT_SIZE)

# Settings
npc_option = True
export_folder = os.getcwd()

# Button positions
main_buttons = {
    "Tile": (100, 100),
    "Item": (100, 200),
    "NPC": (100, 300),
    "Settings": (WIDTH - 100, HEIGHT // 2)
}
export_button_position = (WIDTH - 100, HEIGHT // 2)

# Title text position
title_text_position = (WIDTH - 150, 50)
title_text_rect = pygame.Rect(WIDTH - 250, 25, 200, 50)  # Define the clickable area around the title text

def draw_gradient_circle(screen, text, position, colors):
    gradient_surf = pygame.Surface((BUTTON_RADIUS * 2, BUTTON_RADIUS * 2), pygame.SRCALPHA)
    for x in range(BUTTON_RADIUS * 2):
        color = [
            int(colors[0][i] + (colors[1][i] - colors[0][i]) * (x / (BUTTON_RADIUS * 2)))
            for i in range(3)
        ]
        pygame.draw.line(gradient_surf, color, (0, x), (BUTTON_RADIUS * 2, x))
    gradient_surf = pygame.transform.rotate(gradient_surf, 270)  # Rotate gradient 90 degrees to the left
    mask = pygame.Surface((BUTTON_RADIUS * 2, BUTTON_RADIUS * 2), pygame.SRCALPHA)
    pygame.draw.circle(mask, (255, 255, 255), (BUTTON_RADIUS, BUTTON_RADIUS), BUTTON_RADIUS)
    gradient_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    screen.blit(gradient_surf, (position[0] - BUTTON_RADIUS, position[1] - BUTTON_RADIUS))
    text_surface = small_font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

def draw_text(screen, text, position, font):
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

def draw_input_box(screen, rect, text, active):
    color = ACTIVE_BOX_COLOR if active else INPUT_BOX_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=5)
    text_surface = small_font.render(text, True, TEXT_COLOR)
    screen.blit(text_surface, (rect.x + 5, rect.y + 5))

def generate_tile_file(name, resistance, dust_id, min_pick, mod_name):
    content = f"""using ExampleMod.Dusts;
using Microsoft.Xna.Framework;
using Terraria;
using Terraria.ID;
using Terraria.ModLoader;

namespace {mod_name}
{{
    public class {name} : ModTile
    {{
        public override void SetStaticDefaults()
        {{
            Main.tileSolid[Type] = true; // will work on this later
            Main.tileMergeDirt[Type] = false; // will work on this later
            Main.tileBlockLight[Type] = false; // will work on this later
            Main.tileLighted[Type] = true; // will work on this later
            DustType = DustID.{dust_id};
            AddMapEntry(new Color(200, 200, 200)); // will work on this later

            MineResist = {resistance}f;
            MinPick = {min_pick};
        }}
    }}
}}"""
    filename = os.path.join(export_folder, f"{name}.cs")
    with open(filename, "w") as file:
        file.write(content)
    print(f"{filename} generated!")

def generate_item_file(name, mod_name, width, height, max_stack, value, rarity):
    content = f"""using Terraria;
using Terraria.ID;
using Terraria.ModLoader;

namespace {mod_name}
{{
    public class {name} : ModItem
    {{
        public override void SetDefaults()
        {{
            Item.width = {width};
            Item.height = {height};
            Item.maxStack = {max_stack};
            Item.value = {value};
            Item.rare = ItemRarityID.{rarity};
            // Set other Item.X values here
        }}

        public override void AddRecipes()
        {{
            // Type in recipes by yourself!
        }}
    }}
}}"""
    filename = os.path.join(export_folder, f"{name}.cs")
    with open(filename, "w") as file:
        file.write(content)
    print(f"{filename} generated!")

def select_export_folder():
    global export_folder
    root = Tk()
    root.withdraw()
    export_folder = askdirectory(initialdir=export_folder)
    print(f"Export folder set to: {export_folder}")

def draw_background_gradient(screen, start_color, end_color):
    gradient_surf = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        color = [
            int(start_color[i] + (end_color[i] - start_color[i]) * (y / HEIGHT))
            for i in range(3)
        ]
        pygame.draw.line(gradient_surf, color, (0, y), (WIDTH, y))
    screen.blit(gradient_surf, (0, 0))

def main_menu():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if title_text_rect.collidepoint(mouse_pos):
                    continue  # Prevent clicking the title text area from doing anything in the main menu
                for button, position in main_buttons.items():
                    if (mouse_pos[0] - position[0]) ** 2 + (mouse_pos[1] - position[1]) ** 2 <= BUTTON_RADIUS ** 2:
                        if button == "Tile":
                            tile_menu()
                        elif button == "Item":
                            item_menu()
                        elif button == "NPC" and npc_option:
                            npc_menu()
                        elif button == "Settings":
                            settings_menu()

        # Clear screen
        draw_background_gradient(screen, BACKGROUND_GRADIENT_START, BACKGROUND_GRADIENT_END)

        # Draw buttons
        for button, position in main_buttons.items():
            if button == "NPC" and not npc_option:
                continue
            draw_gradient_circle(screen, button, position, GRADIENT_COLORS[button])

        # Draw title and instruction
        draw_text(screen, "Terraria Mod Maker", title_text_position, title_font)
        draw_text(screen, "Click a button to start!", (WIDTH // 2, HEIGHT - 50), small_font)

        # Update display
        pygame.display.flip()

def handle_text_input(event, active_box, inputs):
    if event.key == pygame.K_RETURN:
        return
    elif event.key == pygame.K_BACKSPACE:
        inputs[active_box] = inputs[active_box][:-1]
    else:
        inputs[active_box] += event.unicode

def tile_menu():
    input_boxes = [
        pygame.Rect(250, 100, 300, 30),
        pygame.Rect(250, 150, 300, 30),
        pygame.Rect(250, 200, 300, 30),
        pygame.Rect(250, 250, 300, 30),
        pygame.Rect(250, 300, 300, 30)  # New input box for MinPick
    ]
    placeholder_texts = [
        "Type resistance here! 0.5-5",
        "Type name here! (no spaces)",
        "Type name here! (spaces)",
        "Type DustID here!",
        "Type MinPick here!"
    ]
    inputs = ["", "", "", "", ""]
    active_box = None
    text_rects = [pygame.Rect(box.x + 5, box.y + 5, box.width - 10, box.height - 10) for box in input_boxes]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if title_text_rect.collidepoint(mouse_pos):
                    return
                for idx, rect in enumerate(text_rects):
                    if rect.collidepoint(mouse_pos):
                        active_box = idx
                    else:
                        if idx == active_box:
                            active_box = None
                if (mouse_pos[0] - export_button_position[0]) ** 2 + (mouse_pos[1] - export_button_position[1]) ** 2 <= BUTTON_RADIUS ** 2:
                    if all(inputs):
                        generate_tile_file(inputs[1], inputs[0], inputs[3], inputs[4], "ChangeThisToModName")
            elif event.type == pygame.KEYDOWN and active_box is not None:
                handle_text_input(event, active_box, inputs)

        # Clear screen
        draw_background_gradient(screen, BACKGROUND_GRADIENT_START, BACKGROUND_GRADIENT_END)

        # Draw circle and text
        draw_gradient_circle(screen, "Tile", (100, HEIGHT // 2), [BLUE_CIRCLE_COLOR, (0, 0, 128)])
        draw_text(screen, "Terraria Mod Maker", title_text_position, title_font)

        # Draw input boxes
        for idx, box in enumerate(input_boxes):
            draw_input_box(screen, box, inputs[idx] if inputs[idx] else placeholder_texts[idx], active_box == idx)

        # Draw export button
        draw_gradient_circle(screen, "Export", export_button_position, GRADIENT_COLORS["Export"])

        # Update display
        pygame.display.flip()

def item_menu():
    input_boxes = [
        pygame.Rect(250, 100, 300, 30),
        pygame.Rect(250, 150, 300, 30),
        pygame.Rect(250, 200, 300, 30),
        pygame.Rect(250, 250, 300, 30),
        pygame.Rect(250, 300, 300, 30),  # New input box for Image X
        pygame.Rect(250, 350, 300, 30),  # New input box for Image Y
        pygame.Rect(250, 400, 300, 30)   # New input box for Rarity
    ]
    placeholder_texts = [
        "Type damage here!",
        "Type name here! (no spaces)",
        "Type name here! (spaces)",
        "Type ProjectileID here!",
        "Type Image X here!",
        "Type Image Y here!",
        "Type Rarity here!"
    ]
    inputs = ["", "", "", "", "", "", ""]
    toggle_buttons = {
        "Is ranged?": [pygame.Rect(150, 500, 100, 30), "YES"],
        "Is weapon?": [pygame.Rect(300, 500, 100, 30), "YES"],
        "Is accessory?": [pygame.Rect(450, 500, 100, 30), "YES"]
    }
    active_box = None
    text_rects = [pygame.Rect(box.x + 5, box.y + 5, box.width - 10, box.height - 10) for box in input_boxes]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if title_text_rect.collidepoint(mouse_pos):
                    return
                for idx, rect in enumerate(text_rects):
                    if rect.collidepoint(mouse_pos):
                        active_box = idx
                    else:
                        if idx == active_box:
                            active_box = None
                for text, (rect, state) in toggle_buttons.items():
                    if rect.collidepoint(mouse_pos):
                        toggle_buttons[text][1] = "NO" if state == "YES" else "YES"
                if (mouse_pos[0] - export_button_position[0]) ** 2 + (mouse_pos[1] - export_button_position[1]) ** 2 <= BUTTON_RADIUS ** 2:
                    name = inputs[1] if inputs[1] else "DefaultName"
                    mod_namespace = "ModNamespaceHere"
                    width = int(inputs[4]) if inputs[4].isdigit() else 32
                    height = int(inputs[5]) if inputs[5].isdigit() else 32
                    rarity = inputs[6] if inputs[6] else "White"
                    generate_item_file(name, mod_namespace, width, height, 999, 10000, rarity)
            elif event.type == pygame.KEYDOWN and active_box is not None:
                handle_text_input(event, active_box, inputs)

        # Clear screen
        draw_background_gradient(screen, BACKGROUND_GRADIENT_START, BACKGROUND_GRADIENT_END)

        # Draw circle and text
        draw_gradient_circle(screen, "Item", (100, HEIGHT // 2), [BLUE_CIRCLE_COLOR, (0, 0, 128)])
        draw_text(screen, "Terraria Mod Maker", title_text_position, title_font)

        # Draw input boxes
        for idx, box in enumerate(input_boxes):
            draw_input_box(screen, box, inputs[idx] if inputs[idx] else placeholder_texts[idx], active_box == idx)

        # Draw toggle buttons below input boxes
        for text, (rect, state) in toggle_buttons.items():
            rect.y += 50  # Adjust Y position to move below input boxes
            draw_gradient_circle(screen, f"{text} {state}", rect.center, GRADIENT_COLORS["Option"])

        # Draw export button
        draw_gradient_circle(screen, "Export", export_button_position, GRADIENT_COLORS["Export"])

        # Update display
        pygame.display.flip()

def npc_menu():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if title_text_rect.collidepoint(mouse_pos):
                    return

        # Clear screen
        draw_background_gradient(screen, BACKGROUND_GRADIENT_START, BACKGROUND_GRADIENT_END)

        # Draw circle and text
        draw_gradient_circle(screen, "NPC", (100, HEIGHT // 2), [BLUE_CIRCLE_COLOR, (0, 0, 128)])
        draw_text(screen, "Terraria Mod Maker", title_text_position, title_font)
        draw_text(screen, "WIP", (WIDTH // 2, HEIGHT // 2), font)

        # Update display
        pygame.display.flip()

def settings_menu():
    global npc_option
    input_boxes = [pygame.Rect(150, 100, 300, 30)]
    placeholder_texts = ["Export Folder"]
    inputs = [export_folder]
    toggle_buttons = {"Show NPC option?": [pygame.Rect(150, 200, 200, 30), "YES" if npc_option else "NO"]}
    active_box = None
    text_rects = [pygame.Rect(box.x + 5, box.y + 5, box.width - 10, box.height - 10) for box in input_boxes]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if title_text_rect.collidepoint(mouse_pos):
                    return
                for idx, rect in enumerate(text_rects):
                    if rect.collidepoint(mouse_pos):
                        active_box = idx
                        select_export_folder()
                        inputs[idx] = export_folder
                    else:
                        if idx == active_box:
                            active_box = None
                for text, (rect, state) in toggle_buttons.items():
                    if rect.collidepoint(mouse_pos):
                        npc_option = not npc_option
                        toggle_buttons[text][1] = "YES" if npc_option else "NO"
            elif event.type == pygame.KEYDOWN and active_box is not None:
                handle_text_input(event, active_box, inputs)

        # Clear screen
        draw_background_gradient(screen, BACKGROUND_GRADIENT_START, BACKGROUND_GRADIENT_END)

        # Draw circle and text
        draw_gradient_circle(screen, "Settings", (WIDTH - 100, HEIGHT // 2), GRADIENT_COLORS["Settings"])
        draw_text(screen, "Terraria Mod Maker", title_text_position, title_font)

        # Draw input boxes
        for idx, box in enumerate(input_boxes):
            draw_input_box(screen, box, inputs[idx] if inputs[idx] else placeholder_texts[idx], active_box == idx)

        # Draw toggle buttons
        for text, (rect, state) in toggle_buttons.items():
            draw_gradient_circle(screen, f"{text} {state}", rect.center, GRADIENT_COLORS["Option"])

        # Update display
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
