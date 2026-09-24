"""红黑树：二叉搜索树 + 平衡着色，5 条性质保证 log 高度。

性质：
  1. 每个节点非红即黑
  2. 根是黑色
  3. 每个叶（NIL 哨兵）是黑色
  4. 红色节点的两个子节点都是黑色（红节点不能有红孩子）
  5. 任一节点到其每个叶子的简单路径含相同数量的黑节点（黑高相等）

公开 API：insert(key) / delete(key) / search(key) -> bool /
inorder() -> list[int]（升序）/ validate() -> None（性质不满足抛异常）
"""
from __future__ import annotations


class RBNode:
    RED = 1
    BLACK = 0

    __slots__ = ("key", "color", "left", "right", "parent")

    def __init__(self, key, color=RED):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class RBTree:
    def __init__(self):
        self.NIL = RBNode(None, RBNode.BLACK)
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.root = self.NIL

    # ------------------------------------------------------------ 基础操作
    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    def _search_node(self, key):
        x = self.root
        while x != self.NIL:
            if key == x.key:
                return x
            x = x.left if key < x.key else x.right
        return self.NIL

    # ------------------------------------------------------------ 插入
    def insert(self, key):
        z = RBNode(key)
        z.left = self.NIL
        z.right = self.NIL
        y = None
        x = self.root
        while x != self.NIL:
            if key == x.key:
                return  # 已存在，忽略重复插入
            y = x
            x = x.left if key < x.key else x.right
        z.parent = y
        if y is None:
            self.root = z
        elif key < y.key:
            y.left = z
        else:
            y.right = z
        self._insert_fixup(z)

    def _insert_fixup(self, z):
        while z.parent is not None and z.parent.color == RBNode.RED:
            if z.parent == z.parent.parent.left:
                uncle = z.parent.parent.right
                if uncle.color == RBNode.RED:
                    z.parent.color = RBNode.BLACK
                    # BUG: uncle 未变黑
                    z.parent.parent.color = RBNode.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self._rotate_left(z)
                    z.parent.color = RBNode.BLACK
                    z.parent.parent.color = RBNode.RED
                    self._rotate_right(z.parent.parent)
            else:
                uncle = z.parent.parent.left
                if uncle.color == RBNode.RED:
                    z.parent.color = RBNode.BLACK
                    # BUG: uncle 未变黑
                    z.parent.parent.color = RBNode.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._rotate_right(z)
                    z.parent.color = RBNode.BLACK
                    z.parent.parent.color = RBNode.RED
                    self._rotate_left(z.parent.parent)
        self.root.color = RBNode.BLACK

    # ------------------------------------------------------------ 删除
    def delete(self, key):
        node = self._search_node(key)
        if node == self.NIL:
            return
        y = node
        y_original_color = y.color
        if node.left == self.NIL:
            x = node.right
            self._transplant(node, node.right)
        elif node.right == self.NIL:
            x = node.left
            self._transplant(node, node.left)
        else:
            y = self._minimum(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            self._transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color
        if y_original_color == RBNode.BLACK:
            self._delete_fixup(x)

    def _delete_fixup(self, x):
        while x != self.root and x.color == RBNode.BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == RBNode.RED:
                    w.color = RBNode.BLACK
                    x.parent.color = RBNode.RED
                    self._rotate_left(x.parent)
                    w = x.parent.right
                if w.left.color == RBNode.BLACK and w.right.color == RBNode.BLACK:
                    # BUG: 兄弟未变红，黑高不守恒
                    x = x.parent
                else:
                    if w.right.color == RBNode.BLACK:
                        w.left.color = RBNode.BLACK
                        w.color = RBNode.RED
                        self._rotate_right(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = RBNode.BLACK
                    w.right.color = RBNode.BLACK
                    self._rotate_left(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == RBNode.RED:
                    w.color = RBNode.BLACK
                    x.parent.color = RBNode.RED
                    self._rotate_right(x.parent)
                    w = x.parent.left
                if w.right.color == RBNode.BLACK and w.left.color == RBNode.BLACK:
                    w.color = RBNode.RED
                    x = x.parent
                else:
                    if w.left.color == RBNode.BLACK:
                        w.right.color = RBNode.BLACK
                        w.color = RBNode.RED
                        self._rotate_left(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = RBNode.BLACK
                    w.left.color = RBNode.BLACK
                    self._rotate_right(x.parent)
                    x = self.root
        x.color = RBNode.BLACK

    # ------------------------------------------------------------ 查询
    def search(self, key) -> bool:
        return self._search_node(key) != self.NIL

    def inorder(self):
        out = []

        def walk(node):
            if node == self.NIL:
                return
            walk(node.left)
            out.append(node.key)
            walk(node.right)

        walk(self.root)
        return out

    # ------------------------------------------------------------ 自检
    def validate(self):
        """校验 5 条红黑性质 + 二叉搜索有序性；不满足抛 RuntimeError。"""
        if self.root == self.NIL:
            return
        if self.root.color != RBNode.BLACK:
            raise RuntimeError("性质2破坏：根不是黑色")
        self._check_red_children(self.root)
        self._check_black_height(self.root)
        seq = self.inorder()
        if any(seq[i] >= seq[i + 1] for i in range(len(seq) - 1)):
            raise RuntimeError("二叉搜索树有序性破坏")

    def _check_red_children(self, node):
        if node == self.NIL:
            return
        if node.color == RBNode.RED:
            if node.left.color != RBNode.BLACK or node.right.color != RBNode.BLACK:
                raise RuntimeError("性质4破坏：红节点的孩子不是黑色")
        self._check_red_children(node.left)
        self._check_red_children(node.right)

    def _check_black_height(self, node):
        """返回黑高；左右子树黑高不等抛异常。"""
        if node == self.NIL:
            return 1
        left_h = self._check_black_height(node.left)
        right_h = self._check_black_height(node.right)
        if left_h != right_h:
            raise RuntimeError(
                f"性质5破坏：节点 {node.key} 左右黑高 {left_h} != {right_h}"
            )
        return left_h + (1 if node.color == RBNode.BLACK else 0)
