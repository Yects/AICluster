from dataclasses import dataclass
from typing import List, Dict, Tuple, Any, Optional, Union
import numpy as np
from tinygrad import dtypes
from tinygrad.codegen.kernel import Kernel
# from tinygrad import Linearizer

@dataclass
class UOp:
    op: str
    dtype: Any
    args: List[Any]

@dataclass
class Kernel:
    name: str
    uops: List[UOp]

class ASTNode:
    def __init__(self, op: str, dtype: Any, args: List[Any]):
        self.op = op
        self.dtype = dtype
        self.args = args

class Linearizer:
    def __init__(self, name: str, ast: List[ASTNode], opts: Dict[str, Any]):
        self.name = name
        self.ast = ast
        self.opts = opts
        self.uops: List[UOp] = []
