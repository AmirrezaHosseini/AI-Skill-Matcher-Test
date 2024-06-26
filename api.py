import requests
import json

# api
path = "https://skillmatcher.liara.run/api/"

api_get_questions = (
    path
    + "Question/GetQuestionsByLevelAndTestId/5751f4a7-b2b5-4602-a0a7-22b16913246b/2"
)
api_post_answer = path + "Questioner/InsertQuestionAnswer"
api_insert_user = path + "User/InsertFirstInfoBot"
api_get_questionerId = path + "Questioner/InsertUserId/"
api_create_report = path + "Questioner/CreateReport/"
headers = {
    "Content-Type": "application/json",  # Include this if your API requires authentication
}
api_get_workflows = "http://127.0.0.1:5000/api/GetWorkflows/"
api_InsertOtherinfo = "User/InsertOtherinfo"


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


def get_Optionlist(q, number):
    list_optionText = []
    for i in range(0, len(q)):
        options = q[i]["options"]
        for j in number:
            list_optionText.append(options[j])
    return list_optionText


# questions = get_data_question(api_get_questions)

# Sort questions based on the 'level' key
# sorted_questions = sorted(questions, key=lambda x: x["level"])


def return_dataQuestion(language, url):
    global questions
    questions = get_data_question(path + "Question/GetQuestionsByLevelAndTestId/" + url)
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
    global telgid
    json_data = {
        "name": name,
        "preferredLanguage": 0,
        "telegramId": telegramId,
    }
    telgid = telegramId
    response = requests.post(path + "User/InsertFirstInfoBot", json=json_data)
    user_DbId = ""
    # Check the response
    if response.status_code == 200:
        print("Request was successful!")
        user_DbId = json.loads(response.text)["id"]
    elif response.status_code == 402:
        print("This TelegramID already exists")
        user_DbId = get_userdata_Existed(telegramId)
    else:
        print(f"Error: {response.status_code}")

    return user_DbId


def send_info(age, job, telegramid):
    json_data = {
        "age": age,
        "job": job,
    }
    response = requests.post(
        path + api_InsertOtherinfo + f"?telegramId={telegramid}", json=json_data
    )
    if response.status_code == 200:
        print("send was successful!")
    else:
        print(f"Error: {response.status_code}")


def get_userdata_Existed(telegramId):
    response = requests.get(path + f"User/GetUserInfoBot/{telegramId}")
    # Check the response

    if response.status_code == 200:
        print("Request was successful!")
        user_id = json.loads(response.text)["id"]
    else:
        print(f"Error: {response.status_code}")

    return user_id


def send_Questioner(user_id, QuestionerId, options, lan, testid):
    # print(questions[1])
    # QuestionerId = get_QuestionerId(user_id)
    # print(QuestionerId)
    json_data = {
        "answers": get_Optionlist(questions, options),
        "optionNo": options,
        "questions": questions,
    }

    response = requests.put(
        f"{api_create_report}{user_id}/{QuestionerId}?testId={testid}&level=2",
        json=json_data,
    )
    # Check the response
    if response.status_code == 200:
        print("Request was successful!")
        re = json.loads(response.text)
        return re[0][lan]
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def get_workflows():
    # url = api_get_workflows
    try:
        response = {
            "workflowName": "test 1",
            "status": "not active",
            "routin": [
                {
                    "id": 1,
                    "tests": ["5751f4a7-b2b5-4602-a0a7-22b16913246b/2"],
                    "prompt": {
                        "yes": "b162f0cb-4c71-4f6f-afab-a80cda394e72",
                        "no": "b162f0cb-4c71-4f6f-afab-a80cda394e72",
                    },
                }
            ],
        }
        response.raise_for_status()
        return json.loads(response)
    except requests.exceptions.RequestException as e:
        print(e)
        return


# print(questions[1]["questionText"]["English"])
# questions = get_data_question(api_get)
# data = get_questionText(questions)
# print(data)
# questions = get_data_question(api_get)
# data = get_OptionText(questions)
# print(data)
