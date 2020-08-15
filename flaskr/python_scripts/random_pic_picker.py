"""
| pick a random pic from the '/static/img/randomProfile' folder
"""
import os
from random import randrange

__author__ = "Itai Dotan"


def pick_my_pic(path=r"./flaskr/static/img/randomProfile"):
    """
    | pick a random pic from the img/randomProfile folder
    :param path: the path to use(leave empty for basic use). default to the pic folder
    :return: str of the pic path to send to the html
    """
    pic_list = os.listdir(path)
    num = randrange(0, len(pic_list))
    return f"{path[8:len(path)]}/{pic_list[num]}"


# if __name__ == "__main__":
#     """just to run and quick test the out put"""
#     print((pick_my_pic(r"../static/img/randomProfile")))
