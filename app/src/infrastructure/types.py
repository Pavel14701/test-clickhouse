# -*- coding: utf-8 -*-

from aiohttp import ClientSession
from typing import Any, Dict, List, TypeVar

T = TypeVar('T', bound=ClientSession)
"""
Тип переменной T, ограниченный классом ClientSession.
"""

F = TypeVar('F', bound=List[Dict[str, Any]])
"""
Тип переменной F, ограниченный списком словарей, где ключи строки, а значения могут быть любыми типами.
"""

Z = TypeVar('Z')
"""
Тип переменной Z, без ограничений.
"""
