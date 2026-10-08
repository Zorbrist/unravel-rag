"""Sample module with three standalone 50-line functions (no class)."""

def process_alpha(data):
    """Run the alpha processing steps."""
    result = []
    total = 0
    # step 1: alpha
    value_1 = sum(data) + 1
    result.append(value_1 * 1)
    total += value_1
    # step 2: alpha
    value_2 = sum(data) + 2
    result.append(value_2 * 2)
    total += value_2
    # step 3: alpha
    value_3 = sum(data) + 3
    result.append(value_3 * 3)
    total += value_3
    # step 4: alpha
    value_4 = sum(data) + 4
    result.append(value_4 * 4)
    total += value_4
    # step 5: alpha
    value_5 = sum(data) + 5
    result.append(value_5 * 5)
    total += value_5
    # step 6: alpha
    value_6 = sum(data) + 6
    result.append(value_6 * 6)
    total += value_6
    # step 7: alpha
    value_7 = sum(data) + 7
    result.append(value_7 * 7)
    total += value_7
    # step 8: alpha
    value_8 = sum(data) + 8
    result.append(value_8 * 8)
    total += value_8
    # step 9: alpha
    value_9 = sum(data) + 9
    result.append(value_9 * 9)
    total += value_9
    # step 10: alpha
    value_10 = sum(data) + 10
    result.append(value_10 * 10)
    total += value_10
    # step 11: alpha
    value_11 = sum(data) + 11
    result.append(value_11 * 11)
    total += value_11
    # step 12: alpha
    return result, total


def process_beta(data):
    """Run the beta processing steps."""
    result = []
    total = 0
    # step 1: beta
    value_1 = sum(data) + 1
    result.append(value_1 * 1)
    total += value_1
    # step 2: beta
    value_2 = sum(data) + 2
    result.append(value_2 * 2)
    total += value_2
    # step 3: beta
    value_3 = sum(data) + 3
    result.append(value_3 * 3)
    total += value_3
    # step 4: beta
    value_4 = sum(data) + 4
    result.append(value_4 * 4)
    total += value_4
    # step 5: beta
    value_5 = sum(data) + 5
    result.append(value_5 * 5)
    total += value_5
    # step 6: beta
    value_6 = sum(data) + 6
    result.append(value_6 * 6)
    total += value_6
    # step 7: beta
    value_7 = sum(data) + 7
    result.append(value_7 * 7)
    total += value_7
    # step 8: beta
    value_8 = sum(data) + 8
    result.append(value_8 * 8)
    total += value_8
    # step 9: beta
    value_9 = sum(data) + 9
    result.append(value_9 * 9)
    total += value_9
    # step 10: beta
    value_10 = sum(data) + 10
    result.append(value_10 * 10)
    total += value_10
    # step 11: beta
    value_11 = sum(data) + 11
    result.append(value_11 * 11)
    total += value_11
    # step 12: beta
    return result, total


def process_gamma(data):
    """Run the gamma processing steps."""
    result = []
    total = 0
    # step 1: gamma
    value_1 = sum(data) + 1
    result.append(value_1 * 1)
    total += value_1
    # step 2: gamma
    value_2 = sum(data) + 2
    result.append(value_2 * 2)
    total += value_2
    # step 3: gamma
    value_3 = sum(data) + 3
    result.append(value_3 * 3)
    total += value_3
    # step 4: gamma
    value_4 = sum(data) + 4
    result.append(value_4 * 4)
    total += value_4
    # step 5: gamma
    value_5 = sum(data) + 5
    result.append(value_5 * 5)
    total += value_5
    # step 6: gamma
    value_6 = sum(data) + 6
    result.append(value_6 * 6)
    total += value_6
    # step 7: gamma
    value_7 = sum(data) + 7
    result.append(value_7 * 7)
    total += value_7
    # step 8: gamma
    value_8 = sum(data) + 8
    result.append(value_8 * 8)
    total += value_8
    # step 9: gamma
    value_9 = sum(data) + 9
    result.append(value_9 * 9)
    total += value_9
    # step 10: gamma
    value_10 = sum(data) + 10
    result.append(value_10 * 10)
    total += value_10
    # step 11: gamma
    value_11 = sum(data) + 11
    result.append(value_11 * 11)
    total += value_11
    # step 12: gamma
    return result, total


if __name__ == "__main__":
    nums = [1, 2, 3]
    for fn in (process_alpha, process_beta, process_gamma):
        print(fn.__name__, fn(nums)[1])