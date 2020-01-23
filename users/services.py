from django.contrib.auth import get_user_model

def deleteUser(userId, info):
    c_user = info.context.user
    if c_user.id != int(userId):
        raise Exception("Unauthorize action!")
    results = get_user_model().objects.filter(id=userId).delete()
    isDeleted = results[0] > 0
    return isDeleted
