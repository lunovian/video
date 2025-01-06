from manim import *

class BasicComponents(Scene):
    def construct(self):
        # Title sequence
        title = Text("Basic Components of Neural Networks", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create a simple network structure
        network = self.create_network()
        network.scale(0.8).shift(DOWN)
        
        # Section 1: Neurons
        neuron_text = Text("Neurons", font_size=32, color=YELLOW)
        neuron_text.next_to(title, DOWN, buff=0.5)
        
        # Simple neuron visualization - centered
        example_neuron = Circle(radius=0.7, fill_opacity=0.3, color=BLUE, stroke_width=5)
        example_neuron.move_to(ORIGIN)  # Place at center of screen
        
        self.play(Write(neuron_text))
        self.play(Create(example_neuron))
        self.wait()
        self.play(
            FadeOut(example_neuron), 
            FadeOut(neuron_text)
        )

        # Section 2: Layers
        self.explain_layers(network, title)  # Pass title as parameter
        
        # Section 3: Connections
        self.explain_connections(network, title)  # Pass title as parameter
        
        self.wait(2)

    def create_network(self):
        # Create layers first
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

        # Position all layers first
        all_layers = VGroup(input_layer, hidden_layer, output_layer).arrange(RIGHT, buff=3)
        
        # Add labels after layers are positioned
        input_label = Text("Input Layer", font_size=24).next_to(input_layer, UP, buff=0.5)
        hidden_label = Text("Hidden Layer", font_size=24).next_to(hidden_layer, UP, buff=0.5)
        output_label = Text("Output Layer", font_size=24).next_to(output_layer, UP, buff=0.5)
        labels = VGroup(input_label, hidden_label, output_label)

        # Create connections after layers are in final position
        connections = VGroup()
        
        # Connect input to hidden with better spacing
        for i in input_layer:
            for h in hidden_layer:
                conn = Line(
                    start=i.get_right(),
                    end=h.get_left(),
                    stroke_opacity=0.2,
                    stroke_width=1
                )
                connections.add(conn)
        
        # Connect hidden to output with better spacing
        for h in hidden_layer:
            for o in output_layer:
                conn = Line(
                    start=h.get_right(),
                    end=o.get_left(),
                    stroke_opacity=0.2,
                    stroke_width=1
                )
                connections.add(conn)

        # Return everything grouped together
        return VGroup(all_layers, connections, labels)

    def explain_layers(self, network, title):
        layer_text = Text("Layers: Organized Information Flow", font_size=32, color=YELLOW)
        layer_text.next_to(title, DOWN, buff=0.5)
        
        # Get the actual layers from the network (input, hidden, output)
        layers = network[0]  # This gets [input_layer, hidden_layer, output_layer]
        
        self.play(Write(layer_text))
        self.play(Create(network))
        
        # Highlight each layer individually
        for i, layer in enumerate(layers):
            indicator = Dot(color=YELLOW, radius=0.1)
            indicator.next_to(layer, DOWN, buff=0.5)
            
            self.play(
                layer.animate.set_color(YELLOW),
                FadeIn(indicator)
            )
            self.wait()
            self.play(
                layer.animate.set_color([BLUE, GREEN, RED][i]),
                FadeOut(indicator)
            )
        
        self.play(FadeOut(layer_text))

    def explain_connections(self, network, title):
        connection_text = Text("Connections: How Neurons Communicate", font_size=32, color=YELLOW)
        connection_text.next_to(title, DOWN, buff=0.5)
        
        # Choose connections to highlight
        strong_conn_index = 0
        weak_conn_index = len(network[1]) - 1
        
        # Create strong connection with smaller, aligned weight
        strong_connection = network[1][strong_conn_index].copy().set_stroke(width=4, opacity=0.8)
        strong_weight = Text("1.0", font_size=12, color=YELLOW)
        # Position weight along the connection line
        strong_midpoint = strong_connection.point_from_proportion(0.5)
        strong_weight.move_to(strong_midpoint).shift(UP * 0.2)
        
        # Create weak connection with smaller, aligned weight
        weak_connection = network[1][weak_conn_index].copy().set_stroke(width=1, opacity=0.3)
        weak_weight = Text("0.2", font_size=12, color=GRAY)
        # Position weight along the connection line
        weak_midpoint = weak_connection.point_from_proportion(0.5)
        weak_weight.move_to(weak_midpoint).shift(UP * 0.2)
        
        # Group connections and weights
        strong_group = VGroup(strong_connection, strong_weight)
        weak_group = VGroup(weak_connection, weak_weight)
        
        # Animation sequence
        self.play(Write(connection_text))
        self.play(
            Create(strong_connection),
            Write(strong_weight)
        )
        self.play(
            Create(weak_connection),
            Write(weak_weight)
        )
        
        self.wait(2)
        
        # Cleanup
        self.play(
            FadeOut(strong_group),
            FadeOut(weak_group),
            FadeOut(connection_text)
        )
