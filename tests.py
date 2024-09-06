# class IsAuthenticated():
#     """
#     Allows access only to authenticated users.
#     """
#
#     def has_permission(self, request, view):
#         return bool(request.user and request.user.is_authenticated)
#

# def wapper(obj, *args):
#     return obj


def wapper(*args):
    datas = [*args]

    class IsDatas():

        def has_permission(self, data):
            if data in datas:
                return True
            return False

    return IsDatas


one = wapper(1, 2, 3, 4)()


print(one.has_permission(1))
two = wapper(5, 6, 7, 8)()


print(two.has_permission(1))
