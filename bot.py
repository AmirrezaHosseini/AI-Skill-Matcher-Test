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
)
import telegram.error

import api

##### get data  #####
# print(api.return_questionText())

# bot identity
# TOKEN: final = "6835505632:AAFJ9Auz7wSS3R-3e89FKIXBQv3OeIEuJHY"
# BOT_USERNAME: final = "@AI_Skill_MatcherBot"
TOKEN: final = "6650488420:AAFayPXrcyuBaJ0HX8upU2CkFnp3AZLUVu0"
BOT_USERNAME: final = "@personaPathTestBot"

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


# questions, answer_options, question_types = [], [], []
ranged_option = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]


# print(type(questions))

# Define the function to handle the /start command


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

    full_name = (
        f"{user_first_name} {user_last_name}" if user_last_name else user_first_name
    )
    # user_id = api.post_User(full_name, user_username)
    print(
        f"User Information:\nID: {user_id}\nFull Name: {full_name}\nUsername: {user_username}"
    )
    context.user_data["user_id"] = api.post_User(full_name, user_username)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hi ! I'm AI_Skill_Matcher .\n Please Choose Your Language",
        reply_markup=reply_markup,
    )


async def language_selected(update: Update, context):
    # Extract the selected language from the callback data
    context.user_data["language"] = update.callback_query.data
    # print(context.user_data["language"])

    # Call the new_test function with the selected language
    await set_flow(update, context)


async def set_flow(update: Update, context):
    if context.user_data["language"] == "persian":
        keyboard = [
            [
                InlineKeyboardButton(" MBTI تست ", callback_data="mbti"),
                InlineKeyboardButton("تست مهارت شناسی ", callback_data="skill"),
                InlineKeyboardButton("تست شخصیت شناسی ", callback_data="personality"),
            ]
        ]
        message = "تست مورد نظر خود را انتخاب کنید "
    elif context.user_data["language"] == "english":
        keyboard = [
            [
                InlineKeyboardButton("Test MBTI ", callback_data="mbti"),
                InlineKeyboardButton("Test Skill Matcher", callback_data="skill"),
                InlineKeyboardButton("Test Personality", callback_data="personality"),
            ]
        ]
        message = " Select the test you want to do it "

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text(
        message,
        reply_markup=reply_markup,
    )


async def status_test(update: Update, context):
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


async def new_test(update: Update, context):
    questions, answer_options, question_types = api.return_dataQuestion(
        context.user_data["language"]
    )

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

    # Display the user's answer
    # user_answer = context.user_data[f"Your answer_{question_index}"]
    # await query.message.reply_text(f"Your answer: {user_answer}")

    # Disable the buttons after answering
    # keyboard = [[]]
    # reply_markup = InlineKeyboardMarkup(keyboard)
    # await query.edit_message_reply_markup(reply_markup)

    # Delete the message after the user has chosen a button
    # await context.bot.delete_message(
    #     chat_id=query.message.chat_id, message_id=query.message.message_id
    # )

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
        answers_list = [
            context.user_data.get(f"Your answer_{i}", "No answer selected")
            for i in range(len(questions))
        ]
        context.user_data["question_index"] = 0
        response = api.send_Questioner(
            context.user_data["user_id"],
            context.user_data["questioner_id"],
            options_list,
            context.user_data["language"],
        )
        await query.message.reply_text(text=response)
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
        app.add_handler(CommandHandler("help", help_command))

        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))

        # Add the init_user_data function to the list of handlers to be called on every update
        # app.add_handler(MessageHandler(filters.ALL, init_user_data), group=-1)

        # Callback query for buttons
        app.add_handler(CallbackQueryHandler(language_selected, pattern="^english$"))
        app.add_handler(CallbackQueryHandler(language_selected, pattern="^persian$"))
        app.add_handler(CallbackQueryHandler(status_test, pattern="^mbti$"))
        app.add_handler(CallbackQueryHandler(new_test, pattern="^new_test$"))
        app.add_handler(CallbackQueryHandler(button))

        # # messages
        # app.add_handler(MessageHandler(filters.TEXT, handle_response))

        # errors
        app.add_error_handler(error)

        # infinite loop to keep the bot listening
        app.run_polling()
    except telegram.error.TimedOut:
        print("Timeout error occurred")
