import base64


def base64url_decode(input):
    return base64.urlsafe_b64decode(input + "==")


def base64url_encode(input):
    stringAsBytes = input.encode("ascii")
    stringAsBase64 = (
        base64.urlsafe_b64encode(stringAsBytes).decode("utf-8").replace("=", "")
    )
    return stringAsBase64