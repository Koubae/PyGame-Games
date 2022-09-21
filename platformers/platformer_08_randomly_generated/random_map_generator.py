"SImple Random Map Generator that generats CSV without a header, recommended only for testing purposes"
import random

def gen(write_csv: bool = False, height_offset: int = 0, widht_offset: int = 0) -> list:
    MAP_NAME = "map.csv"
    MAP_LENGTH = 20  # The visible map length
    MAP_TALL = 10  # THe Visible Map tall

    TILE_SIZE = 64
    WIDTH = TILE_SIZE * MAP_LENGTH  # The window width
    HEIGHT = TILE_SIZE * MAP_TALL  # The window height

    MAP_LENGTH_TOTAL = (MAP_LENGTH * 20) + (widht_offset + 1) # The total map legnth
    MAP_TALL_TOTAL = (MAP_TALL * 4) + (height_offset + 1)  # The Total Map hegith

    # blocks
    # air blocks
    empty = 0
    cloud = -1

    # ground blocks
    ground = 1
    grass = 2
    rock = 3
    water = 4

    # Here we define what we can find and what level
    # where 0 is the top (sky) and MAP_TALL_TOTAL - 1 is the lowser ground
    # kets are blocks type , values  are the ranges where is possible to find them
    # + the frequency to how easy is to find them.
    # 0 frequency: cannot find
    # 1 frequency: very common
    # 1+ frequency: highest numner the more rare is
    terrains_map = {
        -1: {  # cloud
            'range': list(range(0 , 4)),
            'frequency': 15
        },
        0: {  # empty
            'range': list(range(0, MAP_TALL_TOTAL + height_offset)),
            'frequency': 1
        },

        # ground blocks
        1: {  # ground
            'range': list(range(15, MAP_TALL_TOTAL + height_offset)),
            'frequency': 8
        },
        2: {  # grass
            'range': list(range(10 , 25)),
            'frequency': 8
        },
        3: {  # rock
            'range': list(range(20, MAP_TALL_TOTAL + height_offset)),
            'frequency': 10
        },
        4: {  # water
            'range': list(range(15, MAP_TALL_TOTAL + height_offset)),
            'frequency': 20
        },
    }

    # generate empty map
    map_struct = [
        [empty for _ in range(MAP_LENGTH_TOTAL)]
        for _ in range(MAP_TALL_TOTAL)

    ]
    for terrain_level, map_row in enumerate(map_struct):
        # now that we have the possible
        terrain_level_actual: int = terrain_level + height_offset
        for index, cell in enumerate(map_row):



            # Collect all terrain type depending on the level we are ate
            terrains = {
                t_type: t_data
                for t_type, t_data in terrains_map.items()
                if terrain_level_actual in t_data["range"]
            }
            if not terrains:
                print("opps")
            # Note: we sort the terrains by the lowest frequency to highest
            terrains = {k: v for k, v in
                        sorted(terrains.items(), key=lambda item: item[1].get('frequency'), reverse=True)}

            current = None
            to_use = None
            for block, terrain in terrains.items():
                current = block

                # test if this block is going to render here
                terrain_frequency = terrain['frequency'] - terrain_level
                if terrain_frequency < 1:
                    terrain_frequency = 1


                to_render = random.randint(0, terrain_frequency)
                if to_render == 1:
                    to_use = block
                    break

            if not to_use:  # if nothing was picked then we pick the latest (which lowert- more commont frequency)
                to_use = current

            block = to_use  # now we have the next block type!

            map_row[index] = block

    # stringigy the map

    # write map csv
    if write_csv:
        with open(MAP_NAME, 'w') as map_csv:
            for row in map_struct:
                row_stringified = ','.join([str(cell) for cell in row])
                map_csv.write(row_stringified + '\n')

    return map_struct

if __name__ == '__main__':
    gen()
