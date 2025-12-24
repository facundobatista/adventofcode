def get_blocks(lines):
    """Split a bunch of lines in block of lines separated by empty lines.

    The empty lines are consumed.
    """
    block = []
    for line in lines:
        if line:
            block.append(line)
        else:
            yield block
            block = []

    if block:
        yield block
