import requests
import json

# api

api_get_questions = "http://3.67.227.198:54321/api/Question/GetQuestionsByTestId/c5c056d6-0316-417a-b819-48a7e94cba2c"
api_post_answer = (
    "https://skill-matcher-api.liara.run/api/Questioner/InsertQuestionAnswer"
)
api_get_questionerId = "http://3.67.227.198:54321/api/Questioner/InsertUserId/"
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


def get_QuestionText(q, language):
    list_questionText = []
    for i in range(0, len(q)):
        list_questionText.append(q[i]["questionText"][language])
    return list_questionText


def get_QuestionType(q):
    list_questionType = []
    for i in range(0, len(q)):
        list_questionType.append(q[i]["type"])
    return list_questionType


def get_QuestionLevels(q):
    list_questionLevel = []
    for i in range(0, len(q)):
        list_questionLevel.append(q[i]["level"])
    return list_questionLevel


def get_OptionText(q, language):
    list_optionText = []
    for i in range(0, len(q)):
        options = q[i]["options"]
        option = []
        for j in range(0, len(options)):
            option.append(options[j][language])
        list_optionText.append(option)
    return list_optionText


questions = get_data_question(api_get_questions)

# Sort questions based on the 'level' key
# sorted_questions = sorted(questions, key=lambda x: x["level"])


def return_dataQuestion(language):
    questionText = get_QuestionText(questions, language)
    OptionText = get_OptionText(questions, language)
    typeText = get_QuestionType(questions)
    # print(data)
    return questionText, OptionText, typeText


def return_OptionText():
    questions = get_data_question(api_get)
    data = get_OptionText(questions)
    # print(data)
    return data


def get_QuestionerId(user_id):
    response = requests.post(api_get_questionerId + user_id)
    questioner_id = response.text.replace('"', "")

    return questioner_id


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
        user_DbId = get_userdata_Existed(telegramId)
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


def send_Questioner(QuestionerId, user_id, answer, idx):
    # print(questions[1])
    # QuestionerId = get_QuestionerId(user_id)
    # print(QuestionerId)
    json_data = {
        "id": QuestionerId,
        "userId": user_id,
        "questions": questions[idx],
        "answers": answer,
    }

    response = requests.put(api_post_answer, json=json_data)
    # Check the response
    if response.status_code == 200:
        print("Request was successful!")
        print(json.loads(response.text))
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
