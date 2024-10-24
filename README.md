# NutriScan 🍽️

**NutriScan** is a Streamlit-based application that helps users manage their nutrition effortlessly. By analyzing food images, tracking calorie intake, offering personalized recipe suggestions, and calculating daily calorie recommendations, NutriScan ensures that users can stay on top of their dietary habits. Additionally, it features an interactive calendar to visualize calorie data over time.

## Features

- **Food Image Analysis:** Upload food images to get detailed nutritional information using image analysis.
- **Calorie Tracking:** Keep track of your daily calorie intake and monitor your progress.
- **Recipe Suggestions:** Get personalized recipes based on your analyzed food items.
- **Daily Calorie Recommendations:** Calculate your recommended daily calorie intake based on your age, gender, weight, height, and activity level.
- **Interactive Calendar:** View your calorie intake and progress in a visual format with an interactive calendar.

## Technologies

- **Streamlit:** Used as the framework for building the web app.
- **Python (OpenAI, Foodvisor, SERP APIs):** For handling image analysis, generating insights, and providing recipe recommendations.
- **SQL:** For database management to store and retrieve user data.
- **Pandas:** For data manipulation and analysis.

## Installation

To run this project locally, follow these steps:

1. Clone this repository:

   ```bash
   git clone https://github.com/ThienAn783/NutriScan.git
   ```

2. Navigate to the project directory:

   ```bash
   cd NutriScan
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.streamlit/secrets.toml` file and add your API keys:

   ```toml
   [api_credentials]
   FOODVISOR_API_KEY = "your_foodvisor_api_key"
   SERPAPI_API_KEY = "your_serpapi_api_key"
   OPENAI_API_KEY = "your_openai_api_key"
   ```

5. Run the app:

   ```bash
   streamlit run app.py
   ```

## Usage

1. Open the app in your browser (usually runs on `localhost:8501`).
2. Upload an image of food to analyze its nutritional content.
3. Track your daily calorie intake and monitor your progress using the calorie tracker.
4. Get recipe suggestions based on the analyzed food items.
5. Calculate your daily calorie recommendations by inputting personal data.
6. View your calorie data using the interactive calendar.

## Contributions

Contributions are welcome! If you'd like to contribute, please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or suggestions, feel free to reach out.

---
