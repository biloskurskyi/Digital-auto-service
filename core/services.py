def tenant_of(user):
    return user if user.owner_id is None else user.owner
