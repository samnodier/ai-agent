from functions.get_file_content import get_file_content

results = get_file_content("calculator", "lorem.txt")
print("Result for lorem.txt file:")
print(len(results))

results = get_file_content("calculator", "main.py")
print("Result for 'main.py' file:")
print(results)

results = get_file_content("calculator", "pkg/calculator.py")
print("Result for 'pkg/calculator.py' file:")
print(results)

results = get_file_content("calculator", "pkg/does_not_exist.py")
print("Result for 'pkg/does_not_exist.py' file")
print(results)
