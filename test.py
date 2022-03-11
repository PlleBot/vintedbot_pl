import dataset

db = dataset.connect('sqlite:///data/data2.db')
table = db['subscriptions']
table.insert({
        'url': 'rr',
        'channel_id': 'rr',
        'synced': False,
        'last_sync': 'tes'
    })
