#!/usr/bin/env python
import logging
import simuvex
import nose
import os
import angr
from angr_bf import *

def test_hello():
    """
    End-to-end Hello World path analysis
    :return:
    """
    hellobf = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../test_programs/hello.bf'))
    p = angr.Project(hellobf)
    entry = p.factory.entry_state()
    pg = p.factory.path_group(entry)
    pg.explore()
    nose.tools.assert_equals(pg.deadended[0].state.posix.dumps(1), 'Hello World!\n')

def test_1bytecrackme_good():
    """
    The world-famous 1-byte crackme (easy version)
    :return:
    """
    crackme = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../test_programs/1bytecrackme-good.bf'))
    bad_paths = lambda path: "-" in path.state.posix.dumps(1)
    p = angr.Project(crackme)
    entry = p.factory.entry_state(remove_options={simuvex.o.LAZY_SOLVES})
    pg = p.factory.path_group(entry)
    pg.step(until=lambda lpg: len(lpg.active) == 0)
    pg.stash(from_stash="deadended", to_stash="bad", filter_func=bad_paths)
    nose.tools.assert_equals("\n", pg.deadended[0].state.posix.dumps(0))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    test_hello()
    test_1bytecrackme_good()

