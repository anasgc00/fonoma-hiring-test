
criterions = ("completed", "pending", "all", "canceled")


def validate_criterion(criterion: str):
    return criterion in criterions
