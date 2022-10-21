from helpers.base_class import Base_class


class Player(Base_class):
    SERIALIZABLE_FIELDS = [
        'name',
        'id_player',
        'initiative',
        'rolled_initiative'
    ]

    def __init__(self, file_name):
        super().__init__(file_name)
        self.file_name = file_name
        self.name = ''
        self.id_player = ''
        self.initiative = ''
        self.rolled_initiative = ''
