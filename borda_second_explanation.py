from manim import *

class BordaSecondExplanation(Scene):

    def construct(self):
        table_data = [
            ["Ballot", "Count"],
            ["BCA", "8"],
            ["ABC", "6"],
            ["CBA", "5"],
            ["ACB", "4"],
            ["BAC", "2"]
        ]

        table = Table(
            table_data,
            include_outer_lines=True
        ).scale(0.5).to_edge(LEFT)

        self.play(FadeIn(table))

        number_line = NumberLine(
            x_range=[1, 3, 1],
            length=7,
            color=GREY,
            include_numbers=True,
            numbers_to_include=np.arange(1, 4),
            numbers_with_elongated_ticks=[1, 2, 3],
            unit_size=1,
        ).shift(UP*2).shift(RIGHT)

        marker_a = VGroup(
            Triangle(fill_opacity=1, color=GREEN).scale(0.1).rotate(PI),
            Text("A", color=GREEN, font_size=24).next_to(Triangle(fill_opacity=1, color=RED).scale(0.3).rotate(PI), UP, buff=0.1)
        )
        marker_b = VGroup(
            Triangle(fill_opacity=1, color=RED).scale(0.1).rotate(PI),
            Text("B", color=RED, font_size=24).next_to(Triangle(fill_opacity=1, color=BLUE).scale(0.3).rotate(PI), UP, buff=0.1)
        ).next_to(marker_a, RIGHT, buff=0.5)
        marker_c = VGroup(
            Triangle(fill_opacity=1, color=BLUE).scale(0.1).rotate(PI),
            Text("C", color=BLUE, font_size=24).next_to(Triangle(fill_opacity=1, color=GREEN).scale(0.3).rotate(PI), UP, buff=0.1)
        ).next_to(marker_b, RIGHT, buff=0.5)

        markers = VGroup(marker_a, marker_b, marker_c)
        markers.next_to(number_line, UP, buff=0.1)

        self.play(Create(number_line), Create(markers))
        self.wait(8)

        placement_sum_a = 0
        placement_sum_b = 0
        placement_sum_c = 0
        total_count = 0

        for i, row in enumerate(table_data[1:], start=1):
            ballot, count = row
            count = int(count)

            placement_sum_a += count * (ballot.index("A") + 1)
            placement_sum_b += count * (ballot.index("B") + 1)
            placement_sum_c += count * (ballot.index("C") + 1)

            total_count += count

            avg_placement_a = placement_sum_a / total_count
            avg_placement_b = placement_sum_b / total_count
            avg_placement_c = placement_sum_c / total_count

            table.get_rows()[i].set_color(YELLOW)

            self.play(
                marker_a.animate.move_to(number_line.n2p(avg_placement_a) * RIGHT + marker_a.get_center()[1] * UP),
                marker_b.animate.move_to(number_line.n2p(avg_placement_b) * RIGHT + marker_b.get_center()[1] * UP),
                marker_c.animate.move_to(number_line.n2p(avg_placement_c) * RIGHT + marker_c.get_center()[1] * UP),
                run_time=0.3
            )
            table.get_rows()[i].set_color(WHITE)
            self.wait(0.5)

        self.wait(1)
        candidate_score_data = [
            ["Candidate", "Score"],
            ["A", "22"],
            ["B", "31"],
            ["C", "22"],
        ]

        candidate_score_table = Table(
            candidate_score_data,
            include_outer_lines=True
        ).scale(0.5).to_edge(DOWN).shift(UP*1.5)

        self.play(FadeIn(candidate_score_table))
        self.wait(1)

        a = candidate_score_table.get_entries_without_labels()[2]
        a_score = candidate_score_table.get_entries_without_labels()[3]
        b= candidate_score_table.get_entries_without_labels()[4]
        b_score = candidate_score_table.get_entries_without_labels()[5]
        c = candidate_score_table.get_entries_without_labels()[6]
        c_score = candidate_score_table.get_entries_without_labels()[7]

        self.play(
            b.animate.set_color(YELLOW),
            b_score.animate.set_color(YELLOW),
            run_time=1
        )
        self.wait(1)

        self.play(
            a.animate.set_color(YELLOW),
            a_score.animate.set_color(YELLOW),
            b.animate.set_color(WHITE),
            b_score.animate.set_color(WHITE),
            c.animate.set_color(YELLOW),
            c_score.animate.set_color(YELLOW),
            run_time=1
        )
        self.wait(1)
        self.play(
            FadeOut(table),
            FadeOut(candidate_score_table),
            FadeOut(number_line),
            FadeOut(markers)
        )