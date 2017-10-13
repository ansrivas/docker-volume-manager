# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Initialize test modules."""

import os
from app import utils


def test_get_filename_from_path():
    """Test filename."""
    assert ["/abc/bcd", "test.tar.gz"] == utils.get_filename_from_path("/abc/bcd/test.tar.gz")
