import dataset

db = dataset.connect('sqlite:///data/data.db')
table = db['subscriptions']


for i in table:
    print(i)
