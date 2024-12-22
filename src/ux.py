from collections.abc import Sequence


def get_user_choice_from_sequence[T](sequence: Sequence[T], message: str) -> T:
    """Get user choice from sequence of items.

    Args:
        sequence: A sequence of items.
        message: A message to display to the user.

    Returns:
        The item chosen by the user.

    Raises:
        ValueError: If the sequence is empty.
    """
    if not sequence:
        msg = "Sequence is empty"
        raise ValueError(msg)
    while True:
        print(message)
        for i, item in enumerate(sequence):
            print(f"{i + 1}. {item}")

        choice = int(input("Enter your choice: "))
        if choice not in range(1, len(sequence) + 1):
            print("Invalid choice. Try again.")
        else:
            return sequence[choice - 1]


def get_bool_user_choice(message: str) -> bool:
    """Gets a boolean choice from the user."""
    while True:
        print(message)
        user_choice = input("Enter your choice (y/n): ")

        if user_choice.lower().strip() == "y":
            return True
        if user_choice.lower().strip() == "n":
            return False
        print("Invalid choice. Try again.")


def get_int_user_choice(message: str) -> int:
    """Gets an integer from the user."""
    while True:
        print(message)
        try:
            user_choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid choice. Try again.")
        else:
            return user_choice


def get_int_user_choice_ge(message: str, min_value: int) -> int:
    """Gets an integer from the user that is greater than or equal to `min_value`."""
    while True:
        user_choice = get_int_user_choice(message)

        if user_choice >= min_value:
            return user_choice
        print(f"Choice must be greater than or equal to {min_value}. Try again.")
