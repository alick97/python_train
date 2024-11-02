import re

my_names = set(['rosa', 'rose', 'chatty', 'chatbot', 'bot', 'chatterbot'])
curt_names = set(['hal', 'you', 'u'])
greeter_name = 'guest'

r = (
    r"[^a-z]*([y]?o|[h']?ello|ok|hey|(good[ ])?(morn[gin']{0,3}|"
    r"afternoon|even[gin']{0,3}))[\s,;:]{1,3}([a-z]{1,20})"
)
re_greeting = re.compile(r, flags=re.IGNORECASE)

def run_match(s):
    print(f"request: {s}")
    match = re_greeting.match(s)
    print("response: ", end="")
    if match:
        at_name = match.groups()[-1]
        if at_name in curt_names:
            print("Good one.")
        elif at_name.lower() in my_names:
            print("Hi {}, How are you?".format(greeter_name))
    else:
        print("no match")

# example import
examples = [
  "Hello Rosa",
  "Good morning Rosa",
  "321321 Good morning Rosa",
  "Good Manning Rosa",
  "Good evening Rosa",
  "Good Morn'n Rosa",
  "Good evening Rosa Parks",
  "Good evening u",
  "yo Rosa",
]

for s in examples:
    run_match(s)

# request: Hello Rosa
# response: Hi guest, How are you?
# request: Good morning Rosa
# response: Hi guest, How are you?
# request: 321321 Good morning Rosa
# response: Hi guest, How are you?
# request: Good Manning Rosa
# response: no match
# request: Good evening Rosa
# response: Hi guest, How are you?
# request: Good Morn'n Rosa
# response: Hi guest, How are you?
# request: Good evening Rosa Parks
# response: Hi guest, How are you?
# request: Good evening u
# response: Good one.
# request: yo Rosa
# response: Hi guest, How are you?
