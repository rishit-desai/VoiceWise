# VoiceWise

VoiceWise is a project designed to perform Analysis of Agent-Customer Conversations using Natural Language Processing (NLP) techniques. The project is built using Streamlit, a popular framework for building web applications in Python.
This README provides instructions for installation and environment setup.

## Installation

Follow these steps to set up the project:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/rishit-desai/VoiceWise
    cd VoiceWise
    ```
2. **Install Dependencies**:
    - For **Python** projects, create a virtual environment and install dependencies:
    - On Windows use `venv\Scripts\activate`
    ```bash
    
    python -m venv venv
    source venv/bin/activate  
    pip install -r requirements.txt
    ```

    

3. **Start the Application**:
    Run the following command to start the application:
    ```bash
    streamlit run main.py
    ```


## Visualization usage intrsuctions

Follow these steps to use the visualization features of the application:

1. **Create folder structure**:
    - Create a folder named `Data` in the root directory of the project.
    - Inside the `Data` folder, paste the `json` files you want to visualize.
    - The folder structure should look like this:
    ```
    VoiceWise
    ├── Data
    │   ├── file1.json
    │   ├── file2.json
    ```

2. **Install Dependencies**:
    - Ensure you have the required dependencies installed(jupyter). You can do this by running:
    ```bash
    pip install -r requirements.txt
    pip install jupyter
    ```
3. **Run the ipynb file**:
    - Open the `call_metrics_visualization.ipynb` file in Jupyter Notebook or Jupyter Lab.
    - Run the cells in the notebook to visualize the data from the JSON files.

## Additional Notes

- Ensure you have the required version of python installed (3.11.*). Check the `requirements.txt` for version details.