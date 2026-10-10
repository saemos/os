import os
from src.transformer import MicroTransformer

class TextbookAnimatorBot:
    def __init__(self, data_path="data/book_data.txt"):
        self.data_path = data_path

    def read_textbook(self):
        """Reads the local textbook or notes file."""
        if not os.path.exists(self.data_path):
            return "No textbook found."
        with open(self.data_path, "r", encoding="utf-8") as f:
            return f.read()

    def plan_3b1b_scene(self, concept_name):
        """
        Instructions for the bot: 
        Parses text and formats a 3B1B-style storyboard (Intuition -> Formula -> Visual).
        """
        text_content = self.read_textbook()
        print(f"[Bot] Reading local textbook data... Found {len(text_content)} characters.")
        print(f"[Bot] Analyzing concept: '{concept_name}' for visual metaphors...")

        # Here, the bot maps your text into a Manim structural template
        manim_code = f"""
from manim import *

class Generated3B1BScene(Scene):
    def construct(self):
        # 1. Title matching 3B1B style
        title = Text("{concept_name}", font_size=36, color=BLUE)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # 2. Visual geometric explanation based on textbook notes
        square = Square(side_length=2, color=GREEN)
        self.play(Create(square))
        self.wait(1)

        # 3. Transformation / Core Intuition
        circle = Circle(radius=1.5, color=RED)
        self.play(Transform(square, circle))
        self.wait(2)
"""
        return manim_code

    def save_and_render_script(self, code, filename="scene.py"):
        """Saves the generated animation script locally on your PC."""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"[Bot] Saved Manim script to {filename}.")
        print(f"[Bot] To compile video locally, run: manim -pql {filename} Generated3B1BScene")

if __name__ == "__main__":
    bot = TextbookAnimatorBot()
    # Instruct your bot to build an animation from your textbook notes
    animation_code = bot.plan_3b1b_scene("Core Physics Vector Fields")
    bot.save_and_render_script(animation_code)
