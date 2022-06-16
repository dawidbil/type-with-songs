import pytest
import game.utils as utils


@pytest.mark.parametrize("length", [0, 1, 10])
def test_generate_character_queue(length):
    characters = utils.generate_character_list(length)
    all_characters = utils.get_all_letters()
    assert isinstance(characters, list) == True
    assert len(characters) == length
    for character in characters:
        assert character in all_characters


@pytest.mark.parametrize("width, height", [(i, i) for i in [0, 1, 10]])
def test_generate_random_pos(width, height):
    pos = utils.generate_random_pos(width, height)
    assert isinstance(pos, tuple)
    assert len(pos) == 2
    assert 0 <= pos[0] <= width
    assert 0 <= pos[1] <= height
