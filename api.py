import requests
import json

# api

api_get = "https://skill-matcher-api.liara.run/api/Question/GetQuestionsByLevelAndTestId/ef3f2bee-a91a-487f-9f4b-83aeb1e7a3df/1"


# Define the function to send a GET request
def get_data_question(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return json.loads(response.text)
    except requests.exceptions.RequestException as e:
        print(e)
        return


# Define the function to send a POST request
def send_post_request(url, data):
    try:
        headers = {"Content-type": "application/json"}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        return json.loads(response.text)
    except requests.exceptions.RequestException as e:
        print(e)
        return None


def get_QuestionText(q):
    list_questionText = []
    for i in range(0, len(q)):
        list_questionText.append(q[i]["questionText"]["English"])
    return list_questionText


def get_QuestionType(q):
    list_questionType = []
    for i in range(0, len(q)):
        list_questionType.append(q[i]["type"])
    return list_questionType


def get_OptionText(q):
    list_optionText = []
    for i in range(0, len(q)):
        options = q[i]["options"]
        option = []
        for j in range(0, len(options)):
            option.append(options[j]["optionText"]["English"])
        list_optionText.append(option)
    return list_optionText


def return_questionText():
    questions = get_data_question(api_get)
    questionText = get_QuestionText(questions)
    OptionText = get_OptionText(questions)
    typeText = get_QuestionType(questions)
    # print(data)
    return questionText, OptionText, typeText


def return_OptionText():
    questions = get_data_question(api_get)
    data = get_OptionText(questions)
    # print(data)
    return data


# print(questions[1]["questionText"]["English"])
# questions = get_data_question(api_get)
# data = get_questionText(questions)
# print(data)
# questions = get_data_question(api_get)
# data = get_OptionText(questions)
# print(data)
