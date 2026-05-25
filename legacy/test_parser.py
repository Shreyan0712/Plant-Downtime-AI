from legacy.action_parser import (
    parse_action
)

query = input("Enter query: ")

result = parse_action(query)

print(result)