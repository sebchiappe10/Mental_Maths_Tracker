LEVEL_CONFIG = {

    "addition": {
        1: {"min1": 1,   "max1": 20,  "min2": 1,   "max2": 30},
        2: {"min1": 20,  "max1": 50,  "min2": 10,  "max2": 60},
        3: {"min1": 50,  "max1": 100, "min2": 30,  "max2": 120},
        4: {"min1": 100, "max1": 200, "min2": 80,  "max2": 220},
        5: {
            "whole":   {"min1": 200, "max1": 500, "min2": 150, "max2": 550},
            "decimal": {"min1": 0.00, "max1": 20.00, "min2": 0.00, "max2": 20.00}
        },
    },

    "subtraction": {
        1: {"min1": 10,  "max1": 20,  "min2": 1,   "max2": 20},
        2: {"min1": 20,  "max1": 40,  "min2": 10,  "max2": 30},
        3: {"min1": 40,  "max1": 80,  "min2": 20,  "max2": 50},
        4: {"min1": 80,  "max1": 150, "min2": 60,  "max2": 130},
        5: {
            "whole":   {"min1": 150, "max1": 500, "min2": 120, "max2": 470},
            "decimal": {"min1": 8.00, "max1": 20.00, "min2": 0.00, "max2": 16.00}
        },
    },

    "multiplication": {
        1: {"min1": 1,  "max1": 10, "min2": 1,  "max2": 10},
        2: {"min1": 1,  "max1": 10, "min2": 10, "max2": 20},
        3: {"min1": 1,  "max1": 15, "min2": 10, "max2": 25},
        4: {"min1": 5,  "max1": 25, "min2": 15, "max2": 30},
        5: {
            "whole":   {"min1": 10,  "max1": 25,  "min2": 15, "max2": 45},
            "decimal": {"min1": 8.0, "max1": 20.0, "min2": 1,  "max2": 10}
        },
    },

    # Division: pick divisor and result first, then multiply to get dividend
    # This ensures clean whole number answers at levels 1-4
    # Level 5 allows answers ending in .5
    "division": {
        1: {"min_result": 2,  "max_result": 10, "min_divisor": 2,  "max_divisor": 5,  "allow_half": False},
        2: {"min_result": 2,  "max_result": 13, "min_divisor": 2,  "max_divisor": 10, "allow_half": False},
        3: {"min_result": 3,  "max_result": 15, "min_divisor": 3,  "max_divisor": 15, "allow_half": False},
        4: {"min_result": 4,  "max_result": 18, "min_divisor": 4,  "max_divisor": 18, "allow_half": False},
        5: {"min_result": 4,  "max_result": 18, "min_divisor": 4,  "max_divisor": 18, "allow_half": True},
    },

    "percentage": {
        1: {
            "percentages": [10, 50],
            "min2": 10, "max2": 100, "multiples_of": 10
        },
        2: {
            "percentages": [10, 20, 25, 50],
            "min2": 10, "max2": 100, "multiples_of": 10
        },
        3: {
            "percentages": [10, 20, 25, 50],
            "min2": 10, "max2": 100, "multiples_of": 2
        },
        4: {
            "percentages": list(range(2, 100, 2)) + [25],
            "min2": 10, "max2": 150, "multiples_of": 2
        },
        5: {
            "percentages": list(range(1, 101)),
            "min2": 10, "max2": 150, "multiples_of": 1
        },
    },

}