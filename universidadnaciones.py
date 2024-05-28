import tkinter as tk
from tkinter import messagebox, filedialog

class Node:
    def __init__(self, student_id, student_data):
        self.student_id = student_id
        self.student_data = student_data
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def add(self, student_id, student_data):
        if not self.root:
            self.root = Node(student_id, student_data)
        else:
            self._add(self.root, student_id, student_data)

    def _add(self, current, student_id, student_data):
        if student_id < current.student_id:
            if current.left:
                self._add(current.left, student_id, student_data)
            else:
                current.left = Node(student_id, student_data)
        else:
            if current.right:
                self._add(current.right, student_id, student_data)
            else:
                current.right = Node(student_id, student_data)

    def search(self, student_id):
        return self._search(self.root, student_id)

    def _search(self, current, student_id):
        if not current:
            return None
        if current.student_id == student_id:
            return current.student_data
        elif student_id < current.student_id:
            return self._search(current.left, student_id)
        else:
            return self._search(current.right, student_id)

    def delete(self, student_id):
        self.root = self._delete(self.root, student_id)

    def _delete(self, current, student_id):
        if not current:
            return current

        if student_id < current.student_id:
            current.left = self._delete(current.left, student_id)
        elif student_id > current.student_id:
            current.right = self._delete(current.right, student_id)
        else:
            if not current.left:
                return current.right
            elif not current.right:
                return current.left

            temp = self._min_value_node(current.right)
            current.student_id = temp.student_id
            current.student_data = temp.student_data
            current.right = self._delete(current.right, temp.student_id)

        return current

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def list_students(self):
        students = []
        self._inorder(self.root, students)
        return students

    def _inorder(self, node, students):
        if node:
            self._inorder(node.left, students)
            students.append((node.student_id, node.student_data))
            self._inorder(node.right, students)

class AVLNode(Node):
    def __init__(self, student_id, student_data):
        super().__init__(student_id, student_data)
        self.height = 1

class AVL(BST):
    def __init__(self):
        super().__init__()

    def _add(self, current, student_id, student_data):
        if not current:
            return AVLNode(student_id, student_data)
        if student_id < current.student_id:
            current.left = self._add(current.left, student_id, student_data)
        else:
            current.right = self._add(current.right, student_id, student_data)

        current.height = 1 + max(self._get_height(current.left), self._get_height(current.right))

        balance = self._get_balance(current)

        if balance > 1:
            if student_id < current.left.student_id:
                return self._right_rotate(current)
            else:
                current.left = self._left_rotate(current.left)
                return self._right_rotate(current)

        if balance < -1:
            if student_id > current.right.student_id:
                return self._left_rotate(current)
            else:
                current.right = self._right_rotate(current.right)
                return self._left_rotate(current)

        return current

    def _delete(self, current, student_id):
        if not current:
            return current

        if student_id < current.student_id:
            current.left = self._delete(current.left, student_id)
        elif student_id > current.student_id:
            current.right = self._delete(current.right, student_id)
        else:
            if not current.left:
                return current.right
            elif not current.right:
                return current.left

            temp = self._min_value_node(current.right)
            current.student_id = temp.student_id
            current.student_data = temp.student_data
            current.right = self._delete(current.right, temp.student_id)

        current.height = 1 + max(self._get_height(current.left), self._get_height(current.right))

        balance = self._get_balance(current)

        if balance > 1:
            if self._get_balance(current.left) >= 0:
                return self._right_rotate(current)
            else:
                current.left = self._left_rotate(current.left)
                return self._right_rotate(current)

        if balance < -1:
            if self._get_balance(current.right) <= 0:
                return self._left_rotate(current)
            else:
                current.right = self._right_rotate(current.right)
                return self._left_rotate(current)

        return current

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

class StudentManagementApp:
    def __init__(self, root):
        self.bst = BST()
        self.avl = AVL()
        self.root = root
        self.root.title("Universidad Naciones")

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.id_label = tk.Label(self.frame, text="ID Estudiante")
        self.id_label.grid(row=0, column=0)
        self.id_entry = tk.Entry(self.frame)
        self.id_entry.grid(row=0, column=1)

        self.data_label = tk.Label(self.frame, text="Nombre Estudiante")
        self.data_label.grid(row=1, column=0)
        self.data_entry = tk.Entry(self.frame)
        self.data_entry.grid(row=1, column=1)

        self.add_button = tk.Button(self.frame, text="Añadir Estudiantes", command=self.add_student)
        self.add_button.grid(row=2, column=0)

        self.search_button = tk.Button(self.frame, text="Buscar Estudiantes", command=self.search_student)
        self.search_button.grid(row=2, column=1)

        self.delete_button = tk.Button(self.frame, text="Eliminar Estudiantes", command=self.delete_student)
        self.delete_button.grid(row=3, column=0)

        self.list_button = tk.Button(self.frame, text="Listar Estudiantes", command=self.list_students)
        self.list_button.grid(row=3, column=1)

        self.visualize_bst_button = tk.Button(self.frame, text="Visualizar ABB", command=self.visualize_bst)
        self.visualize_bst_button.grid(row=4, column=0)

        self.visualize_avl_button = tk.Button(self.frame, text="Visualizar AVL", command=self.visualize_avl)
        self.visualize_avl_button.grid(row=4, column=1)

        self.export_button = tk.Button(self.frame, text="Exportar Datos", command=self.export_data)
        self.export_button.grid(row=5, column=0)

        self.output_text = tk.Text(self.frame, height=10, width=50)
        self.output_text.grid(row=6, columnspan=2)

    def add_student(self):
        student_id = int(self.id_entry.get())
        student_data = self.data_entry.get()
        self.bst.add(student_id, student_data)
        self.avl.add(student_id, student_data)
        messagebox.showinfo("Exitoso", "Estudiante Añadido Correctamente")

    def search_student(self):
        student_id = int(self.id_entry.get())
        student_data = self.bst.search(student_id)
        if student_data:
            messagebox.showinfo("Estudiante Encontrado: ", f"ID: {student_id}, Nombre: {student_data}")
        else:
            messagebox.showinfo("Estudiante No Encontrado", "No existe ningun estudiante con esta ID")

    def delete_student(self):
        student_id = int(self.id_entry.get())
        self.bst.delete(student_id)
        self.avl.delete(student_id)
        messagebox.showinfo("Exitoso", "Estudiante Eliminado Correctamente")

    def list_students(self):
        students = self.bst.list_students()
        self.output_text.delete(1.0, tk.END)
        for student_id, student_data in students:
            self.output_text.insert(tk.END, f"ID: {student_id}, Nombre: {student_data}\n")

    def visualize_bst(self):
        self.output_text.delete(1.0, tk.END)
        self._visualize_tree(self.bst.root, "", True)

    def visualize_avl(self):
        self.output_text.delete(1.0, tk.END)
        self._visualize_tree(self.avl.root, "", True)

    def _visualize_tree(self, node, indent, last):
        if node:
            self.output_text.insert(tk.END, indent)
            if last:
                self.output_text.insert(tk.END, "R----")
                indent += "     "
            else:
                self.output_text.insert(tk.END, "L----")
                indent += "|    "
            self.output_text.insert(tk.END, f"{node.student_id}\n")
            self._visualize_tree(node.left, indent, False)
            self._visualize_tree(node.right, indent, True)

    def export_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            students = self.bst.list_students()
            with open(file_path, "w") as file:
                for student_id, student_data in students:
                    file.write(f"ID: {student_id}, Nombre: {student_data}\n")
            messagebox.showinfo("Exitoso", "Datos Exportados Correctamente")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementApp(root)
    root.mainloop()