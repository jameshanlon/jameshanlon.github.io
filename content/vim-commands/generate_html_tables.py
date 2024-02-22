#!/usr/bin/env python

import sys
import re

with open(sys.argv[1]) as f:
    content = f.readlines()
content = [x for x in content if x.strip() != ""]
headers = [x.strip() for x in content[0].split("|")]
print('<table class="table table-striped table-sm">')
print("<thead>")
print("<tr>")
print("<th>{}</th>".format(headers[0]))
print("<th>{}</th>".format(headers[1]))
print("</tr>")
print("</thead>")
print("<tbody>")


def replace_code(s):
    s = re.sub(pattern=r"`((?:\\`|.)*?)`", repl="<code>\\1</code>", string=s)
    s = s.replace("\`", "`")
    return s


for line in content[1:]:
    row = [replace_code(x.strip()) for x in line.split("|")]
    print("<tr>")
    print("<td>{}</td>".format(row[0]))
    print("<td>{}</td>".format(row[1]))
    print("</tr>")
print("</tbody>")
print("</table>")
