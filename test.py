import api

# print(api.send_Questioner("1"))
# print(api.post_User("Amir", "Amir_blurr"))
# print(
#     api.get_data_question(
#         "https://skill-matcher-api.liara.run/api/Question/GetQuestionsByLevelAndTestId/ef3f2bee-a91a-487f-9f4b-83aeb1e7a3df/1"
#     )
# )
# print(api.return_dataQuestion("english", "5751f4a7-b2b5-4602-a0a7-22b16913246b/2"))
# print(api.get_QuestionerId("c7951c1f-6ca9-44d7-aaf6-54a7a845a82e"))
# print(
#     api.send_Questioner(
#         "45b23d93-e123-48e7-aa5a-43c45cb8670b",
#         "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#         "Strongly",
#         1,
#     )
# )
# print(
#     api.send_Questioner(
#         api.post_User("aap", "lkkkppuy"),
#         api.get_QuestionerId("5dce6839-9c4f-4eec-972f-e0eb84ae80db"),
#         [0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1],
#         "english",
#     )
# )
# print(
#     api.get_Optionlist(
#         api.get_data_question(
#             "https://skill-matcher-api.liara.run/api/Question/GetQuestionsByLevelAndTestId/ef3f2bee-a91a-487f-9f4b-83aeb1e7a3df/1"
#         ),
#         [0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1],

#     )
# )
# d = api.get_workflows()
# print(d[0]["routin"][0]["prompt"]["yes"])

print(api.send_info(20, "any", "Amir_blurr"))
