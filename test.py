import api

# print(api.send_Questioner("1"))
# print(api.post_User("aap", "lkkkppuy"))
print(
    api.get_data_question(
        "https://skill-matcher-api.liara.run/api/Question/GetQuestionsByLevelAndTestId/ef3f2bee-a91a-487f-9f4b-83aeb1e7a3df/1"
    )
)
# print(api.return_dataQuestion())
# print(api.get_QuestionerId("64fd88cd-c187-4df5-96a5-599612472701"))
# print(api.send_Questioner("3fa85f64-5717-4562-b3fc-2c963f66afa6", "test", 1))
