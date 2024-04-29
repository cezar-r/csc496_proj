from manim import *

class IRVIntroScene(Scene):

    def draw_pie_chart(self, votes, labels, colors, table):
        # votes = [14, 9, 4]  # First-place votes for candidates A, B, C
        total_votes = sum(votes)
        angles = [TAU * vote / total_votes for vote in votes]
        # colors = [RED, BLUE, GREEN]
        # labels = ["A", "B", "C"]

        sectors = []
        current_angle = 0
        for angle, color, label in zip(angles, colors, labels):
            sector = Sector(
                outer_radius=1.5,
                start_angle=current_angle,
                angle=angle,
                fill_color=color,
                fill_opacity=0.7,
                stroke_width=2,
            )
            current_angle += angle
            sectors.append(sector)

        pie_chart = VGroup(*sectors).next_to(table, RIGHT*2, buff=0.5).rotate(PI/2)
        pie_labels = VGroup()
        for label, sector in zip(labels, sectors):
            label_pos = sector.get_center()
            label_text = Text(label, font_size=21, color=WHITE).move_to(label_pos)
            pie_labels.add(label_text)
        return pie_chart, pie_labels, sectors

    def construct(self):
        table_data = [
            ["Ballot", "Count"],
            ["BCA", "8"],
            ["ABC", "6"],
            ["CBA", "6"],
            ["ACB", "4"],
            ["BAC", "3"]
        ]

        table = Table(
            table_data,
            include_outer_lines=True
        ).scale(0.5).to_edge(LEFT)

        irv_text = Text("Instant-Runoff Voting (IRV)", font_size=48).scale(0.8).next_to(table, UP, buff=0.5).shift(RIGHT*2)
        threshold_text = Text("Majority Threshold = 14", font_size=24, color=TEAL).next_to(table, DOWN, buff=0.5)


        self.play(FadeIn(irv_text))
        self.wait(9)
        steps_text = VGroup(
            Text("1) Count the number of first choice votes each candidate received", font_size=24),
            Text("2) If a candidate receives the majority (over half) of the first choice votes,\n\tthey are the winner", font_size=24),
            Text("3) Otherwise, eliminate the candidate with the fewest votes", font_size=24),
            Text("4) Repeat steps 1-3 until there is only one candidate remaining", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(irv_text, DOWN, buff=0.5).shift(RIGHT*3)

        for step in steps_text:
            self.play(FadeIn(step))
            self.wait(4)
        self.wait(10)
        self.play(FadeOut(irv_text), FadeOut(steps_text), FadeIn(table), FadeIn(threshold_text))

        self.wait(10)

        pie_chart, pie_labels, _ = self.draw_pie_chart([10, 11, 6], ["A", "B", "C"], [RED, BLUE, GREEN], table)
        fc_votes_text = VGroup(
            Text("A = 10", font_size=30, color=RED),
            Text("B = 10", font_size=30, color=BLUE),
            Text("C = 5", font_size=30, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(pie_chart, RIGHT, buff=1)

        self.play(FadeIn(pie_chart), FadeIn(pie_labels), FadeIn(fc_votes_text))

        self.wait(4)

        c_text = fc_votes_text[2]
        line1 = Line(c_text.get_corner(UL), c_text.get_corner(DR), color=RED)
        line2 = Line(c_text.get_corner(UR), c_text.get_corner(DL), color=RED)
        cross_lines = VGroup(line1, line2)

        self.play(Create(cross_lines))
        self.wait(2)
        self.play(
            FadeOut(pie_chart),
            FadeOut(pie_labels),
            FadeOut(cross_lines),
            FadeOut(fc_votes_text),
        )

        new_table_data = [
            ["Ballot", "Count"],
            ["BA", "8"],
            ["AB", "6"],
            ["BA", "6"],
            ["AB", "4"],
            ["BA", "3"]
        ]

        new_table = Table(
            new_table_data,
            include_outer_lines=True
        ).scale(0.5).to_edge(LEFT)

        self.play(
            FadeOut(table),
            FadeIn(new_table)
        )

        self.wait(2)

        pie_chart, pie_labels, sectors = self.draw_pie_chart([10, 17], ["A", "B"], [RED, BLUE], new_table)
        fc_votes_text = VGroup(
            Text("A = 10", font_size=30, color=RED),
            Text("B = 17", font_size=30, color=BLUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(pie_chart, RIGHT, buff=1)

        self.play(FadeIn(pie_chart), FadeIn(pie_labels), FadeIn(fc_votes_text))
        
        self.wait(1)

        sector_a = sectors[1]
        label_a = pie_labels[1]
        self.play(
            sector_a.animate.scale(1.1),
            label_a.animate.scale(1.1),
            run_time=2
        )
        self.wait(1)
        self.play(
            sector_a.animate.scale(1 / 1.1),
            label_a.animate.scale(1 / 1.1),
            run_time=2
        )
        self.wait(1)

        irv_winner_text = Text("IRV Winner = Betty", color=BLUE, font_size=36)
        irv_winner_text.next_to(pie_chart, DOWN, buff=1).shift(RIGHT)
        self.play(Write(irv_winner_text), run_time=2)
        self.wait(2)

        irv_uc_text = Text("IRV Real World Examples", font_size=48).scale(0.8).next_to(new_table, UP, buff=0.5).shift(RIGHT*1.75)


        self.play(
            FadeOut(new_table),
            FadeOut(threshold_text),
            FadeOut(pie_chart),
            FadeOut(pie_labels),
            FadeOut(irv_winner_text),
            FadeOut(fc_votes_text),
        )
        self.wait(2)
        self.play(FadeIn(irv_uc_text))
        self.wait(2)
        examples_text = VGroup(
            Text("1) U.S. Senate and House of Representatives since 2018", font_size=24),
            Text("2) Maine uses IRV for presidential elections since 2020", font_size=24),
            Text("3) Alaska uses a variation of IRV for both federal and state elections", font_size=24),
            Text("4) San Francisco has used IRV since 2004 for local elections", font_size=24),
            Text("5) Minneapolis adopted IRV for municipal elections in 2009", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(irv_uc_text, DOWN, buff=0.5).shift(RIGHT*3)

        for ex in examples_text:
            self.play(FadeIn(ex))
            self.wait(2)
        self.wait(4)
