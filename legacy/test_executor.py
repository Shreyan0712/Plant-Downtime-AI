from legacy.action_parser import (
    parse_action
)

from legacy.tool_executor import (
    execute_action
)


query = input("Enter query: ")


parsed_action = parse_action(
    query
)

print("\nPARSED ACTION:\n")

print(parsed_action)


result = execute_action(
    parsed_action
)

print("\nEXECUTION RESULT:\n")

print(result)