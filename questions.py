import random
from config import LEVEL_CONFIG


def generate_question(operator: str, level: int) -> dict:
    """
    Generate a mental maths question for the given operator and level.

    Args:
        operator: One of "addition", "subtraction", "multiplication",
                  "division", "percentage"
        level:    Integer level (1-5) corresponding to a key in LEVEL_CONFIG

    Returns:
        A dictionary with keys: operator, number_1, number_2, correct_answer
    """

    # -------------------------------------------------------------------------
    # Look up the config block for this operator and level
    # -------------------------------------------------------------------------
    cfg = LEVEL_CONFIG[operator][level]

    # -------------------------------------------------------------------------
    # ADDITION / SUBTRACTION / MULTIPLICATION
    # Level 5 has two sub-modes ("whole" and "decimal"); pick one at random.
    # All other levels use the config block directly.
    # -------------------------------------------------------------------------
    if operator in ("addition", "subtraction"):

        # Level 5: randomly select the "whole" or "decimal" sub-mode
        if level == 5:
            cfg = cfg[random.choice(["whole", "decimal"])]

        # Determine whether the ranges are decimal (float) or whole (int)
        # by checking if any boundary value is a float
        is_decimal = any(isinstance(cfg[k], float) for k in cfg)

        if is_decimal:
            # Generate two floats rounded to 2 decimal places
            n1 = round(random.uniform(cfg["min1"], cfg["max1"]), 2)
            n2 = round(random.uniform(cfg["min2"], cfg["max2"]), 2)
        else:
            n1 = random.randint(cfg["min1"], cfg["max1"])
            n2 = random.randint(cfg["min2"], cfg["max2"])

        # Calculate the correct answer for each operator
        if operator == "addition":
            answer = round(n1 + n2, 2)

        elif operator == "subtraction":
            # Swap so the larger number is always number_1, keeping answers
            # positive and sensible for a mental maths context
            n1, n2 = max(n1, n2), min(n1, n2)
            answer = round(n1 - n2, 2)




    elif operator == "multiplication":
        # Level 5: randomly select the "whole" or "decimal" sub-mode
        if level == 5:
            cfg = cfg[random.choice(["whole", "decimal"])]

        # Determine whether the ranges are decimal (float) or whole (int)
        is_decimal = any(isinstance(cfg[k], float) for k in cfg)

        if is_decimal:
            n1 = round(random.uniform(cfg["min1"], cfg["max1"]), 1)
            n2 = random.randint(cfg["min2"], cfg["max2"])
        else:
            n1 = random.randint(cfg["min1"], cfg["max1"])
            n2 = random.randint(cfg["min2"], cfg["max2"])

        answer = round(n1 * n2, 2)
    # -------------------------------------------------------------------------
     # DIVISION
    # Pick the divisor and result first, then derive the dividend by
    # multiplying them. This guarantees clean answers (whole numbers at
    # levels 1-4; optionally ending in .5 at level 5).
    # -------------------------------------------------------------------------
    elif operator == "division":
 
        divisor = random.randint(cfg["min_divisor"], cfg["max_divisor"])
        result  = random.randint(cfg["min_result"],  cfg["max_result"])
 
        if cfg["allow_half"]:
            # At level 5, the result can optionally end in .5
            # Randomly add 0.5 to the result 50% of the time
            if random.choice([True, False]):
                result += 0.5
                # A result ending in .5 means dividend = divisor * result, which
                # only produces a whole number when the divisor is even.
                # If the current divisor is odd, re-draw from even numbers only.
                if divisor % 2 != 0:
                    even_divisors = list(range(
                        cfg["min_divisor"] + (cfg["min_divisor"] % 2),  # first even >= min
                        cfg["max_divisor"] + 1,
                        2
                    ))
                    divisor = random.choice(even_divisors)
 
        # Derive the dividend so that dividend ÷ divisor = result exactly
        # dividend is always a whole number: even divisor * x.5 = whole number
        dividend = divisor * result
 
        # number_1 is what the student sees on the left of the ÷ sign
        n1     = dividend
        n2     = divisor
        answer = result
    # -------------------------------------------------------------------------
    # PERCENTAGE
    # number_1 is a percentage value chosen from the allowed list.
    # number_2 is a random multiple of multiples_of within the given range.
    # -------------------------------------------------------------------------
    elif operator == "percentage":

        # Pick the percentage from the allowed list for this level
        n1 = random.choice(cfg["percentages"])

        # Build a list of valid multiples within [min2, max2] then pick one
        step      = cfg["multiples_of"]
        multiples = list(range(cfg["min2"], cfg["max2"] + 1, step))
        n2        = random.choice(multiples)

        # Calculate: what is n1% of n2?
        answer = round((n1 / 100) * n2, 2)

    # -------------------------------------------------------------------------
    # Return the completed question dictionary
    # -------------------------------------------------------------------------
    return {
        "operator":      operator,
        "number_1":      n1,
        "number_2":      n2,
        "correct_answer": answer,
    }

answer = generate_question("subtraction", 5)
print(answer)



