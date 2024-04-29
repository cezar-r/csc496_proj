from manim import *

class BallotIntroScene(Scene):
    def construct(self):
        alice = Text("Alice", color=RED).to_edge(UP).shift(LEFT * 3)
        betty = Text("Betty", color=BLUE).to_edge(UP)
        charles = Text("Charles", color=GREEN).to_edge(UP).shift(RIGHT * 3)
        
        self.play(
            Write(alice),
            Write(betty),
            Write(charles)
        )
        self.wait(1)
        
        # DOT MOVING
        dot = Dot(color=YELLOW)
        dot.next_to(alice, DOWN)
        
        self.play(FadeIn(dot))
        self.wait(0.5)
        
        self.play(dot.animate.move_to(betty.get_center() + DOWN * 0.5), run_time=0.5)
        self.wait(0.5)
        self.play(dot.animate.move_to(charles.get_center() + DOWN * 0.5), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(dot))
        self.wait(0.5)

        # GRID
        numbers = VGroup(
            *[Text(str(i)).scale(0.8).next_to(alice, DOWN).shift(LEFT * 2 + DOWN * (i)) for i in range(1, 4)]
        )
        
        grid = VGroup(
            *[Dot(color=BLACK, fill_opacity=1, stroke_color=WHITE, stroke_width=2).scale(2.5).next_to(numbers[i // 3], RIGHT).shift(RIGHT * 3 * ((i % 3)+.5)) for i in range(9)]
        )
        
        self.play(
            Write(numbers),
            Write(grid)
        )
        self.wait(4)


        # FILL IN DOTS
        self.play(
            grid[0].animate.set_color(BLUE_C),  # (Alice, 1)
            grid[5].animate.set_color(BLUE_C),  # (Charles, 2)
            grid[7].animate.set_color(BLUE_C)   # (Betty, 3)
        )
        
        ballot_text = VGroup(
            Text("Ballot = ", font_size=36),
            Text("A", color=RED, font_size=36),
            Text("C", color=GREEN, font_size=36),
            Text("B", color=BLUE, font_size=36)
        ).arrange(RIGHT, buff=0.1).next_to(grid, DOWN, buff=1).shift(LEFT * 3.5)
        self.wait(.5)

        self.play(FadeIn(ballot_text))
        self.wait(2)

        # CLEAR BALLOT TEXT AND REMOVE FILL COLOR
        self.play(
            FadeOut(ballot_text),
            grid[0].animate.set_color(WHITE).set_fill(opacity=0),
            grid[5].animate.set_color(WHITE).set_fill(opacity=0),
            grid[7].animate.set_color(WHITE).set_fill(opacity=0)
        )
        self.wait(1)

        # FILL IN DOTS
        self.play(
            grid[1].animate.set_color(BLUE_C),  # (Alice, 1)
            grid[3].animate.set_color(BLUE_C),  # (Charles, 2)
            grid[8].animate.set_color(BLUE_C)   # (Betty, 3)
        )
        
        ballot_text = VGroup(
            Text("Ballot = ", font_size=40),
            Text("B", color=BLUE, font_size=40),
            Text("A", color=RED, font_size=40),
            Text("C", color=GREEN, font_size=40)
        ).arrange(RIGHT, buff=0.1).next_to(grid, DOWN, buff=1).shift(LEFT * 3.5)
        self.wait(.5)

        self.play(FadeIn(ballot_text))
        self.wait(2)

        # CLEAR BALLOT TEXT AND REMOVE FILL COLOR
        self.play(
            FadeOut(ballot_text),
            grid[1].animate.set_color(WHITE).set_fill(opacity=0),
            grid[3].animate.set_color(WHITE).set_fill(opacity=0),
            grid[8].animate.set_color(WHITE).set_fill(opacity=0)
        )
        self.wait(0.5)
        self.play(
            FadeOut(alice),
            FadeOut(betty),
            FadeOut(charles),
            FadeOut(numbers),
            FadeOut(grid),
        )
