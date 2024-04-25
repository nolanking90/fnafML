import itertools
import operator

numbers = [6356176, 1, 6356304, 6356360]
target = 89
ops = [operator.and_, operator.or_, operator.xor]

# Generate all possible combinations of operations
op_combinations = list(itertools.product(ops, repeat=len(numbers)-1))

for ops in op_combinations:
    # Apply the operations to the numbers
    result = numbers[0]
    for i, op in enumerate(ops):
        result = op(result, numbers[i+1])
        print(result, ops)
    # Check if the result matches the target
    if result == target:
        print("Found a match:", ops)
        break
else:
    print("No match found")
