from utils.BaseClass import IntChoicesBaseEnum, Enum, auto


class UserGender(IntChoicesBaseEnum):
    MALE = "男"
    FEMALE = "女"
    GN = "保密"

class UserSignState(IntChoicesBaseEnum):
    IN = "注册"
    OUT = "注销"


