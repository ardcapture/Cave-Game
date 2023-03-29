from dataclasses import dataclass, astuple, asdict
from pprint import pprint
import inspect


@dataclass(frozen=True)
class Comment:
    id: int
    text: str


def main():
    comment = Comment(1, "I just subscribed!")
    print(comment)
    print(astuple(comment))
    print(asdict(comment))

    pprint(inspect.getmembers(Comment, inspect.isfunction))
    # pprint(dir(Comment))

    # x, y = comment

    # print(f"{x=}")
    # print(f"{y=}")


if __name__ == "__main__":
    main()
