def as_float(value: str) -> float:
    return float(value.replace(',', ''))


def as_screenshot_path(id: str):
    return "./screenshots/{}.png".format(id)
