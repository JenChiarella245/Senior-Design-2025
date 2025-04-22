import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askdirectory


def select_folder(prompt):
    # Hide the Tkinter root window and prompt the user to select a folder.
    Tk().withdraw()
    folder = askdirectory(title=prompt)
    return folder


# Select the input folder containing the .txt files and the output folder for generated images.
input_folder = select_folder("Select the folder containing the .txt files")
output_folder = select_folder("Select the output folder for the generated files")

# Ensure that the output folder exists.
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Create the SentimentIntensityAnalyzer object.
analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(file_path):
    # Open and read the file.
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Split the text into sentences using newline as delimiter.
    sentences = text.split('\n')

    positive_count = 0
    negative_count = 0

    # Iterate over each sentence.
    for sentence in sentences:
        # Split the sentence into words.
        words = sentence.split()
        for word in words:
            sentiment = analyzer.polarity_scores(word)
            if sentiment['compound'] > 0:
                positive_count += 1
            elif sentiment['compound'] < 0:
                negative_count += 1

    # Create a bar graph displaying the total counts.
    plt.figure(figsize=(6, 4))
    labels = ['Positive', 'Negative']
    counts = [positive_count, negative_count]
    colors = ['orange', 'blue']  # Positive words in orange, negative words in blue.
    plt.bar(labels, counts, color=colors)
    plt.title(f"Final Word Sentiment Counts for {os.path.basename(file_path)}")
    plt.xlabel("Sentiment")
    plt.ylabel("Word Count")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save the plot as a PNG file in the output folder.
    output_png = os.path.join(output_folder, os.path.basename(file_path).replace('.txt', '.png'))
    plt.savefig(output_png)
    plt.close()


# Process each .txt file in the input folder.
for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        file_path = os.path.join(input_folder, filename)
        analyze_sentiment(file_path)

print("Sentiment analysis complete. Files saved to:", output_folder)

