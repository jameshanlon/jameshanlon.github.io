import random
import cgi

MOTIONS = ['l', 'h', 'j', 'k', 'w', 'e', 'b', 'B', '0', '$', '^', 'g_', '{',
        '}', 't{ch}', 'f{ch}', 'T{ch}', 'F{ch}', 'gg', 'G',
        '%', '[(', '[)', '[{', '[}', '/{pat}', '?{pat}']
OPERATORS = ['c', 'd', 'y', '~', '<', '>', 'g~', 'gu', 'gU', 'gq', 'g@']
TEXT_OBJECTS = ['w', 'W', 's', 'p', 't', '[', ']', '{', '}', '(', ')', '\'',
        '"', '`', '<', '>', 'b', 'B']
MODIFIERS = ['a', 'i']
REPEAT=32

def text_object(use_count=True):
    if use_count:
        count = int(random.random() * 10) if random.random() > 0.75 else ''
        return '{}{}{}'.format(count, random.choice(MODIFIERS), random.choice(TEXT_OBJECTS))
    else:
        return '{}{}'.format(random.choice(MODIFIERS), random.choice(TEXT_OBJECTS))

def motion():
    count = int(random.random() * 10) if random.random() > 0.75 else ''
    return '{}{}'.format(count, random.choice(MOTIONS))

def operator_text_object():
    count = int(random.random() * 10) if random.random() > 0.75 else ''
    return '{}{}{}'.format(count, random.choice(OPERATORS), text_object())

def operator_motion():
    count = int(random.random() * 10) if random.random > 0.75 else ''
    return '{}{}{}'.format(count, random.choice(OPERATORS), random.choice(MOTIONS))

def double_operator():
    return '{0}{0}'.format(random.choice(OPERATORS))

s="""
<div class="container">
  <div class="row">
    <div class="col-sm-3"><h3>Motions</h3></div>
    <div class="col-sm-3"><h3>Text objects</h3></div>
    <div class="col-sm-3"><h3>Operators on text objects</h3></div>
    <div class="col-sm-3"><h3>Operators on motions</h3></div>
  </div>
  <div class="row">
    <div class="col-sm-3">
      <div class="row">
	<div class="col-4">{}</div>
	<div class="col-4">{}</div>
      </div>
    </div>
    <div class="col-sm-3">
      <div class="row">
	<div class="col-4">{}</div>
	<div class="col-4">{}</div>
      </div>
    </div>
    <div class="col-sm-3">
      <div class="row">
	<div class="col-4">{}</div>
	<div class="col-4">{}</div>
      </div>
    </div>
    <div class="col-sm-3">
      <div class="row">
	<div class="col-4">{}</div>
	<div class="col-4">{}</div>
      </div>
    </div>
  </div>
</div>
"""
col1='<br>'.join(['<code>{}</code>'.format(cgi.escape(motion())) for x in range(REPEAT)])
col2='<br>'.join(['<code>{}</code>'.format(cgi.escape(motion())) for x in range(REPEAT)])
col3='<br>'.join(['<code>{}</code>'.format(cgi.escape(text_object(use_count=False))) for x in range(REPEAT)])
col4='<br>'.join(['<code>{}</code>'.format(cgi.escape(text_object(use_count=False))) for x in range(REPEAT)])
col5='<br>'.join(['<code>{}</code>'.format(cgi.escape(operator_text_object())) for x in range(REPEAT)])
col6='<br>'.join(['<code>{}</code>'.format(cgi.escape(operator_text_object())) for x in range(REPEAT)])
col7='<br>'.join(['<code>{}</code>'.format(cgi.escape(operator_motion())) for x in range(REPEAT)])
col8='<br>'.join(['<code>{}</code>'.format(cgi.escape(operator_motion())) for x in range(REPEAT)])
print s.format(col1, col2, col3, col4, col5, col6, col7, col8)
