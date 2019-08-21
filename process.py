import re
import logging
import threading
import concurrent.futures

# def thread_function(name):
#     logging.info("Thread %s: starting", name)
#     time.sleep(1)
#     logging.info("Thread %s: finishing", name)

# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

#     with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
#         executor.map(thread_function, range(3))

# str = "makan <b>nasi</b> di rumah makan <hello>padang</hello> di grand Indonesia <disease>sakit perut</disease>"
# x = re.findall("<[a-zA-Z]*>(.*?)<\/[a-zA-Z]*>", str)
# print(x)

# str = "<makan>"
# x = re.match("<[a-zA-Z]*>", str)
# print(x)
# print(x.group(0))

# str = "</makan>"
# x = re.match("<\/[a-zA-Z]*>", str)
# print(x)
# print(x.group(0))

str = "makan <b>nasi</b> di rumah makan <hello>padang</hello> di grand Indonesia <disease>sakit perut perut perut</disease>"
words =  [x.strip().lower() for x in str.split() if x.strip()] # Hapus seluruh empty char pada list
print(words)
for idx, word in enumerate(words):
    tag = re.match("(<[a-zA-Z]*>)(.*?)(<\/[a-zA-Z]*>)", word)
    if tag:
        # print(tag)
        print(tag.group(1))
        print(tag.group(2))
        print(tag.group(3))
        continue

    tag = re.match("(<[a-zA-Z]*>)(.*?)$", word)
    if tag:
        # print(tag)
        print(tag.group(1))
        print(tag.group(2))
        continue
    
    tag = re.match("^(.*?)(<\/[a-zA-Z]*>)", word)
    if tag:
        # print(tag)
        print(tag.group(1))
        print(tag.group(2))
        continue

    print(word)