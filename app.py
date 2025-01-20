import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from sklearn.linear_model import LinearRegression
import numpy as np
import yfinance as yf
import tweepy

# Sidebar Navigation
st.sidebar.title("App Navigation")
app_mode = st.sidebar.selectbox("Choose a section", ["Home", "Weather App", "Data Input & Statistics", "CSV Upload", "Stock Price", "News", "Twitter"])

# Initialize an empty DataFrame
df = pd.DataFrame()

# Home Section
if app_mode == "Home":
    st.title("Welcome to My First Streamlit App!")
    st.write("This is the home page where you can navigate to other sections.")

# Weather App Section
elif app_mode == "Weather App":
    st.title("Real-Time Weather App")
    city = st.text_input("Enter the city name:", value="Accra")

    if st.button("Get Weather"):
        try:
            api_key = "6d29d5fb064ce1bcf87588d5b867dce7"  # Replace with your API key
            city = city.strip()
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city},GH&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                weather = data["weather"][0]["description"]
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]

                st.subheader(f"Weather in {city.title()}:")
                st.write(f"Condition: {weather.capitalize()}")
                st.write(f"Temperature: {temp}°C")
                st.write(f"Humidity: {humidity}%")
            else:
                st.error(f"City '{city}' not found. Please try again.")

        except Exception as e:
            st.error(f"Error fetching weather data: {e}")

# Data Input & Statistics Section
elif app_mode == "Data Input & Statistics":
    st.title("User Input and Basic Statistics")
    
    # User Input Section
    st.subheader("Enter your data:")
    data_input = st.text_area("Paste your numbers (comma-separated):", value="10, 20, 30, 40")

    # Chart Selection
    chart_type = st.selectbox("Choose Chart Type:", ["Bar Chart", "Line Chart", "Pie Chart"])

    # Data Processing
    if st.button("Calculate Statistics and Predict Next Value"):
        try:
            # Process user input and convert to a list of numbers
            numbers = [float(x.strip()) for x in data_input.split(",") if x.strip()]
            
            if not numbers:
                st.error("No valid numbers found. Please enter numbers separated by commas.")
            else:
                df = pd.DataFrame(numbers, columns=["Values"])

                # Display DataFrame
                st.subheader("Your Data:")
                st.dataframe(df)

                # Calculate and display basic statistics
                mean_val = df["Values"].mean()
                median_val = df["Values"].median()
                max_val = df["Values"].max()
                min_val = df["Values"].min()

                st.subheader("Basic Statistics:")
                st.write(f"Mean: {mean_val}")
                st.write(f"Median: {median_val}")
                st.write(f"Maximum: {max_val}")
                st.write(f"Minimum: {min_val}")

                # Linear Regression Prediction (Predict the next value)
                X = np.array(range(len(numbers))).reshape(-1, 1)  # Feature: position of the number
                y = np.array(numbers)  # Target: the numbers themselves

                model = LinearRegression()
                model.fit(X, y)

                # Predict the next value (next position)
                next_position = np.array([[len(numbers)]])
                next_value = model.predict(next_position)[0]

                st.subheader("Linear Regression Prediction:")
                st.write(f"Predicted next value: {next_value:.2f}")

                # Display the chosen chart
                st.subheader(f"{chart_type} of Values")
                fig, ax = plt.subplots()

                if chart_type == "Bar Chart":
                    ax.bar(df.index, df["Values"], color='skyblue')
                elif chart_type == "Line Chart":
                    ax.plot(df.index, df["Values"], marker='o', color='skyblue')
                elif chart_type == "Pie Chart":
                    ax.pie(df["Values"], labels=df.index, autopct='%1.1f%%', startangle=90)
                ax.set_title(f"{chart_type} of User Input Values")
                st.pyplot(fig)

                # Visualize the Linear Regression Line
                ax.plot(X, model.predict(X), color='red', label='Regression Line')
                ax.legend()

                # Export Data as CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="user_data.csv",
                    mime="text/csv"
                )

                # Export Chart as PNG
                chart_img = "chart.png"
                fig.savefig(chart_img)
                st.download_button(
                    label="Download Chart",
                    data=open(chart_img, "rb").read(),
                    file_name="chart.png",
                    mime="image/png"
                )

        except ValueError as ve:
            st.error(f"Input Error: {ve}. Please enter valid numbers separated by commas.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# CSV Upload Section
elif app_mode == "CSV Upload":
    st.subheader("Upload Your CSV File:")
    uploaded_file = st.file_uploader("Choose a file", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.subheader("Uploaded Data:")
            st.dataframe(df)

            st.subheader("Basic Statistics of Uploaded Data:")
            st.write(df.describe())

            # Export Data as CSV
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="uploaded_data.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"Error loading CSV file: {e}")

# Stock Price Section
elif app_mode == "Stock Price":
    st.title("Real-Time Stock Price")
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):", value="AAPL")

    if st.button("Get Stock Price"):
        try:
            stock_data = yf.download(ticker, period="1d", interval="1m")
            st.subheader(f"Stock Price for {ticker}:")
            st.write(stock_data.tail())  # Show the latest data
            st.line_chart(stock_data['Close'])
        except Exception as e:
            st.error(f"Failed to fetch stock data for {ticker}: {e}")

# News Section
elif app_mode == "News":
    st.title("Latest News")
    topic = st.text_input("Enter Topic (e.g., Technology, Health):", value="Technology")

    if st.button("Get News"):
        try:
            api_key = "YOUR_NEWSAPI_KEY"  # Replace with your API key
            url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200 and data["status"] == "ok":
                st.write(f"**Latest News on {topic}:**")
                for article in data["articles"][:5]:  # Display top 5 articles
                    st.subheader(article["title"])
                    st.write(f"Source: {article['source']['name']}")
                    st.write(f"Published: {article['publishedAt']}")
                    st.write(f"[Read more]({article['url']})")
            else:
                st.error("Failed to fetch news.")
        except Exception as e:
            st.error(f"Error fetching news: {e}")

# Twitter Section
elif app_mode == "Twitter":
    st.title("Latest Tweets")
    hashtag = st.text_input("Enter Hashtag (e.g., #AI, #Tech):", value="#AI")

    if st.button("Get Tweets"):
        try:
            # Twitter API keys
            consumer_key = "YOUR_CONSUMER_KEY"  # Replace with your keys
            consumer_secret = "YOUR_CONSUMER_SECRET"
            access_token = "YOUR_ACCESS_TOKEN"
            access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

            auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
            api = tweepy.API(auth)

            tweets = api.search_tweets(q=hashtag, lang="en", count=5)
            st.write(f"**Recent Tweets for {hashtag}:**")
            for tweet in tweets:
                st.write(f"- {tweet.user.screen_name}: {tweet.text}")
                st.write(f"Link: [View Tweet](https://twitter.com/{tweet.user.screen_name}/status/{tweet.id})")
        except tweepy.TweepError as e:
            st.error(f"Failed to fetch tweets: {e}")
