import json


class Base_class:
    SERIALIZABLE_FIELDS = [

    ]

    def __init__(self, name):
        self.name = name

    def save_state(self):
        print(f'Saving {self.name}_data.json')
        state = {}
        for property_name in self.SERIALIZABLE_FIELDS:
            state[property_name] = self.__getattribute__(property_name)

        # s3 = boto3.resource('s3')
        # remote_object = s3.Object(self.STATE_BUCKET, self.STATE_REMOTE_FILE_NAME)
        # remote_object.put(Body=(bytes(json.dumps(state).encode('UTF-8'))))
        with open(f'{self.name}_data.json', 'w') as f:
            json.dump(state, f)

    def load_state(self):
        print(f'Loading {self.name}_data.json')
        # s3 = boto3.client('s3')
        # s3_response = s3.get_object(Bucket=self.STATE_BUCKET, Key=self.STATE_REMOTE_FILE_NAME)
        # state_json = s3_response['Body'].read()
        with open(f'{self.name}_data.json', 'r') as f:
            state = json.loads(f.read())
        print(state)
        for property_name in self.SERIALIZABLE_FIELDS:
            self.__setattr__(property_name, state[property_name])
