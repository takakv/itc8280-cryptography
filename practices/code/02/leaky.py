import secrets

from lib02 import strong_rng, weak_rng, bytes_to_binary

# List of choices made by the challenger.
# The adversary does not have access to this.
CHALLENGER_CHOICES: list[bool] = []


def challenger(n_bytes: int) -> bytes:
    # Randomly choose whether to use the strong or weak RNG.
    use_strong = secrets.choice([True, False])

    # Keep track of the choices made for later comparison
    CHALLENGER_CHOICES.append(use_strong)

    if use_strong:
        return strong_rng(n_bytes)
    else:
        return weak_rng(n_bytes)


def distinguish() -> bool:
    # The larger the challenge size, the more apparent the bias.
    challenge_size = 64

    challenge = challenger(challenge_size)

    # Convert to bitstring to easily count zeroes and ones.
    challenge_bitstring = bytes_to_binary(challenge)

    zeros = challenge_bitstring.count("0")
    ones = challenge_bitstring.count("1")

    difference = abs(zeros - ones)
    total_bits = zeros + ones

    bias = difference / total_bits

    # Tweak the bias cutoff either experimentally or by doing a bit of math.
    if bias < 0.05:
        # If the bias is low, probably the strong RNG was used.
        return True
    else:
        return False


def main():
    num_guesses = 10

    adversary_guesses = []
    for _ in range(num_guesses):
        guess = distinguish()
        adversary_guesses.append(guess)

    num_correct = 0
    for i in range(num_guesses):
        if adversary_guesses[i] == CHALLENGER_CHOICES[i]:
            num_correct += 1

    success_ratio = num_correct / num_guesses
    print("Total rounds. . :", num_guesses)
    print("Correct guesses :", num_correct)
    print("Success ratio . :", success_ratio)


if __name__ == "__main__":
    main()
