from manim import *

class ElectionBallotScene(Scene):
    def construct(self):

        table_data = [
            ["Ballot", "Count"],
            ["BCA", "129"],
            ["ABC", "86"],
            ["CBA", "75"],
            ["ACB", "64"],
            ["BAC", "21"]
        ]
        
         
        table = Table(
            table_data,
            include_outer_lines=True
        ).scale(0.5).to_edge(LEFT)

        # Fade in the table
        self.play(FadeIn(table))
        self.wait(4)

        dot = Dot(color=YELLOW).next_to(table.get_rows()[1], RIGHT*3)
        self.play(FadeIn(dot))
        self.wait(1) 

        alice = Text("Alice", color=RED).to_edge(UP).shift(LEFT).scale(0.7)
        betty = Text("Betty", color=BLUE).to_edge(UP).shift(RIGHT).scale(0.7)
        charles = Text("Charles", color=GREEN).to_edge(UP).shift(RIGHT * 3).scale(0.7)

        self.play(
            Write(alice),
            Write(betty),
            Write(charles)
        )

        self.wait(1)

        numbers = VGroup(
            *[Text(str(i)).scale(0.8).next_to(alice, DOWN).shift(LEFT * 1.5 + DOWN * (i)) for i in range(1, 4)]
        )

        grid = VGroup(
            *[Dot(color=BLACK, fill_opacity=1, stroke_color=WHITE, stroke_width=2).scale(1.5).next_to(numbers[i // 3], RIGHT).shift(RIGHT * 2 * ((i % 3)+.5)) for i in range(9)]
        )

        self.play(
            Write(numbers[0]),
            Write(grid[:3]),
            grid[1].animate.set_color(BLUE_C)
        )
        self.wait(1)

        self.play(
            Write(numbers[1]),
            Write(grid[3:6]),
            grid[5].animate.set_color(BLUE_C)
        )
        self.wait(1)

        self.play(
            Write(numbers[2]),
            Write(grid[6:]),
            grid[6].animate.set_color(BLUE_C)
        )
        self.wait(1)

        ballot_text = VGroup(
            Text("Ballot ", font_size=32),
            Text("B", color=BLUE, font_size=32),
            Text("C", color=GREEN, font_size=32),
            Text("A", color=RED, font_size=32),
            Text(" = 129 votes", font_size=32).shift(RIGHT*2)
        ).arrange(RIGHT, buff=0.1).next_to(grid, DOWN, buff=1).shift(LEFT*1.5)
        self.wait(.5)

        self.play(FadeIn(ballot_text))
        self.wait(2)

        self.play(
            FadeOut(grid),
            FadeOut(ballot_text),
            dot.animate.next_to(table.get_rows()[2], RIGHT*3.25)
        )
        self.wait(2)


        grid = VGroup(
            *[Dot(color=BLACK, fill_opacity=1, stroke_color=WHITE, stroke_width=2).scale(1.5).next_to(numbers[i // 3], RIGHT).shift(RIGHT * 2 * ((i % 3)+.5)) for i in range(9)]
        )

        self.play(
            Write(grid[:3]),
            grid[0].animate.set_color(BLUE_C)
        )
        self.wait(1)

        self.play(
            Write(grid[3:6]),
            grid[4].animate.set_color(BLUE_C)
        )
        self.wait(1)

        self.play(
            Write(grid[6:]),
            grid[8].animate.set_color(BLUE_C)
        )
        self.wait(1)

        ballot_text = VGroup(
            Text("Ballot ", font_size=32),
            Text("A", color=RED, font_size=32),
            Text("B", color=BLUE, font_size=32),
            Text("C", color=GREEN, font_size=32),
            Text(" = 86 votes", font_size=32).shift(RIGHT*2)
        ).arrange(RIGHT, buff=0.1).next_to(grid, DOWN, buff=1).shift(LEFT*1.5)
        self.wait(.5)

        self.play(FadeIn(ballot_text))
        self.wait(4)

        self.play(
            FadeOut(alice),
            FadeOut(betty),
            FadeOut(charles),
            FadeOut(grid),
            FadeOut(numbers),
            FadeOut(ballot_text),
            FadeOut(dot)
        )
        self.wait(2)

        first_place_votes_text = Text("First Place Votes", font_size=40).next_to(table, RIGHT, buff=1).shift(UP*2.5)

        vote_counts = VGroup(
            Text("A = 86 + 64 = 150", font_size=32),
            Text("B = 129 + 21 = 150", font_size=32),
            Text("C = 75", font_size=32)
        ).arrange(DOWN * 1.2, aligned_edge=LEFT).next_to(first_place_votes_text, DOWN, buff=0.5)

        self.play(FadeIn(first_place_votes_text))
        self.wait(1)

        # Highlight rows for "A = 86 + 64 = 150"
        self.play(
            FadeIn(vote_counts[0]),
            vote_counts[0].animate.set_color(YELLOW),
            table.get_rows()[2].animate.set_color(YELLOW),
            table.get_rows()[4].animate.set_color(YELLOW)
        )
        self.wait(1)
        self.play(
            vote_counts[0].animate.set_color(WHITE),
            table.get_rows()[2].animate.set_color(WHITE),
            table.get_rows()[4].animate.set_color(WHITE)
        )

        # Highlight rows for "B = 129 + 21 = 150"
        self.play(
            FadeIn(vote_counts[1]),
            vote_counts[1].animate.set_color(YELLOW),
            table.get_rows()[1].animate.set_color(YELLOW),
            table.get_rows()[5].animate.set_color(YELLOW)
        )
        self.wait(1)
        self.play(
            vote_counts[1].animate.set_color(WHITE),
            table.get_rows()[1].animate.set_color(WHITE),
            table.get_rows()[5].animate.set_color(WHITE)
        )

        # Highlight row for "C = 75"
        self.play(
            FadeIn(vote_counts[2]),
            vote_counts[2].animate.set_color(YELLOW),
            table.get_rows()[3].animate.set_color(YELLOW)
        )
        self.wait(1)
        self.play(
            vote_counts[2].animate.set_color(WHITE),
            table.get_rows()[3].animate.set_color(WHITE)
        )

        self.wait(2) # set longer

        question_mark = Text("?", font_size=200)
        question_mark.set_color(RED)
        question_mark.move_to(ORIGIN)  # Position the question mark at the center

        self.play(FadeIn(question_mark))
        self.wait(2)

        self.play(
            FadeOut(first_place_votes_text),
            FadeOut(vote_counts),
            FadeOut(question_mark),
            FadeOut(table)
        )
        self.wait(2)

        