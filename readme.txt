1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```
    (Replace `your-username/your-repo-name.git` with your actual repository URL.)

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

    * **On Linux/macOS:**
        ```bash
        source venv/bin/activate
        ```
    * **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

### API Key Configuration

This project uses the OpenAI API for its language model capabilities. You need to provide your OpenAI API key.

1.  **Get your OpenAI API Key:** If you don't have one, you can obtain it from the [OpenAI platform](https://platform.openai.com/account/api-keys).

2.  **Create a `.env` file:** In the root directory of your project (the same directory as `streamlit_app.py`), create a file named `.env`.

3.  **Add your API key to the `.env` file:**

    ```
    OPENAI_API_KEY='your_openai_api_key_here'
    ```
    Replace `your_openai_api_key_here` with your actual OpenAI API key.

    **Note:** For deployment (e.g., to Streamlit Community Cloud), it's recommended to set your API key directly as a secret in the deployment platform's settings rather than including the `.env` file in your repository.

## Running the Application

Once you have completed the setup, you can run the Streamlit application:

1.  **Ensure your virtual environment is active.**
2.  **Run the Streamlit app:**

    ```bash
    streamlit run streamlit_app.py
    ```

    This command will open the application in your default web browser, usually at `http://localhost:8501`.