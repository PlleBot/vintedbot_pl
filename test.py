import dataset

db = dataset.connect('sqlite:///data/data.db')
table = db['subscriptions']
table.insert({
        'url': 'rr',
        'channel_id': 'rr',
        'synced': False,
        'last_sync': 'tes'
    })

for i in table:
    print(i)
