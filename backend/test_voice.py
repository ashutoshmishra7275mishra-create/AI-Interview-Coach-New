from voice_input import get_answer
from command_executor import execute_command

command = get_answer()

print("\nYou said/typed:")
print(command)

execute_command(command)