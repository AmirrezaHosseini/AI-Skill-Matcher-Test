from asyncore import dispatcher
from typing import final
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler,
)
import telegram.error

import api

##### get data  #####


# bot identity
TOKEN: final = "6835505632:AAFJ9Auz7wSS3R-3e89FKIXBQv3OeIEuJHY"
BOT_USERNAME: final = "@AI_Skill_MatcherBot"
# TOKEN: final = "6650488420:AAFayPXrcyuBaJ0HX8upU2CkFnp3AZLUVu0"
# BOT_USERNAME: final = "@personaPathTestBot"

# Define the questions and answer options
# questions = ["What is your name?", "What is your age?", "What is your favorite color?"]
# answer_options = [
#     ["Alice", "Bob", "Charlie"],
#     [],
#     ["Red", "Green", "Blue"],
# ]
# question_types = ["0", "0", "1"]

user_username = ""
full_name = ""
# id save in DataBase
user_id = ""

# Define states for conversation
FIRST, SECOND = range(2)


# answer_options = [
#     [
#         "1) Strongly Disagree",
#         "2) Disagree",
#         "3) Neither Agree nor Disagree",
#         "4) Agree",
#         "5) Strongly Agree",
#     ],
#     [
#         "1) Strongly Disagree ",
#         "2) Disagree ",
#         "3) Neither Agree nor Disagree",
#         "4) Agree",
#         "5) Strongly Agree",
#     ],
# ]
# questions = [
#     "I usually prefer group work and get energy from others. I have many friends and share my personal information easily with others. I usually take the lead in work and activities and building relationships. ",
#     "I am independent and sometimes shy. I learn better through reflection and mental exercise. I rarely share my personal information with others. I listen more and talk less. I tend to work individually or at most with the cooperation of two or three people.",
#     "write your opinion learn better through reflection and mental exercise ",
# ]

ranged_option = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("English", callback_data="english"),
            InlineKeyboardButton("فارسی", callback_data="persian"),
        ]
    ]
    user = update.message.from_user
    user_id = user.id
    user_first_name = user.first_name
    user_last_name = user.last_name
    user_username = user.username
    context.user_data["user_username"] = user_username
    full_name = (
        f"{user_first_name} {user_last_name}" if user_last_name else user_first_name
    )
    # context.user_data["user_id"] = api.post_User(full_name, user_username)
    context.user_data["user_id"] = "c7951c1f-6ca9-44d7-aaf6-54a7a845a82e"
    print(
        f"User Information:\nID: {user_id}\nFull Name: {full_name}\nUsername: {user_username}"
    )
    # context.user_data["user_id"] = api.post_User(full_name, user_username)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hi ! I'm AI_Skill_Matcher .\n Please Choose Your Language",
        reply_markup=reply_markup,
    )


async def language_selected(update: Update, context):
    # Extract the selected language from the callback data
    context.user_data["language"] = update.callback_query.data
    print(context.user_data["language"])

    # Call the new_test function with the selected language
    await set_flow(update, context)


async def set_flow(update: Update, context):
    context.user_data["workflows"] = api.get_workflows()
    # if context.user_data["language"] == "persian":
    #     keyboard = [
    #         [
    #             InlineKeyboardButton(" MBTI تست ", callback_data="mbti"),
    #             InlineKeyboardButton("تست مهارت شناسی ", callback_data="skill"),
    #             InlineKeyboardButton("تست شخصیت شناسی ", callback_data="personality"),
    #         ]
    #     ]
    #     message = "تست مورد نظر خود را انتخاب کنید "
    # elif context.user_data["language"] == "english":
    #     keyboard = [
    #         [
    #             InlineKeyboardButton("Test MBTI ", callback_data="mbti"),
    #             InlineKeyboardButton("Test Skill Matcher", callback_data="skill"),
    #             InlineKeyboardButton("Test Personality", callback_data="personality"),
    #         ]
    #     ]
    #     message = " Select the test you want to do it "
    keyboard = [
        [
            InlineKeyboardButton(
                f"{idx + 1}) {workflow['workflowName']}",
                callback_data=f"{idx} workflow",
            )
        ]
        for idx, workflow in enumerate(context.user_data.get("workflows", []), start=0)
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text(
        " Select the test you want to do it ",
        reply_markup=reply_markup,
    )


async def workflow_test(update: Update, context):
    print(" work flow select")
    workflow_idx = int(update.callback_query.data.split(" ")[0])
    # context.user_data["workflows"]s
    context.user_data["flow"] = context.user_data["workflows"][workflow_idx]
    keyboard = [
        [
            InlineKeyboardButton("Previous Result", callback_data="previous_results"),
            InlineKeyboardButton("New Test", callback_data="new_test"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    # Check if the callback query originated from a message
    if update.callback_query and update.callback_query.message:
        await update.callback_query.message.edit_text(
            "If You want assistance, Select 'New test'",
            reply_markup=reply_markup,
        )
    else:
        await update.message.reply_text(
            "If You want assistance, Select 'New test'",
            reply_markup=reply_markup,
        )
    # await show_question(update, context)


async def handle_flow(update: Update, context):
    context.user_data["for"] = 0
    print(context.user_data["flow"]["routin"])
    routin = context.user_data["flow"]["routin"]
    test = routin[0]["tests"][0]
    context.user_data["testid"] = test.split("/")[0]
    await new_test(update, context, test)

    # if context.user_data["for"] == len(routin[0]["tests"]):
    #     context.user_data["for"] = 0
    #     await prompt(update, context)


async def routin(update: Update, context, idx):
    context.user_data["for"] = 0
    print(context.user_data["flow"]["routin"])
    routin = context.user_data["flow"]["routin"]
    for test in routin[idx]["tests"]:
        context.user_data["testid"] = test
        await new_test(update, context, test)

    # if context.user_data["for"] == len(routin[0]["tests"]):
    #     context.user_data["for"] = 0
    #     await prompt(update, context)


async def ask_question(update: Update, context):
    print("ask    ----  ")
    # if update.callback_query:
    # await update.callback_query.answer()
    if "question1" not in context.user_data:
        await update.callback_query.message.edit_text(
            "if you want the report result please answer this questions \n Question 1: how old are you ?"
        )
    elif "question2" not in context.user_data:
        await update.message.reply_text("Question 2: What is your job ?")


# Define a function to handle user answers
async def handle_answer(update: Update, context):

    user_text = update.message.text
    if "question1" not in context.user_data:
        context.user_data["question1"] = user_text
        await ask_question(update, context)  # Ask the next question
    elif "question2" not in context.user_data:
        keyboard = [
            [
                InlineKeyboardButton("َAnalysis with AI Model ", callback_data="Model"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.user_data["question2"] = user_text
        api.send_info(
            context.user_data["question1"],
            context.user_data["question2"],
            context.user_data["user_username"],
        )
        res = context.user_data["response"]
        await update.message.reply_text(
            f"Thank you for answering! Here are your report:\n {res}",
            reply_markup=reply_markup,
        )
        # Clear user_answers for future interactions
        # user_answers.clear()


async def ask_prompt(update: Update, context):
    keyboard = [
        [
            InlineKeyboardButton("Skills Analysis", callback_data="prompt skills"),
            InlineKeyboardButton(
                "Personality Analysis", callback_data="prompt personality "
            ),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query and update.callback_query.message:
        await update.callback_query.message.edit_text(
            "Select the option you want it ",
            reply_markup=reply_markup,
        )
    else:
        await update.message.reply_text(
            "Select the option you want it",
            reply_markup=reply_markup,
        )


async def model(update: Update, context):
    query = update.callback_query

    keyboard = [
        [
            InlineKeyboardButton("New Test", callback_data="new_test"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Ai respone ",
        reply_markup=reply_markup,
    )


async def new_test(update: Update, context, test):
    print(" new test func")
    questions, answer_options, question_types = api.return_dataQuestion(
        context.user_data["language"], test
    )
    print(" data q")
    # Store the data in the context object
    context.user_data["questions"] = questions
    context.user_data["answer_options"] = answer_options
    context.user_data["question_types"] = question_types

    context.user_data["questioner_id"] = api.get_QuestionerId(
        context.user_data["user_id"]
    )

    await show_question(update, context)


# Define the function to show the question and answer options
async def show_question(update, context):
    questions = context.user_data.get("questions")
    answer_options = context.user_data.get("answer_options")
    question_types = context.user_data.get("question_types")

    if update.callback_query:
        message = update.callback_query.message
    else:
        message = update.message

    question_index = context.user_data.get("question_index", 0)

    question_type = int(question_types[question_index])

    if question_type == 0:  # Multiple Choice
        # Create the keyboard with the answer options as buttons
        keyboard = [
            [
                InlineKeyboardButton(
                    f"{idx})  {answer}",
                    callback_data=f"answer_{idx}",
                    switch_inline_query_current_chat="",
                )
            ]
            for idx, answer in enumerate(answer_options[question_index], start=1)
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send the message with the question and the keyboard
        await message.edit_text(
            f"Question number{question_index+1}\n{questions[question_index]} \n 1){answer_options[question_index][0]} \n 2){answer_options[question_index][1]}",
            reply_markup=reply_markup,
        )
    elif question_type == 2:  # Descriptive
        await message.edit_text(
            f"Question number{question_index+1}\n{questions[question_index]}"
        )
    elif question_type == 1:  # Ranged
        keyboard = [
            [
                InlineKeyboardButton(
                    answer,
                    callback_data=f"answer_{idx}",
                    switch_inline_query_current_chat="",
                )
            ]
            for idx, answer in enumerate(ranged_option, start=1)
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send the message with the question and the keyboard
        await message.edit_text(
            f"Question number{question_index+1}\n{questions[question_index]}",
            reply_markup=reply_markup,
        )


# Define the function to handle the button press
async def button(update, context):
    query = update.callback_query
    questions = context.user_data.get("questions")
    answer_options = context.user_data.get("answer_options")
    question_types = context.user_data.get("question_types")

    # Store the answer index to the selected question in user_data
    question_index = context.user_data.get("question_index", 0)
    answer_index = int(query.data.split("_")[1]) - 1
    if question_types[question_index] == 0:
        context.user_data[f"Your answer_{question_index}"] = answer_options[
            question_index
        ][answer_index]
        context.user_data[f"options_{question_index}"] = answer_index
    elif question_types[question_index] == 1:
        context.user_data[f"Your answer_{question_index}"] = ranged_option[answer_index]

    # Move to the next question or show the results
    if question_index < len(questions) - 1:
        context.user_data["question_index"] = question_index + 1
        await show_question(update, context)
    else:
        # results = [
        #     f"Question {i + 1}: {questions[i]}\nYour answer: {context.user_data.get(f'Your answer_{i}', 'No answer selected')}"
        #     for i in range(len(questions))
        # ]
        options_list = [
            context.user_data[f"options_{i}"] for i in range(len(questions))
        ]
        # answers_list = [
        #     context.user_data.get(f"Your answer_{i}", "No answer selected")
        #     for i in range(len(questions))
        # ]
        context.user_data["question_index"] = 0
        response = api.send_Questioner(
            context.user_data["user_id"],
            context.user_data["questioner_id"],
            options_list,
            context.user_data["language"],
            context.user_data["testid"],
        )
        print(response)
        context.user_data["response"] = response
        context.user_data["for"] += 1
        # await query.message.reply_text(response)
        await ask_question(update, context)

        # query.answer()


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "نیاز به راهنمایی دارید؟ هیچ مشکلی نیست! برای دریافت راهنمایی درباره نحوه استفاده از ربات، می‌توانید از دستور /help استفاده کنید. همچنین، اگر سوالاتی در مورد سیستم یا فرآیند پرسش و پاسخ دارید، من همیشه در دسترس هستم. با ارسال /help به من، می‌توانید به آسانی راهنمایی مورد نیاز خود را دریافت کنید."
    )


# Define the function to handle the user's answer
async def answer(update, context):
    # Get the user's answer and the selected question index from user_data
    answer_text = update.message.text
    question_index = context.user_data.get("question_index")
    questions = context.user_data.get("questions")

    if question_index is not None:
        # Store the answer in user_data
        # context.user_data["answers"][question_index] = answer_text
        context.user_data[f"Your answer_{question_index}"] = answer_text

        # Move to the next question
        if question_index < len(questions) - 1:
            context.user_data["question_index"] = question_index + 1
            await show_question(update, context)
        else:
            results = [
                f"Question {i + 1}: {questions[i]}\nYour answer: {context.user_data.get(f'Your answer_{i}', 'No answer selected')}"
                for i in range(len(questions))
            ]

        await update.message.reply_text(text="\n\n".join(results))
        update.answer()
    else:
        await update.message.reply_text(
            "Sorry, I couldn't identify the current question."
        )


def init_user_data(update, context):
    context.user_data["answers"] = {}


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Error {update} caused error {context.error}")


# Set up the bot
if __name__ == "__main__":
    try:
        print("starting bot ..")
        app = Application.builder().token(TOKEN).build()

        # commands
        app.add_handler(CommandHandler("start", start))

        # Add message handler to ask questions

        # Add message handler to handle user answers
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

        app.add_handler(CommandHandler("help", help_command))

        # app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))

        # Add the init_user_data function to the list of handlers to be called on every update
        # app.add_handler(MessageHandler(filters.ALL, init_user_data), group=-1)

        # Callback query for buttons
        app.add_handler(CallbackQueryHandler(language_selected, pattern="^english$"))
        app.add_handler(CallbackQueryHandler(language_selected, pattern="^persian$"))
        app.add_handler(CallbackQueryHandler(workflow_test, pattern=".*workflow.*"))
        app.add_handler(CallbackQueryHandler(handle_flow, pattern="^new_test$"))
        app.add_handler(CallbackQueryHandler(ask_prompt, pattern="^Model$"))
        app.add_handler(CallbackQueryHandler(model, pattern=".*prompt.*"))
        # app.add_handler(CallbackQueryHandler(prompt_selected, pattern="^(yes|no)$"))

        # Define the asynchronous conversation handler with states FIRST and SECOND
        # )

        # Add conversation handler to the application
        # app.add_handler(conv_handler)

        app.add_handler(CallbackQueryHandler(button))

        # # messages
        # app.add_handler(MessageHandler(filters.TEXT, handle_response))

        # errors
        app.add_error_handler(error)

        # infinite loop to keep the bot listening
        app.run_polling()
    except telegram.error.TimedOut:
        print("Timeout error occurred")


# async def prompt(update, context):
#     # prompt = context.user_data["flow"]["prompt"]

#     keyboard = [
#         [
#             InlineKeyboardButton("Yes", callback_data="yes"),
#             InlineKeyboardButton("No", callback_data="no"),
#         ]
#     ]

#     reply_markup = InlineKeyboardMarkup(keyboard)

#     if update.callback_query and update.callback_query.message:
#         await update.callback_query.message.edit_text(
#             "If You want to continue click Yes and get result Click No ",
#             reply_markup=reply_markup,
#         )
#     else:
#         await update.message.reply_text(
#             "If You want to continue click Yes and get result Click No ",
#             reply_markup=reply_markup,
#         )


# async def prompt_selected(update: Update, context):
#     # Extract the data
#     prompt = context.user_data["flow"]["routin"][0]["prompt"]

#     answer = update.callback_query.data
#     user_ans = prompt[answer]
#     # print(context.user_data["language"])
#     if str(user_ans).isdigit():
#         await routin(Update, context, user_ans)
#     else:
#         await update.callback_query.message.edit_text(
#             "Your prompt :" + str(user_ans),
#         )
#     # Call the new_test function with the selected language
