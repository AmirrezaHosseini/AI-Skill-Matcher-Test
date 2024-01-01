import requests
import json

# api

api_get = "https://skill-matcher.liara.run/api/Question/GetQuestionsByLevelAndTestId/d0680d38-90c7-480f-89f8-e8b8bd8ff3cc/1"
api_post = "https://skill-matcher-api.liara.run/api/Questioner/InsertQuestionAnswer"
api_get_questionerId = "https://skill-matcher-api.liara.run/api/Questioner/InsertUserId/3fa85f64-5717-0000-b3fc-2c963f66afa6"
headers = {
    "Content-Type": "application/json",  # Include this if your API requires authentication
}


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
        list_questionText.append(q[i]["questionText"]["english"])
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
            option.append(options[j]["english"])
        list_optionText.append(option)
    return list_optionText


def return_dataQuestion():
    questions = get_data_question(api_get)
    questionText = get_QuestionText(questions)
    OptionText = get_OptionText(questions)
    # typeText = get_QuestionType(questions)
    # print(data)
    return questionText, OptionText


def return_OptionText():
    questions = get_data_question(api_get)
    data = get_OptionText(questions)
    # print(data)
    return data


def get_QuestionerId():
    response = requests.post(api_get_questionerId)

    return response.text


def post_User(name, telegramId):
    json_data = {
        "name": name,
        "preferredLanguage": 0,
        "telegramId": telegramId,
    }
    response = requests.post(
        "https://skill-matcher.liara.run/api/User/InsertFirstInfoBot", json=json_data
    )
    # Check the response
    if response.status_code == 200:
        print("Request was successful!")
        user_DbId = json.loads(response.text)["id"]
    elif response.status_code == 400:
        print("This TelegramID already exists")
        return get_userdata_Existed(telegramId)
    else:
        print(f"Error: {response.status_code}")

    return user_DbId


def get_userdata_Existed(telegramId):
    response = requests.get(
        f"https://skill-matcher.liara.run/api/User/GetUserInfoBot/{telegramId}"
    )
    # Check the response

    if response.status_code == 200:
        print("Request was successful!")
        user_DbId = json.loads(response.text)["id"]
    else:
        print(f"Error: {response.status_code}")

    return user_DbId


def send_Questioner(answer):
    print(questions[0])
    json_data = {
        "id": "da0883cb-fad3-44f4-ae43-9e4e701334a8",
        "userId": "3fa85f64-5717-0000-b3fc-2c963f66afa6",
        "questions": questions[0],
        "answers": answer,
    }
    response = requests.post(api_post, json=json_data)
    # Check the response
    if response.status_code == 200:
        print("Request was successful!")
        print(response.json())
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


# print(questions[1]["questionText"]["English"])
# questions = get_data_question(api_get)
# data = get_questionText(questions)
# print(data)
# questions = get_data_question(api_get)
# data = get_OptionText(questions)
# print(data)
