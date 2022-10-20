import random
from helpers.base_class import Base_class


class illusions(Base_class):
    SERIALIZABLE_FIELDS = [
        'names_orig',
        'ids_orig',
        'names_swapped',
        'ids_swapped',
        'leshiy',
        'orig_leshiy_name'
    ]

    def __init__(self, player_list, ids):
        super().__init__('illusions')
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

    def transform(self, id_name):
        self.leshiy = id_name
        index = self.ids_orig.index(id_name)
        self.orig_leshiy_name = self.names_orig[index]
        self.save_state()
