import streamlit as st
import json
import utils.privacy_violation as privacy_violation
import utils.profanity as profanity
import utils.visual_analysis as visual_analysis

# This code is a Streamlit app that allows users to upload a JSON file containing conversation data and select between two implementations (Regex or ML) and two models (Profanity Filter or Privacy and Compliance Violation). The app then processes the conversation data using the selected implementation and model, displaying the results on the page.
# The app uses functions from the utils.privacy_violation and utils.profanity modules to perform the necessary processing.
# The app also includes error handling to ensure that the user selects a valid implementation type and model before processing the conversation data.

# get file input from user
uploaded_file = st.file_uploader("Choose a file", type=["json"])


if uploaded_file is not None:
    # read the file and display its contents
    file_contents = uploaded_file.read()

    conversation = json.loads(file_contents.decode("utf-8")) 

    # dropdowns to select the implementation type and model
    implementation_type = st.selectbox("Select Implementation Type", ["Regex", "ML"])
    model_type = st.selectbox("Select Classification Entity", ["Profanity Filter", "Privacy and Compliance Violation"])
    tab_analysis, tab_visualization = st.tabs(["Analysis", "Visualization"])

    # create a button to run the implementation
    run_button = st.button("Run Implementation")

    if run_button:
        with tab_analysis:
            if implementation_type == "Regex":
                if model_type == "Profanity Filter":
                    customer_profanity, agent_profanity = profanity.regex_implementation(conversation)
                    st.write("Customer Profanity Detected:", customer_profanity)
                    st.write("Agent Profanity Detected:", agent_profanity)
                elif model_type == "Privacy and Compliance Violation":
                    privacy_revealed, compliance_violation = privacy_violation.privacy_and_compliance_violation_regex_implementation(conversation)
                    st.write("Customer Privacy Revealed:", privacy_revealed)
                    st.write("Compliance Violation Detected:", compliance_violation)

            elif implementation_type == "ML":
                if model_type == "Profanity Filter":
                    customer_profanity, agent_profanity = profanity.ml_implementation(conversation)
                    st.write("Customer Profanity Detected:", customer_profanity)
                    st.write("Agent Profanity Detected:", agent_profanity)
                elif model_type == "Privacy and Compliance Violation":
                    privacy_revealed, compliance_violation = privacy_violation.privacy_and_compliance_violation_ml_implementation(conversation)
                    st.write("Customer Privacy Revealed:", privacy_revealed)
                    st.write("Compliance Violation Detected:", compliance_violation)
            else:
                st.write("Please select a valid implementation type and model.")

        with tab_visualization:
            silence_intervals, overtalk_intervals, total_duration, silence_percentage, overtalk_percentage = visual_analysis.analyze_call_timeline(conversation)
            st.write("Total Duration:", total_duration)
            st.write("Silence Percentage:", silence_percentage)
            st.write("Overtalk Percentage:", overtalk_percentage)

            fig_timeline, fig_metrics  = visual_analysis.plot_call_timeline(call_id=uploaded_file.name.split(".")[0],utterances=conversation,silence_intervals=silence_intervals,overtalk_intervals=overtalk_intervals, total_duration=total_duration,silence_percentage=silence_percentage, overtalk_percentage=overtalk_percentage)
            st.pyplot(fig_timeline)
            st.pyplot(fig_metrics)


else:
    st.write("Please upload a JSON file containing the conversation data.")
