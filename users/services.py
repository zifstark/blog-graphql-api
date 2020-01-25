from django.contrib.auth import get_user_model

def deleteUser(userId, info):
    c_user = info.context.user
    if c_user.id != int(userId):
        raise Exception("Unauthorize action!")
    results = get_user_model().objects.filter(id=userId).delete()
    isDeleted = results[0] > 0
    return isDeleted

def updateUser(input, info):
    c_user = info.context.user
    user = get_user_model().objects.get(pk=c_user.id)
    user.username = input.get('username', user.username)
    user.email = input.get('email', user.email)
    input.get('email') and user.set_password(input['password'])
    user.save()
    return user
