# List of choices made by the challenger.
# The adversary does not have access to this.
CHALLENGER_CHOICES: list[bool] = []


def challenger(n_bytes: int) -> bytes:
    """Output the requested number of strong or weak RNG bytes.

    The challenger flips a fair coin to decide whether it is going to use
    the strong or weak RNG to generate the challenge.
    Then, the challenger uses the chosen RNG, to generate the challenge bytes
    of requested length, and returns them to the caller.

    :param n_bytes: the number of bytes to generate
    :return: the challenge bytes
    """
    # TODO: Randomly choose whether to use the strong or weak RNG.
    use_strong = ...

    # Keep track of the choices made for later comparison
    CHALLENGER_CHOICES.append(use_strong)

    # TODO: generate the bytes and return them


def distinguish() -> bool:
    """Determine whether the challenger used the strong or weak RNG.

    The adversary's goal is to convince the challenger that it is able
    to distinguish the output of the weak RNG from the strong RNG.
    The adversary can request a challenge byte-string of the desired length
    from the challenger, but only once. Then, it can perform any computation
    to help determine whether the weak or strong RNG was used. The adversary
    returns which RNG it thinks was used.

    :return: `True` if the challenger used the strong RNG, `False` otherwise
    """
    pass


def main():
    num_guesses = 10

    adversary_guesses = []
    for _ in range(num_guesses):
        guess = distinguish()
        adversary_guesses.append(guess)

    # TODO: calculate the adversary's success rate
    num_correct = 0
    success_ratio = 0

    print("Total rounds. . :", num_guesses)
    print("Correct guesses :", num_correct)
    print("Success ratio . :", success_ratio)


if __name__ == "__main__":
    main()
