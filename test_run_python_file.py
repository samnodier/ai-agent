from functions.run_python_file import run_python_file


results = run_python_file("calculator", "main.py")
print('Running "main.py" file:')
print(results)

results = run_python_file("calculator", "main.py", ["3 + 5"])
print('Running "main.py "3 + 5" file:')
print(results)

results = run_python_file("calculator", "tests.py")
print('Running "tests.py" file:')
print(results)

results = run_python_file("calculator", "../main.py")
print('Running "../main.py" file:')
print(results)

results = run_python_file("calculator", "nonexistent.py")
print('Running "nonexistent.py" file:')
print(results)

results = run_python_file("calculator", "lorem.txt")
print('Running "lorem.txt" file:')
print(results)
