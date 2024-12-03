### Vietnamese AI Chatbot Project

This project is a Vietnamese AI chatbot aimed to provide various functionalities through a simple web interface. Below is a detailed explanation of each file in the project and its usage:

#### Files and their functionalities:

1. **all_cards_data.json**
   - **Description**: This file contains metadata about various banking cards, including features, benefits, terms, and FAQs.
   - **Usage**: It is used to store and retrieve information about banking cards for the chatbot to respond to user queries related to banking products.

2. **app.py**
   - **Description**: This is the main application file for the Flask server that handles incoming chat requests and returns responses.
   - **Usage**: Start the server by running this file. It validates JSON input, processes the user message, generates a response using the chatbot, and returns the response to the client.

3. **chatbot.py**
   - **Description**: This file contains the logic for initializing and testing the chatbot model. It includes functions for diagnosing the setup, downloading the model, and testing the model loading.
   - **Usage**: Use this file to set up the Hugging Face model, diagnose issues, and ensure the chatbot model is functioning correctly.

4. **index.html**
   - **Description**: This file contains the HTML and JavaScript for the user interface of the chatbot. It includes a chat box and handles sending user messages to the server and displaying responses.
   - **Usage**: Open this file in a web browser to interact with the chatbot. It uses Axios to send messages to the Flask server and displays the chatbot's responses in the chat box.

5. **requirement.txt**
   - **Description**: This file lists all the necessary Python packages required to run the project.
   - **Usage**: Install the required packages using the command `pip install -r requirement.txt` to set up the project environment.

#### Usage Instructions:

1. **Setting up the environment**:
   - Clone the repository: `git clone https://github.com/quangtrancst/Chatbot_AI.git`
   - Navigate to the project directory: `cd Chatbot_AI`
   - Install the dependencies: `pip install -r requirement.txt`

2. **Running the server**:
   - Start the Flask server: `python app.py`
   - The server will run on `http://127.0.0.1:5000`

3. **Interacting with the chatbot**:
   - Open `index.html` in a web browser.
   - Type your message in the input box and click "Gửi" to send the message.
   - The chatbot's response will be displayed in the chat box.

By following these instructions, you will be able to set up and interact with the Vietnamese AI chatbot.
