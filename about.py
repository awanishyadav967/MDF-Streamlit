import streamlit as st

def about_page():
    st.write(
        """
        ## About This App

        This Streamlit app demonstrates the execution of a dynamical system model defined using the Model Description Format (MDF).

        ### Purpose:
        The purpose of this app is to provide an interactive environment for users to explore the behavior of the dynamical system model.

        ### Components:
        - Streamlit App: The Streamlit app provides an interactive user interface for configuring and executing the model.
        - Model Definition: The MDF model is defined using Python classes and objects. It consists of three nodes interconnected in a specific pattern.
        - Model Parameters: The user can adjust the initial values of the variables (x, y, and z) through sliders in the sidebar.
        - Execute Model Button: Upon clicking the "Execute Model" button, the model is created with the user-defined parameters, and its evaluation is triggered.
        - Evaluation: The model is evaluated using an execution engine (EvaluableGraph) from the modeci_mdf library. The evaluation progresses in discrete time increments, updating the state of the model.
        - Output Display: The output of each node (x, y, and z) is displayed to the user after the model evaluation is complete.
        - Sidebar Navigation: Allows users to navigate between different sections.

        ### Execution Flow:
        1. The user adjusts the initial values of x, y, and z using sliders in the sidebar.
        2. The user clicks the "Execute Model" button to run the simulation.
        3. The model is created with the specified parameters, and its evaluation begins.
        4. As the model is evaluated, the current values of x, y, and z are displayed to the user.
        5. Real-time plotting shows how the values of x, y, and z change over time.
        6. The user can navigate between different sections of the app using the sidebar options.

        ### Conclusion:
        This Streamlit app provides an interactive environment for users to explore the behavior of a dynamical system model defined in the MDF format. It offers flexibility in adjusting model parameters and visualizing the system's output in real-time. Additionally, the sidebar navigation enhances user experience by providing access to different sections of the app.
        """
    )


def app():
    about_page()

if __name__ == "__main__":
    app()
