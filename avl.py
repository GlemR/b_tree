class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class AVL:
    def __init__(self):
        self.root = None

    def tree_to_vine(self, root):
        vine_tail = root
        remainder = root.right
        while remainder:
            if remainder.left is None:
                vine_tail = remainder
                remainder = remainder.right
            else:
                temp = remainder.left
                remainder.left = temp.right
                temp.right = remainder
                remainder = temp
                vine_tail.right = temp
                vine_tail = temp

    def rotate_left(self, grandparent, parent, child):
        if grandparent:
            grandparent.right = child
        else:
            self.root = child
        parent.right = child.left
        child.left = parent

    def rotate_right(self, grandparent, parent, child):
        if grandparent:
            grandparent.right = child
        else:
            self.root = child
        parent.left = child.right
        child.right = parent

    def vine_to_tree(self, root, size):
        if root is None:
            return None

        m = size + 1 - 2 ** ((size + 1).bit_length() - 1)
        current = root
        for _ in range(m):
            grandparent = None
            parent = current
            child = current.right
            self.rotate_left(grandparent, parent, child)
            current = child
        size -= m
        while size > 1 and current and current.right:  # Check if current and current.right are not None
            grandparent = None
            parent = current
            child = current.right.right
            self.rotate_left(grandparent, parent, child)
            current = child
            size -= 2
        if current:  # Check if current is not None
            current = root
            while current.right:
                grandparent = None
                parent = current
                child = current.right
                self.rotate_right(grandparent, parent, child)
                current = grandparent
        return root

    def balance(self):
        if not self.root:
            return
        size = 0
        current = self.root
        while current:
            if current.left:
                self.rotate_right(None, current, current.left)
                current = current.left
            else:
                size += 1
                current = current.right
        self.tree_to_vine(self.root)
        self.root = self.vine_to_tree(self.root, size)

    def insert(self, key):
        if not self.root:
            self.root = Node(key)
            return
        current = self.root
        while True:
            if key < current.key:
                if current.left:
                    current = current.left
                else:
                    current.left = Node(key)
                    return
            elif key > current.key:
                if current.right:
                    current = current.right
                else:
                    current.right = Node(key)
                    return
            else:
                return

    def find_level(self, root, key, level):
        if root is None:
            return -1
        if root.key == key:
            return level
        left_level = self.find_level(root.left, key, level + 1)
        if left_level != -1:
            return left_level
        return self.find_level(root.right, key, level + 1)

    def print_same_level(self, root, level, current_level=1):
        if root is None:
            return
        if current_level == level:
            print(root.key, end=" ")
        else:
            self.print_same_level(root.left, level, current_level + 1)
            self.print_same_level(root.right, level, current_level + 1)

    def delete(self, root, key):
        if root is None:
            return root
        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.find_min(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)
        if root is None:
            return root
        return root

    def find_min(self, root):
        current = root
        while current.left is not None:
            current = current.left
        return current

    def find_max(self, root):
        current = root
        while current.right is not None:
            current = current.right
        return current

    def inorder_traversal(self, root):
        if root:
            self.inorder_traversal(root.right)
            print(root.key, end=" ")
            self.inorder_traversal(root.left)

    def preorder_traversal(self, root):
        if root:
            print(root.key, end=" ")
            self.preorder_traversal(root.left)
            self.preorder_traversal(root.right)

    def postorder_traversal(self, root):
        if root:
            self.postorder_traversal(root.left)
            self.postorder_traversal(root.right)
            print(root.key, end=" ")

    def find_subtree(self, root, key):
        if root is None:
            return None
        if root.key == key:
            return root
        elif key < root.key:
            return self.find_subtree(root.left, key)
        else:
            return self.find_subtree(root.right, key)

    # Function to print a subtree using pre-order traversal
    def print_subtree(self, subtree):
        if subtree:
            print("\nPreorder traversal of the subtree:")
            self.preorder_traversal(subtree)
            print("\n")
        else:
            print("Subtree not found.")

    # Function to delete a subtree rooted at a given key using post-order traversal
    def delete_subtree(self, root, key):
        subtree_root = self.find_subtree(root, key)
        if subtree_root:
            self.postorder_traversal(subtree_root)
            print("\nDeleting subtree rooted at", key)
            root = self.delete(root, key)
            print("Inorder traversal after deletion:")
            self.inorder_traversal(root)
        else:
            print("Subtree not found.")


# Example usage:
avl_tree = AVL()
def avl_create(arr):
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        key = arr[mid]
        avl_tree.insert(key)
        avl_create(arr[left:mid])
        left = mid + 1

# Example usage:
my_list = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
avl_create(my_list)

print("Inorder traversal of the tree before balancing:")
avl_tree.inorder_traversal(avl_tree.root)

print("\nPreorder traversal of the tree before balancing:")
avl_tree.preorder_traversal(avl_tree.root)

print("\nPostorder traversal of the tree before balancing:")
avl_tree.postorder_traversal(avl_tree.root)

key = int(input("\nEnter the key you want to delete: "))
level = avl_tree.find_level(avl_tree.root, key, 1)
if level == -1:
    print("Key not found in the tree.")
else:
    print(f"Nodes on level {level}: ", end="")
    avl_tree.print_same_level(avl_tree.root, level)
    print("\nDeleting node with key", key)
    avl_tree.root = avl_tree.delete(avl_tree.root, key)
    print("\nInorder traversal after deletion:")
    avl_tree.inorder_traversal(avl_tree.root)

print("\nBalancing the tree...")
avl_tree.balance()

print("\nInorder traversal of the tree after balancing:")
avl_tree.inorder_traversal(avl_tree.root)

print("\nPreorder traversal of the tree after balancing:")
avl_tree.preorder_traversal(avl_tree.root)

print("\nPostorder traversal of the tree after balancing:")
avl_tree.postorder_traversal(avl_tree.root)
