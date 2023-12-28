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
# TOKEN: final = "6650488420:AAFayPXrcyuBaJ0HX8upU2CkFnp3AZLUVu0"
# BOT_USERNAME: final = "@personaPathTestBot"

# Define the questions and answers
# Define the questions and answer options
# questions = ["What is your name?", "What is your age?", "What is your favorite color?"]
# answer_options = [
#     ["Alice", "Bob", "Charlie"],
#     [],
#     ["Red", "Green", "Blue"],
# ]
# question_types = ["0", "1", "0"]

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
#     "I usually prefer group work and get energy from others.  ",
#     "I am independent and sometimes shy. ",
# ]

questions, answer_options, question_types = api.return_questionText()

# Define the function to handle the /start command


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("نتایج تست گذشته", callback_data="previous_results"),
            InlineKeyboardButton("new Test", callback_data="new_test"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # init_user_data(update, context)

    await update.message.reply_text(
        "Select new test",
        reply_markup=reply_markup,
    )



# Define the function to show the question and answer options
async def show_question(update, context):
    # Check if the update is a callback query or a regular message
    if update.callback_query:
        message = update.callback_query.message
    else:
        message = update.message

    question_index = context.user_data.get("question_index", 0)

    question_type = int(question_types[question_index])

    if question_type == 0:  # Multiple Choice
        keyboard = [
            [InlineKeyboardButton(a, callback_data=a)]
            for a in answer_options[question_index]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await message.reply_text(
            questions[question_index], reply_markup=reply_markup
        )
    elif question_type == 1:  # Descriptive
        await message.reply_text(questions[question_index])
    elif question_type == 2:  # Ranged
        pass



# Define the function to handle the button press
async def button(update, context):
    query = update.callback_query

    # Get the question index from user_data
    question_index = context.user_data.get("question_index", 0)
    print("print 1")
    # Check if the question index is within bounds
    if 0 <= question_index < len(questions):
        print("print 2")
        context.user_data[f"answer_{question_index}"] = query.data
        print("print 3")
        # Move to the next question or show the results
        if question_index < len(questions) - 1:
            print("print 4")
            context.user_data["question_index"] = question_index + 1
            await show_question(update, context)
        else:
            print("print 5")
            results = [
                f"{q}: {context.user_data[f'answer_{i}']}" for i, q in enumerate(questions)
            ]
            print("print 6")
            query.answer()
            print("print 7")
            await query.edit_message_text(text="\n".join(results))
            # Reset question_index to None to avoid errors when processing new responses
            context.user_data["question_index"] = None
    else:
        await query.answer()
        await query.edit_message_text("Sorry, I couldn't identify the current question.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "نیاز به راهنمایی دارید؟ هیچ مشکلی نیست! برای دریافت راهنمایی درباره نحوه استفاده از ربات، می‌توانید از دستور /help استفاده کنید. همچنین، اگر سوالاتی در مورد سیستم یا فرآیند پرسش و پاسخ دارید، من همیشه در دسترس هستم. با ارسال /help به من، می‌توانید به آسانی راهنمایی مورد نیاز خود را دریافت کنید."
    )


# Define the function to handle the user's answer
async def answer(update, context):
    # Get the user's answer and the selected question index from user_data
    answer_text = update.message.text
    question_index = context.user_data.get("question_index")

    if question_index is not None:
        # Store the answer in user_data
        # context.user_data["answers"][question_index] = answer_text
        context.user_data[f"answer_{question_index}"] = answer_text


        # Move to the next question
        if question_index < len(questions) - 1:
            context.user_data["question_index"] = question_index + 1
            await show_question(update, context)
        else:
            results = [
                f"{q}: {context.user_data[f'answer_{i}']}" for i, q in enumerate(questions)
            ]
            await update.message.reply_text(text="\n".join(results))
    else:
        await update.message.reply_text("Sorry, I couldn't identify the current question.")



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
