import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from modeci_mdf.mdf import *

def app():
    st.title("Multi-Mass System Simulation")
    st.write("Set the masses with the sliders below and click the button to run the simulation.")

    m1 = st.slider("Mass 1 (kg)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    m2 = st.slider("Mass 2 (kg)", min_value=0.1, max_value=10.0, value=2.0, step=0.1)
    m3 = st.slider("Mass 3 (kg)", min_value=0.1, max_value=10.0, value=1.5, step=0.1)

    if st.button("Run Simulation"):
        execute_model(m1, m2, m3)

def execute_model(m1, m2, m3):
    # Define system parameters
    k1 = 10.0  # spring constant for the first spring (N/m)
    k2 = 15.0  # spring constant for the second spring (N/m)

    # Create a new Model
    multi_mass_model = Model(id="MultiMass_Model")

    # Create a Graph inside the Model
    multi_mass_graph = Graph(id="MultiMass_Graph")
    multi_mass_model.graphs.append(multi_mass_graph)

    # Define time array
    t = np.linspace(0, 10, 100)

    # Node for the first mass
    mass1_node = Node(id="Mass1_Node")
    displacement1_param = Parameter(id="displacement1", value=np.sin(2 * np.pi * t))
    velocity1_param = Parameter(id="velocity1", value=np.gradient(displacement1_param.value, t))
    acceleration1_param = Parameter(id="acceleration1", value=np.gradient(velocity1_param.value, t))
    mass1_node.parameters.extend([displacement1_param, velocity1_param, acceleration1_param])

    # Node for the second mass
    mass2_node = Node(id="Mass2_Node")
    displacement2_param = Parameter(id="displacement2", value=np.cos(2 * np.pi * t))
    velocity2_param = Parameter(id="velocity2", value=np.gradient(displacement2_param.value, t))
    acceleration2_param = Parameter(id="acceleration2", value=np.gradient(velocity2_param.value, t))
    mass2_node.parameters.extend([displacement2_param, velocity2_param, acceleration2_param])

    # Node for the third mass
    mass3_node = Node(id="Mass3_Node")
    displacement3_param = Parameter(id="displacement3", value=np.sin(2 * np.pi * t + np.pi/4))
    velocity3_param = Parameter(id="velocity3", value=np.gradient(displacement3_param.value, t))
    acceleration3_param = Parameter(id="acceleration3", value=np.gradient(velocity3_param.value, t))
    mass3_node.parameters.extend([displacement3_param, velocity3_param, acceleration3_param])

    # Add nodes to the graph
    multi_mass_graph.nodes.extend([mass1_node, mass2_node, mass3_node])

    # Define edges representing the springs between masses
    spring1_edge = Edge(id="spring1_edge", sender=mass1_node.id, receiver=mass2_node.id, sender_port="displacement1", receiver_port="displacement2")
    spring2_edge = Edge(id="spring2_edge", sender=mass2_node.id, receiver=mass3_node.id, sender_port="displacement2", receiver_port="displacement3")

    # Add edges to the graph
    multi_mass_graph.edges.extend([spring1_edge, spring2_edge])

    # Generate a graph image
    graph_image_file = "MultiMassSystem.png"
    multi_mass_model.to_graph_image(engine="dot", output_format="png", filename_root="MultiMassSystem", is_horizontal=True)

    # Display the generated graph image
    st.write("Displaying the generated graph image")
    st.image(graph_image_file)

    # Plotting the displacements over time
    st.write("Plotting the displacements over time")
    plt.figure(figsize=(10, 5))
    plt.plot(t, displacement1_param.value, label='Mass 1', color='blue')
    plt.plot(t, displacement2_param.value, label='Mass 2', color='orange')
    plt.plot(t, displacement3_param.value, label='Mass 3', color='green')
    plt.xlabel('Time')
    plt.ylabel('Displacement')
    plt.title('Displacement over Time for Multiple Masses')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    # Plotting the velocities over time
    st.write("Plotting the velocities over time")
    plt.figure(figsize=(10, 5))
    plt.plot(t, velocity1_param.value, label='Velocity Mass 1', color='blue')
    plt.plot(t, velocity2_param.value, label='Velocity Mass 2', color='orange')
    plt.plot(t, velocity3_param.value, label='Velocity Mass 3', color='green')
    plt.xlabel('Time')
    plt.ylabel('Velocity')
    plt.title('Velocity over Time for Multiple Masses')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    # Plotting the accelerations over time
    st.write("Plotting the accelerations over time")
    plt.figure(figsize=(10, 5))
    plt.plot(t, acceleration1_param.value, label='Acceleration Mass 1', color='blue')
    plt.plot(t, acceleration2_param.value, label='Acceleration Mass 2', color='orange')
    plt.plot(t, acceleration3_param.value, label='Acceleration Mass 3', color='green')
    plt.xlabel('Time')
    plt.ylabel('Acceleration')
    plt.title('Acceleration over Time for Multiple Masses')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

if __name__ == "__main__":
    app()
