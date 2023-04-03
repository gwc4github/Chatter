import openai
from serpapi import GoogleSearch
# import requests
from bs4 import BeautifulSoup
import os


def generate_question(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{prompt}?",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    question = response.choices[0].text.strip()
    return question


def search_internet(query):
    params = {
        "q": query,
        # "location" : "Austin, Texas, United States",
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": "b237ead238a01a5de7f6ae79901c682a9dc1e3457959403a4ac8b261c4c39e36",
    }
    query = GoogleSearch(params)
    dictionary_results = query.get_dict()
    if 'answer_box' in dictionary_results and 'type' in dictionary_results['answer_box'] and dictionary_results['answer_box']['type'] == 'dictionary_results':
        # this is a dictionary result meaning a definition lookup. Different structure
        return (f"Definition: {dictionary_results['answer_box']['definitions'][0]}")

    if 'answer_box' in dictionary_results and 'snippet' in dictionary_results['answer_box']:
        return (f"{dictionary_results['answer_box']['snippet']}",
                f"{dictionary_results['answer_box']['about_page_link']}")

    if 'answer_box' in dictionary_results and 'answer' in dictionary_results['answer_box']:
        return (f"{dictionary_results['answer_box']['answer']}",
                f"{dictionary_results['answer_box']['link']}")
    else:
        return ("I couldn't find any relevant information.")



def chat_gpt4_bot():
    print("Welcome to the ChatGPT-4 Bot! Feel free to ask me anything or type 'quit' to exit.")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "quit":
            break

        user_input_rails = "?  If you don't know just respond with 'I don't know'"
        question = generate_question(user_input+user_input_rails)
        if question == "I don't know.":
            # or 'At this time,' in question or 'not yet' in question or 'too early' in question:
            # This question is asking about a futue event, so we can't answer it
            # so we'll search the internet instead.
            print('Hmmmm... seeking guidance from a higher power... (searching the internet...)')
            google_answer = search_internet(user_input)
            if google_answer == "I couldn't find any relevant information.": # no answer found
                print("ChatGPT Bot: I couldn't find any relevant information.")
                continue
            source = google_answer[1]
            answer = google_answer[0]
        else:
            answer = question
            source = 'ChatGPT Bot'
        print(f"ChatGPT Bot: {answer}")
        print(f"Source: {source}")


if __name__ == "__main__":
    # search_internet('what is google')
    openai.api_key = os.getenv('OPENAI_API_KEY')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

    chat_gpt4_bot()
