def verify_social_email(strategy, details, backend, user=None, *args, **kwargs):
    if user and hasattr(user, 'email_verified'):
        if backend.name in ('google-oauth2', 'github'):
            user.email_verified = True
            user.save(update_fields=["email_verified"])

    return {"user": user, **kwargs}