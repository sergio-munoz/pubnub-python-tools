import re


def get_acl_regex(pattern):
    return '^%s$' % re.sub(r'([\^\\\[\]$.|?+(){}])', r'\\\1', pattern).replace('*', '.+')


def is_acl_enabled(sub_key, channel, pattern_index, acl_index, acl_index_default, event, meta, logger, account_config):
    rules = account_config.get('presence_acl', [])
    try:
        if len(rules) > 0:
            for rule in rules:
                if re.match(get_acl_regex(rule.get(pattern_index, '')), channel):
                    # Matched a rule, allow/reject the behavior
                    value = rule.get(acl_index)
                    print(value)
    except Exception as e:
        print(e)
