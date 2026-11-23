import json
import csv
from sys import excepthook

print()
print ("anime personality tracker")
print("Discover which anime character matches your personality!")
print()

def load_question():
    try:
        with open("questions.json", "r") as file:
            questions = json.load(file)
        return questions
    except FileNotFoundError:
        print("Something went wrong when loading the questions.")
        return []

def load_characters():
    characters = []

    try:
        with open("characters.csv", "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                characters.append(row)

        return characters

    except FileNotFoundError:
        print("Something went wrong when loading the characters.")
        return []



def create_scores():
    scores = {
        "Determination": 0,
        "Intelligence": 0,
        "Confidence": 0,
        "Loyalty": 0,
        "Compassion": 0,
        "Adventurousness": 0
    }

    return scores

def run_quiz(questions, scores):
    for question in questions:
        print("\n" + question["question"])

        for answer in question["answers"]:
            print(answer["option"] + ". " + answer["text"])

        choice = input("Enter your answer (A, B, C or D): ").upper()

        if choice in ["A", "B", "C", "D"]:
            for answer in question["answers"]:
                if choice == answer["option"]:
                    scores[answer["trait"]] += answer["points"]
        else:
            print("Invalid choice. Moving to the next question.")

    return scores

def find_best_trait(scores):
    highest_score = 0
    best_trait = ""

    for trait in scores:
        if scores[trait] > highest_score:
            highest_score = scores[trait]
            best_trait = trait

    return best_trait

def find_character(best_trait, characters):
    for character in characters:
        if character["Trait"] == best_trait:
            return character

    return None

def display_result(character):
    print("your anime MATCH IS.....")

    if character:
        print("Character:", character["Character"])
        print("Anime:", character["Anime"])
        print("Personality:", character["Trait"])
        print("Description:", character["Description"])
    else:
        print("Sorry, no matching character was found.")


def save_result(character):
    try:
        file = open("results.txt", "a")

        file.write("Character: " + character["Character"] + "\n")
        file.write("Anime: " + character["Anime"] + "\n")
        file.write("Personality: " + character["Trait"] + "\n")
        file.write("Description: " + character["Description"] + "\n\n")

        file.close()
        print("Result saved successfully!")

    except FileNotFoundError:
        print("Error saving result.")



def main():
    questions = load_question()
    characters = load_characters()
    scores = create_scores()

    if questions and characters:
        run_quiz(questions, scores)

        best_trait = find_best_trait(scores)
        character = find_character(best_trait, characters)

        display_result(character)

        if character:
           save_result(character)

    else:
        print("Quiz could not start.")


main()