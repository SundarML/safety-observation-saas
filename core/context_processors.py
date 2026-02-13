def organization_context(request):
    org = None

    if request.user.is_authenticated:
        org = getattr(request.user, "organization", None)

    return {
        "current_org": org,
        "current_user": request.user,
    }
