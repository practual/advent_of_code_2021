with open('input') as f:
    algorithm = f.readline().strip('\n')
    image = [[col for col in row] for row in f.read().split('\n') if row]


def pad_image(image, padding):
    new_image = [[padding for i in range(len(image[0]) + 2)]]
    for row in image:
        new_image.append([padding] + row + [padding])
    new_image.append([padding for i in range(len(image[0]) + 2)])
    return new_image


def get_image_value(image, x, y, default):
    if x < 0 or y < 0:
        return default
    try:
        return image[x][y]
    except IndexError:
        return default


def get_algorithm_key(image, x, y, default):
    block_coords = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
    pixel_string = ''
    for coords in block_coords:
        pixel_string += get_image_value(image, x + coords[0], y + coords[1], default)
    binary_string = ''.join(['0' if p == '.' else '1' for p in pixel_string])
    new_val = algorithm[int(binary_string, base=2)]
    return algorithm[int(binary_string, base=2)]


def enhance(image, padding):
    image = pad_image(image, padding)
    new_image = []
    for x, row in enumerate(image):
        new_image.append([])
        for y in range(len(row)):
            new_image[x].append(get_algorithm_key(image, x, y, padding))
    return new_image


def enhance_n_times(image, n):
    background = '.'
    for i in range(n):
        image = enhance(image, background)
        background = algorithm[0 if background == '.' else 511]
    return image


def count_pixels(image):
    return sum(1 if col == '#' else 0 for row in image for col in row)


print(count_pixels(enhance_n_times(image, 2)))
print(count_pixels(enhance_n_times(image, 50)))

