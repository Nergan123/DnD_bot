import json
import random
import os


class illusions:
    SERIALIZABLE_FIELDS = [
        'names_orig',
        'ids_orig',
        'names_swapped',
        'ids_swapped',
        'leshiy',
        'orig_leshiy_name'
    ]

    def __init__(self, player_list, ids):
        self.names_orig = player_list
        self.ids_orig = ids
        self.names_swapped = player_list
        self.ids_swapped = ids
        self.leshiy = ''
        self.orig_leshiy_name = ''
        self.load_state()

    def swap(self):
        index = list(range(len(self.names_orig)))
        random.shuffle(index)
        self.names_swapped = []
        self.ids_swapped = []
        for ind in index:
            self.names_swapped.append(self.names_orig[ind])
            self.ids_swapped.append(self.ids_orig[ind])
        self.save_state()

        return self.names_swapped

    def transform(self, id):
        self.leshiy = id
        index = self.ids_orig.index(id)
        self.orig_leshiy_name = self.names_orig[index]
        self.save_state()

    def save_state(self):
        state = {}
        for property_name in self.SERIALIZABLE_FIELDS:
            state[property_name] = self.__getattribute__(property_name)

        # s3 = boto3.resource('s3')
        # remote_object = s3.Object(self.STATE_BUCKET, self.STATE_REMOTE_FILE_NAME)
        # remote_object.put(Body=(bytes(json.dumps(state).encode('UTF-8'))))
        with open('illusions_data.json', 'w') as f:
            json.dump(state, f)

    def load_state(self):
        # s3 = boto3.client('s3')
        # s3_response = s3.get_object(Bucket=self.STATE_BUCKET, Key=self.STATE_REMOTE_FILE_NAME)
        # state_json = s3_response['Body'].read()
        with open('illusions_data.json', 'r') as f:
            state = json.loads(f.read())
        print(state)
        for property_name in self.SERIALIZABLE_FIELDS:
            self.__setattr__(property_name, state[property_name])
