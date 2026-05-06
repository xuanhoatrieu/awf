"""
neural_network.py — Neural Network visualization using pure ManimCE.

Scenes:
  - NeuralNetworkForwardPass: Forward pass through a simple feedforward NN
  - NeuralNetworkActivation: Shows activation functions (Sigmoid, ReLU)

Usage:
  manim -qm neural_network.py NeuralNetworkForwardPass
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from manim import *
import numpy as np
from common_styles import *


class NeuralNetworkForwardPass(Scene):
    """
    Visualize a simple feedforward neural network with forward pass animation.

    Network architecture: [3, 4, 4, 2]
    Shows:
    1. Build network layer by layer
    2. Show weights as connecting lines
    3. Animate forward pass: input → hidden → output
    4. Show activation values lighting up neurons
    """

    # Network config
    layer_sizes = [3, 5, 4, 2]
    neuron_radius = 0.22
    layer_spacing = 2.5
    neuron_spacing = 0.85
    neuron_color = C_NEURON
    edge_color = C_MUTED
    activation_color = C_ACTIVATION

    def construct(self):
        self.camera.background_color = C_DARK_BG

        # ─── Title ───
        create_title_slide(
            self,
            "Neural Network",
            "Forward Propagation"
        )

        # ─── Build Network ───
        layers = self.create_network()
        edges = self.create_edges(layers)

        # Animate layer creation
        for i, layer in enumerate(layers):
            self.play(
                LaggedStart(
                    *[GrowFromCenter(n) for n in layer],
                    lag_ratio=0.1,
                    run_time=0.8
                )
            )

        # Animate edge creation
        self.play(
            LaggedStart(
                *[Create(e) for e in edges],
                lag_ratio=0.002,
                run_time=2
            )
        )
        self.wait(0.5)

        # ─── Layer Labels ───
        labels_text = ["Input", "Hidden 1", "Hidden 2", "Output"]
        labels = VGroup()
        for i, (layer, text) in enumerate(zip(layers, labels_text)):
            label = Text(text, font_size=SMALL_SIZE, color=C_MUTED)
            label.next_to(layer, DOWN, buff=0.4)
            labels.add(label)

        self.play(
            LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.15, run_time=1)
        )
        self.wait(0.5)

        # ─── Forward Pass Animation ───
        # Generate random activations
        np.random.seed(42)
        activations = []
        for size in self.layer_sizes:
            act = np.random.uniform(0.1, 1.0, size)
            activations.append(act)

        # Animate each layer activation
        for layer_idx in range(len(layers)):
            layer = layers[layer_idx]
            act = activations[layer_idx]

            # Light up neurons
            anims = []
            for neuron, a in zip(layer, act):
                anims.append(
                    neuron.animate.set_fill(
                        color=C_ACTIVATION,
                        opacity=float(a)
                    )
                )

            # Highlight incoming edges
            edge_anims = []
            if layer_idx > 0:
                # Find edges connecting to this layer
                edge_start = sum(
                    self.layer_sizes[i] * self.layer_sizes[i + 1]
                    for i in range(layer_idx - 1)
                )
                edge_count = self.layer_sizes[layer_idx - 1] * self.layer_sizes[layer_idx]

                relevant_edges = edges[edge_start:edge_start + edge_count]
                pulse_edges = relevant_edges.copy()
                pulse_edges.set_stroke(C_ACTIVATION, width=3, opacity=0.8)

                edge_anims.append(
                    ShowPassingFlash(
                        pulse_edges,
                        time_width=0.5,
                        run_time=1.2
                    )
                )

            self.play(*anims, *edge_anims, run_time=1.2)
            self.wait(0.3)

        # ─── Output highlight ───
        output_layer = layers[-1]
        output_acts = activations[-1]
        winner_idx = np.argmax(output_acts)

        # Highlight winning neuron
        winner = output_layer[winner_idx]
        flash = Circle(
            radius=self.neuron_radius + 0.1,
            color=C_GREEN,
            stroke_width=3
        )
        flash.move_to(winner.get_center())

        result_text = Text(
            f"Output: Neuron {winner_idx + 1}",
            font_size=BODY_SIZE,
            color=C_GREEN
        )
        result_text.to_edge(DOWN, buff=0.5)

        self.play(
            Create(flash),
            FadeIn(result_text),
            run_time=1
        )
        self.wait(2)

        # Cleanup
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.5)

    def create_network(self):
        """Create neuron circles arranged in layers."""
        layers = VGroup()
        n_layers = len(self.layer_sizes)

        total_width = (n_layers - 1) * self.layer_spacing
        start_x = -total_width / 2

        for i, size in enumerate(self.layer_sizes):
            layer = VGroup()
            total_height = (size - 1) * self.neuron_spacing
            start_y = total_height / 2

            for j in range(size):
                neuron = Circle(
                    radius=self.neuron_radius,
                    color=self.neuron_color,
                    stroke_width=2,
                    fill_color=self.neuron_color,
                    fill_opacity=0.1,
                )
                neuron.move_to(
                    RIGHT * (start_x + i * self.layer_spacing) +
                    UP * (start_y - j * self.neuron_spacing)
                )
                layer.add(neuron)

            layers.add(layer)

        return layers

    def create_edges(self, layers):
        """Create connecting lines between adjacent layers."""
        edges = VGroup()

        for i in range(len(layers) - 1):
            for n1 in layers[i]:
                for n2 in layers[i + 1]:
                    edge = Line(
                        n1.get_center(),
                        n2.get_center(),
                        color=self.edge_color,
                        stroke_width=1,
                        stroke_opacity=0.3,
                        buff=self.neuron_radius,
                    )
                    edges.add(edge)

        return edges


class NeuralNetworkActivation(Scene):
    """
    Visualize activation functions: Sigmoid, ReLU, Tanh
    Shows the function curves and their properties.
    """

    def construct(self):
        self.camera.background_color = C_DARK_BG

        create_title_slide(
            self,
            "Activation Functions",
            "Hàm kích hoạt trong Neural Network"
        )

        # ─── Setup 3 side-by-side plots ───
        functions = [
            ("Sigmoid", sigmoid, [-6, 6], [0, 1], C_BLUE),
            ("ReLU", relu, [-4, 6], [-1, 6], C_GREEN),
            ("Tanh", lambda x: np.tanh(x), [-4, 4], [-1.5, 1.5], C_PURPLE),
        ]

        plots = VGroup()
        for i, (name, func, x_range, y_range, color) in enumerate(functions):
            ax = Axes(
                x_range=[x_range[0], x_range[1], 1],
                y_range=[y_range[0], y_range[1], 0.5],
                x_length=3.5,
                y_length=2.5,
                axis_config={"color": C_MUTED, "stroke_width": 1.5},
                tips=False,
            )

            curve = ax.plot(func, color=color, stroke_width=2.5)
            label = Text(name, font_size=LABEL_SIZE, color=color)
            label.next_to(ax, UP, buff=0.2)

            plot_group = VGroup(ax, curve, label)
            plots.add(plot_group)

        plots.arrange(RIGHT, buff=0.8)
        plots.center()

        # Animate each plot
        for plot in plots:
            ax, curve, label = plot
            self.play(
                Create(ax),
                FadeIn(label),
                run_time=0.5
            )
            self.play(Create(curve, run_time=1))

        self.wait(2)

        # ─── Highlight key properties ───
        properties = [
            "Output: (0, 1)\nSmooth gradient",
            "f(x) = max(0, x)\nFast computation",
            "Output: (-1, 1)\nZero-centered",
        ]

        prop_texts = VGroup()
        for i, (plot, prop) in enumerate(zip(plots, properties)):
            text = Text(prop, font_size=16, color=C_MUTED, line_spacing=1.2)
            text.next_to(plot, DOWN, buff=0.3)
            prop_texts.add(text)

        self.play(
            LaggedStart(*[FadeIn(t) for t in prop_texts], lag_ratio=0.3, run_time=1.5)
        )
        self.wait(3)

        # Cleanup
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.5)
