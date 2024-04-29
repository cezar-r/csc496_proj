from manim import *

class BordaProblemScene(Scene):

    def construct(self):
        table_data = [
            ["Ballot", "Count"],
            ["ABC", "10"],
            ["BCA", "7"],
            ["ACB", "4"],
            ["CBA", "4"],
            ["BAC", "2"]
        ]

        table = Table(
            table_data,
            include_outer_lines=True
        ).scale(0.5).to_edge(LEFT)

        self.play(FadeIn(table))
        self.wait(10)

        total_votes_text = Text("Total votes: 27",color=BLUE, font_size=36).next_to(table, RIGHT,  buff=1).shift(UP*1.75)
        self.play(Write(total_votes_text))
        self.wait(3)

        votes = [14, 9, 4]  # First-place votes for candidates A, B, C
        total_votes = sum(votes)
        angles = [TAU * vote / total_votes for vote in votes]
        colors = [RED, BLUE, GREEN]
        labels = ["A", "B", "C"]

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

        pie_chart = VGroup(*sectors).next_to(total_votes_text, DOWN, buff=0.5).rotate(PI/2)
        pie_labels = VGroup()
        for label, sector in zip(labels, sectors):
            label_pos = sector.get_center()
            label_text = Text(label, font_size=21, color=WHITE).move_to(label_pos)
            pie_labels.add(label_text)

        self.play(FadeIn(pie_chart), FadeIn(pie_labels))
        self.wait(2)

        sector_a = sectors[0]
        label_a = pie_labels[0]
        self.play(
            sector_a.animate.scale(1.1),
            label_a.animate.scale(1.1),
            run_time=2
        )
        self.wait(2)
        self.play(
            sector_a.animate.scale(1 / 1.1),
            label_a.animate.scale(1 / 1.1),
            run_time=2
        )
        self.wait(2)

        self.play(
            FadeOut(total_votes_text),
            FadeOut(pie_chart),
            FadeOut(pie_labels)
        )

        self.wait(2)

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
        self.wait(1)

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
                run_time=0.25
            )
            table.get_rows()[i].set_color(WHITE)
            self.wait(0.5)

        self.wait(4)

        self.play(
            FadeOut(table),
            FadeOut(number_line),
            FadeOut(markers)
        )

        criteria_texts = [
            "Majority Criterion",
            "Condorcet Winner",
            "Smith",
            "ISDA",
            "Monotone",
            "Participation",
            "Later-No-Harm",
            "Later-No-Help"
        ]

        criteria_group = VGroup()

        for criterion in criteria_texts:
            criterion_text = Text(criterion, font_size=36)
            criteria_group.add(criterion_text)

        rows = len(criteria_texts) // 2
        grid = criteria_group.arrange_in_grid(rows=rows, cols=2, buff=(1, 1)).to_edge(UP).shift(DOWN*.5)

        majority_criterion_text = grid[0]

        self.play(FadeIn(majority_criterion_text))
        self.wait(2)

        self.play(FadeIn(grid[1:]))
        self.wait(4)

        self.play(FadeOut(grid[1:]))
        
        self.wait(15)
        self.play(FadeOut(majority_criterion_text))
        