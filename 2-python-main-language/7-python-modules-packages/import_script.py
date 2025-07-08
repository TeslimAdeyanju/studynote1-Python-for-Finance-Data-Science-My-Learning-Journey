import test_module

# Option 1: List with index numbers as keys in a dictionary
quotes_dict = {
    1: "No matter how many mistakes you make or how slow you progress, you are still way ahead of everyone who isn't trying",
    2: "You cannot change what you refuse to confront",
    3: "Sometimes good things fall apart so better things can fall together.",
    4: "Don't think of cost. Think of value.",
    5: "Sometimes you need to distance yourself to see things clearly.",
    6: "Too many people buy things they don't need with money they don't have to impress people they don't know.",
    7: "If a person wants to be a part of your life, they will make an obvious effort to do so. Think twice before reserving a space in your heart for people who do not make an effort to stay.",
    8: "Making one person smile can change the world – maybe not the whole world, but their world."
}

# Print all quotes from the dictionary
for index, quote in quotes_dict.items():
    print(f"{index}. {quote}")

# Access individual quotes by index
print("\nAccessing individual quotes:")
print(f"Quote #3: {quotes_dict[3]}")
print(f"Quote #7: {quotes_dict[7]}")