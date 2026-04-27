from libresprite_py.ordered_dither import BayerMatrix, Palette, color_distance, dither_rgb_pixel_to_index


def test_bayer_matrix_2x2_values() -> None:
    matrix = BayerMatrix(2)
    assert matrix.max_value() == 4
    assert [matrix.at(i, j) for i in range(2) for j in range(2)] == [0, 2, 3, 1]


def test_bayer_matrix_4x4_first_row_matches_expected_pattern() -> None:
    matrix = BayerMatrix(4)
    assert [matrix.at(0, j) for j in range(4)] == [0, 8, 2, 10]


def test_color_distance_is_zero_for_equal_colors() -> None:
    c = (42, 77, 123, 255)
    assert color_distance(c, c) == 0


def test_transparent_pixel_returns_transparent_index() -> None:
    matrix = BayerMatrix(2)
    palette = Palette(colors=[(255, 0, 255, 0), (0, 0, 0, 255), (255, 255, 255, 255)])
    index = dither_rgb_pixel_to_index(matrix, (10, 10, 10, 0), 0, 0, palette, transparent_index=0)
    assert index == 0


def test_dither_selects_one_of_two_nearest_colors() -> None:
    matrix = BayerMatrix(2)
    palette = Palette(colors=[(0, 0, 0, 255), (255, 255, 255, 255)])
    index = dither_rgb_pixel_to_index(matrix, (127, 127, 127, 255), 1, 1, palette)
    assert index in (0, 1)
