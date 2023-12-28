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
TOKEN: final = "6835505632:AAFJ9Auz7wSS3R-3e89FKIXBQv3OeIEuJHY"
BOT_USERNAME: final = "@AI_Skill_MatcherBot"
# Define the questions and answers
# Define the questions and answer options

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
#     "1 )I usually prefer group work and get energy from others. I have many friends and share my personal information easily with others. I usually take the lead in work and activities and building relationships. ",
#     "2)I am independent and sometimes shy. I learn better through reflection and mental exercise. I rarely share my personal information with others. I listen more and talk less. I tend to work individually or at most with the cooperation of two or three people.",
# ]

questions, answer_options = api.return_questionText()
print(type(questions))

# Define the function to handle the /start command


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Previous Result", callback_data="previous_results"),
            InlineKeyboardButton("New Test", callback_data="new_test"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hi ! I'm AI_Skill_Matcher .\n If You want I assist you  Select New test",
        reply_markup=reply_markup,
    )


# Define the function to show the question and answer options
async def show_question(update, context):
    # Get the question index from user_data
    question_index = context.user_data.get("question_index", 0)

    # Create the keyboard with the answer options as buttons
    keyboard = [
        [InlineKeyboardButton(answer, callback_data=f"answer_{idx}")]
        for idx, answer in enumerate(answer_options[question_index], start=1)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the question and the keyboard
    await update.callback_query.edit_message_text(
        f"Question number{question_index+1}\n{questions[question_index]}",
        reply_markup=reply_markup,
    )


# Define the function to handle the button press
async def button(update, context):
    query = update.callback_query

    # Store the answer index to the selected question in user_data
    question_index = context.user_data.get("question_index", 0)
    answer_index = int(query.data.split("_")[1]) - 1
    context.user_data[f"Your answer_{question_index}"] = answer_options[question_index][
        answer_index
    ]

    # Move to the next question or show the results
    if question_index < len(questions) - 1:
        context.user_data["question_index"] = question_index + 1
        await show_question(update, context)

    else:
        results = [
            f"Question {i + 1}: {questions[i]}\nYour answer: {context.user_data.get(f'Your answer_{i}', 'No answer selected')}"
            for i in range(len(questions))
        ]
        update.callback_query.answer()
        await update.callback_query.edit_message_text(text="\n\n".join(results))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "نیاز به راهنمایی دارید؟ هیچ مشکلی نیست! برای دریافت راهنمایی درباره نحوه استفاده از ربات، می‌توانید از دستور /help استفاده کنید. همچنین، اگر سوالاتی در مورد سیستم یا فرآیند پرسش و پاسخ دارید، من همیشه در دسترس هستم. با ارسال /help به من، می‌توانید به آسانی راهنمایی مورد نیاز خود را دریافت کنید."
    )


# Define the function to handle the user's answer
def answer(update, context):
    # Get the user's answer and the selected question index from user_data
    answer_text = update.message.text
    question_index = context.user_data.get("selected_question")

    # Store the answer in user_data
    context.user_data["answers"][question_index] = answer_text

    # Send a confirmation message to the user
    update.message.reply_text(f"Your answer '{answer_text}' has been saved.")


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

        # app.add_handler(MessageHandler(filters.Text, answer))

        # Add the init_user_data function to the list of handlers to be called on every update
        # app.add_handler(MessageHandler(filters.ALL, init_user_data), group=-1)

        # Callback query for buttons
        app.add_handler(CallbackQueryHandler(show_question, pattern="^new_test$"))
        app.add_handler(CallbackQueryHandler(button))

        # # messages
        # app.add_handler(MessageHandler(filters.TEXT, handle_response))

        # errors
        app.add_error_handler(error)

        # infinite loop to keep the bot listening
        app.run_polling()
    except telegram.error.TimedOut:
        print("Timeout error occurred")
