from random import choice


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == 'a':
        return 'b'
    elif lowered == 'rng':
        return choice(['good rng','mid rng', 'mid rng', 'mid rng', 'mid rng', 'mid rng', 'bad rng'])

