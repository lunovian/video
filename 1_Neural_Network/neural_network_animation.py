from manim import *
import numpy as np

class NeuralNetworkScene(Scene):
    def create_curve(self, start, end):
        # Helper method to create smooth curves
        control1 = start + np.array([1.0, 0, 0])
        control2 = end + np.array([-1.0, 0, 0])
        return VMobject().set_points_smoothly([start, control1, control2, end])

    def construct(self):
        # Create layers using circles with different colors
        input_layer = VGroup(*[
            Circle(radius=0.3, fill_opacity=0.4, color=BLUE) 
            for _ in range(3)
        ]).arrange(DOWN, buff=0.8)
        
        hidden_layer = VGroup(*[
            Circle(radius=0.3, fill_opacity=0.4, color=GREEN) 
            for _ in range(4)
        ]).arrange(DOWN, buff=0.8)
        
        output_layer = VGroup(*[
            Circle(radius=0.3, fill_opacity=0.4, color=RED) 
            for _ in range(2)
        ]).arrange(DOWN, buff=0.8)

        # Position layers
        layers = VGroup(input_layer, hidden_layer, output_layer).arrange(RIGHT, buff=2.5)
        
        # Add connections between layers
        connections1 = VGroup()
        connections2 = VGroup()

        # Connect input to hidden layer with curved lines
        for i in input_layer:
            for h in hidden_layer:
                curve = self.create_curve(i.get_right(), h.get_left())
                curve.set_stroke(opacity=0.3, width=2)
                connections1.add(curve)

        # Connect hidden to output layer with curved lines
        for h in hidden_layer:
            for o in output_layer:
                curve = self.create_curve(h.get_right(), o.get_left())
                curve.set_stroke(opacity=0.3, width=2)
                connections2.add(curve)

        # Smoother animation sequence
        self.play(
            AnimationGroup(
                *[FadeIn(node, shift=UP*0.5) for node in input_layer],
                lag_ratio=0.2
            )
        )
        self.play(
            AnimationGroup(
                *[FadeIn(node, shift=UP*0.5) for node in hidden_layer],
                lag_ratio=0.2
            )
        )
        self.play(
            AnimationGroup(
                *[FadeIn(node, shift=UP*0.5) for node in output_layer],
                lag_ratio=0.2
            )
        )
        
        # Animate connections with smooth fade in
        self.play(
            AnimationGroup(
                *[Create(conn) for conn in connections1],
                lag_ratio=0.05
            )
        )
        self.play(
            AnimationGroup(
                *[Create(conn) for conn in connections2],
                lag_ratio=0.05
            )
        )

        # Add smoother data flow animation
        self.add_data_flow_animation(connections1, connections2)
        
        self.wait()

    def add_data_flow_animation(self, connections1, connections2):
        # Run the animation twice for better effect
        for _ in range(2):
            # First layer of connections
            squares1 = VGroup(*[
                Square(side_length=0.1, fill_opacity=0.8, color=BLUE).move_to(conn.points[0])
                for conn in connections1
            ])
            self.add(squares1)
            
            self.play(
                AnimationGroup(
                    *[
                        MoveAlongPath(square, conn)
                        for square, conn in zip(squares1, connections1)
                    ],
                    lag_ratio=0.05
                ),
                run_time=2
            )
            self.remove(squares1)
            
            # Second layer of connections
            squares2 = VGroup(*[
                Square(side_length=0.1, fill_opacity=0.8, color=GREEN).move_to(conn.points[0])
                for conn in connections2
            ])
            self.add(squares2)
            
            self.play(
                AnimationGroup(
                    *[
                        MoveAlongPath(square, conn)
                        for square, conn in zip(squares2, connections2)
                    ],
                    lag_ratio=0.05
                ),
                run_time=2
            )
            self.remove(squares2)
