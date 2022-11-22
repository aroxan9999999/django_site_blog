from email_validate import validate, validate_or_fail

email = validate(
    email_address='aroxan.999mail.ru',
    check_format=True,
    check_blacklist=True,
    check_dns=True,
    dns_timeout=10,
    check_smtp=False,
    smtp_debug=False)

print(email)