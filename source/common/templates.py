# coding=utf-8

from string import Template


def substitute(template, obj):
    t = Template(template)
    return t.substitute(obj)


def substitute_u(template, obj):
    t = Template(unicode(template))
    return t.substitute(obj)


if __name__ == '__main__':
    # s = Template('$who like $what')
    # print(s.substitute(who='I', what='MBP'))
    #
    # su = Template(u'$who 喜欢 $what')
    # print(su.substitute({'who': 'I', 'what': 'MBP'}))

    obj = {'who': 'I', 'what': 'MBP'}
    print(substitute('$who like $what', obj))

    obj_u = {'who': u'我', 'what': '编程'}
    print(substitute_u(u'$who 喜欢 $what', obj_u))