import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import seaborn as sns

def app():
    st.sidebar.title("Social Media Chat Analyzer")

    st.markdown(
        """
        <style>
        /* Main app background */
        .stApp {
            background-image: url('https://www.itl.cat/pngfile/big/0-596_originalhd-whatsapp-background-wallpapers-wallpaper.jpg');  /* Add your image URL or path here */
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            height: 100vh;
            color: white !important;
        }

        .stAppHeader{
            background-color: black;
        }

        /* Sidebar background */
        section[data-testid="stSidebar"] {
            background-color: #075e54;
            color: white;
        }

        /* Adjust sidebar title and widget label color */
        .css-1d391kg, .css-qbe2hs {
            color: white !important;
        }

         .st-title {
        color: white;
        }
        .st-header {
            color: white;
            font-size: 2.5em;  /* Larger font size */
            font-weight: bold;
        }
        .st-subheader {
            color: white;
        }
        .st-markdown {
            color: white;
        }

        /* Optional: Change headers if needed */
        # h1, h2, h3, h4, h5 {
        #     color: #075e54;
        # }
        </style>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.sidebar.file_uploader("Choose a file")

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        mydata = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(mydata)


        # Fetch unique users
        user_list = df['user'].unique().tolist()
        if "group_notification" in user_list:
            user_list.remove("group_notification")
        user_list.sort()
        user_list.insert(0, "Overall")

        selected_user = st.sidebar.selectbox("Show Analysis with respect to", user_list)

        # Show the 'Show Analysis' button only after the file is uploaded
        show_analysis_button = st.sidebar.button("Show Analysis", key="show_analysis_button")


        if show_analysis_button:
            # Display analysis after the button is clicked
            st.title("Top Statistics")    
            num_messages, words, num_media_msg, links = helper.fetch_stats(selected_user, df)

            col1, col2, col3, col4 = st.columns(4)

            with col1:  
                st.header("Total Messages")
                st.title(num_messages)
            with col2:
                st.header("Total Words")
                st.title(words)
            with col3:
                st.header("Media Shared")
                st.title(num_media_msg)
            with col4:
                st.header("Links Shared")
                st.title(links)
            
            # Monthly Timeline
            st.title("Monthly Activity Timeline")
            timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 6))
            palette = sns.color_palette("hsv", 1)
            sns.lineplot(x='time', y='message', data=timeline, palette=palette, linewidth=2.5)

            plt.xticks(rotation='vertical')
            plt.xlabel('Time', fontsize=15)
            plt.ylabel('Message', fontsize=15)

            st.pyplot(fig)

            # Daily Timeline
            st.title("Daily Activity Timeline")
            d_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 6))

            # Using a bright color palette
            palette = sns.color_palette("hsv", 1)

            sns.lineplot(x='only_date', y='message', data=d_timeline, palette=palette, linewidth=2.5)

            plt.xticks(rotation='vertical')
            plt.xlabel('Time', fontsize=15)
            plt.ylabel('Message', fontsize=15)
            st.pyplot(fig)

            # Activity Map 
            st.title("Activity Map")
            col1, col2 = st.columns(2)

            with col1: 
                st.header("Most Busy Day")
                busy_day = helper.week_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.header("Most Busy Month")
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            # Busiest Users in Group (if 'Overall' is selected)
            if selected_user == 'Overall':
                st.title('Most Busy Users')

                x, new_df = helper.most_busy_user(df)

                fig, ax = plt.subplots()

                col1, col2 = st.columns(2)

                with col1:
                    colors = cm.viridis(np.linspace(0, 1, len(x.index)))  # Create a colormap
                    ax.bar(x.index, x.values, color=colors)  # Use the colormap for the bars
                    plt.title('User Activity')  # Add a title
                    plt.xlabel('User')  # Add x-axis label
                    plt.ylabel('Activity Count')  # Add y-axis label
                    plt.xticks(rotation="vertical")
                    plt.grid(True)  # Add grid lines
                    st.pyplot(fig)

                with col2:
                    st.write('## User Activity Data')  # Add a title to the DataFrame
                    st.dataframe(new_df.style.highlight_max(color='lightgreen'))  # Highlight max values

                # Weekly Activity Heatmap
                st.title("Weekly Activity Map")
                user_heatmap = helper.activity_heatmap(selected_user, df)
                fig, ax = plt.subplots()

                sns.heatmap(user_heatmap, cmap='viridis', linewidths=0.001, linecolor='white', cbar_kws={'label': 'Activity Level'}, ax=ax)
                plt.xlabel('Hour of the Day', fontsize=10)
                plt.ylabel('Day of the Week', fontsize=10)

                st.pyplot(fig)

            # Word Cloud
            st.title("Word Cloud for Frequent Words")
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

            # Most Common Words
            most_common_df = helper.most_common_words(selected_user, df)

            fig, ax = plt.subplots()

            ax.barh(most_common_df["Words"], most_common_df["Frequency"])
            plt.xticks(rotation='vertical')
            st.title("Most Common Words")
            st.pyplot(fig)  

            # Emoji Analysis
            emoji_df = helper.emoji_helper(selected_user, df)
            st.title("Emoji Analysis")

            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df["Frequency"].head(), labels=emoji_df["Emoji"].head(), autopct="%0.2f")
                st.pyplot(fig)

            # User Sentiment Analysis
            st.title("Sentiment Analysis")

            user_sentiments = helper.analyze_sentiment(selected_user, df)

            # If the selected user is 'Overall', display sentiment for all users
            if selected_user == 'Overall':
                overall_sentiment = {key: sum([user[key] for user in user_sentiments.values()])/len(user_sentiments) for key in ['pos', 'neu', 'neg', 'compound']}
                st.subheader("Overall")

                # Create a horizontal bar chart for the overall sentiment scores
                fig, ax = plt.subplots()
                ax.barh(list(overall_sentiment.keys()), list(overall_sentiment.values()), color=['green' if v >= 0 else 'red' for v in overall_sentiment.values()])
                ax.set_xlabel('Score')
                ax.set_title('Overall sentiment scores')
                st.pyplot(fig)
            else:
                # If the selected user exists in the sentiment analysis results
                if selected_user in user_sentiments:
                    sentiment_scores = user_sentiments[selected_user]

                    st.subheader(f"User: {selected_user}")

                    # Create a horizontal bar chart for the sentiment scores
                    fig, ax = plt.subplots()
                    ax.barh(list(sentiment_scores.keys()), list(sentiment_scores.values()), color=['green' if v >= 0 else 'red' for v in sentiment_scores.values()])
                    ax.set_xlabel('Score')
                    ax.set_title(f'Sentiment scores for {selected_user}')
                    st.pyplot(fig)
                else:
                    st.write(f"No sentiment analysis results for {selected_user}")

            ## Final results for the sentiment analysis
            sentiment = helper.sentiment_score(user_sentiments, selected_user)
            st.subheader(f"The sentiment of {selected_user} is {sentiment}")

    else:
        # Display the title and logo before uploading the file
        st.markdown("""
            <h1 style="display: flex; align-items: center; justify-content: center; color: white">
                Upload Your Whatsapp Chat
                <img src="https://logo-download.com/wp-content/data/images/png/WhatsApp-logo.png" width="100" style="margin-right: 10px;">
            </h1>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
