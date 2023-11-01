#!/usr/bin/env python
# coding: utf-8

from collections import Counter
import json
import time

from tabulate import tabulate


start_time = time.time()

# Create counter variable
tag_counts = Counter()

# Parse through the whole json file
with open('list.json', 'r') as f:
    for line in f:
        item = json.loads(line)
        # Either create a new entry if tag doesn't exist yet or add one to already existing counter entry
        try:
            for tag in item['tags']:
                tag_counts[tag] += 1
        except:
            pass

# Extract only the top 5 tags
top_tags = tag_counts.most_common(5)

print(tabulate(top_tags, headers=['tag', '#usage'], tablefmt="psql"))

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Script execution time: {elapsed_time:.2f} seconds")
