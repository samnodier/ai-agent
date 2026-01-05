from functions.write_file_content import write_file_content

results = write_file_content("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
print("Result for lorem.txt file:")
print(results)

results = write_file_content(
    "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"
)
print("Result for 'pkg/morelorem.txt' file:")
print(results)

results = write_file_content(
    "calculator", "/tmp/temp.txt", "this should not be allowed"
)
print("Result for '/tmp/temp.txt' file:")
print(results)
