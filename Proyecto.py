from pymongo import MongoClient
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["blog"]

# Aplicación de Blog CRUD
class BlogApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Blog Management")
        self.geometry("600x500")
        self.create_tabs()

    def create_tabs(self):
        # Crear el contenedor de pestañas
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill='both')

        # Crear pestañas para cada colección
        self.article_tab = Frame(notebook)
        self.comment_tab = Frame(notebook)
        self.user_tab = Frame(notebook)
        self.category_tab = Frame(notebook)
        self.tag_tab = Frame(notebook)

        notebook.add(self.article_tab, text="Artículos")
        notebook.add(self.comment_tab, text="Comentarios")
        notebook.add(self.user_tab, text="Usuarios")
        notebook.add(self.category_tab, text="Categorías")
        notebook.add(self.tag_tab, text="Etiquetas del blog")

        # Crear interfaces de cada pestaña
        self.create_article_tab()
        self.create_comment_tab()
        self.create_user_tab()
        self.create_category_tab()
        self.create_tag_tab()

    # Pestana de Articulos
    def create_article_tab(self):
        Label(self.article_tab, text="Titulo").pack()
        self.article_title = Entry(self.article_tab)
        self.article_title.pack()

        Label(self.article_tab, text="Contenido").pack()
        self.article_content = Text(self.article_tab, height=5, width=50)
        self.article_content.pack()

        Label(self.article_tab, text="Nombre del autor").pack()
        self.article_author_id = Entry(self.article_tab)
        self.article_author_id.pack()

        Label(self.article_tab, text="Nombre de Tags").pack()
        self.article_tags = Entry(self.article_tab)
        self.article_tags.pack()

        Label(self.article_tab, text="Nombre de Categorias").pack()
        self.article_categories = Entry(self.article_tab)
        self.article_categories.pack()

        Button(self.article_tab, text="Crear Articulo", command=self.create_article).pack(pady=5)
        Button(self.article_tab, text="Leer Articulos", command=self.read_articles).pack(pady=5)
        Button(self.article_tab, text="Actualizar Articulo", command=self.update_article).pack(pady=5)
        Button(self.article_tab, text="Eliminar Articulo", command=self.delete_article).pack(pady=5)

    def create_article(self):
        title = self.article_title.get().strip()
        content = self.article_content.get("1.0", END).strip()
        author_id = self.article_author_id.get().strip()
        tags = self.article_tags.get().split(',')
        categories = self.article_categories.get().split(',')

        if title and content and author_id:
            # Verificar si el articulo ya existe
            if db.articles.find_one({"TITULO": title}):
                messagebox.showerror("Error", "El titulo del articulo ya existe. Usa un titulo diferente.")
                return

            # Verificar si el autor existe en la coleccion de usuarios
            if not db.users.find_one({"username": author_id}):
                messagebox.showerror("Error", "El autor no existe. No se puede crear el articulo.")
                return

            # Verificar que todas las categorias existan
            for category_name in categories:
                category_name = category_name.strip()
                if not db.categories.find_one({"name": category_name}):
                    messagebox.showerror("Error", f"La categoria '{category_name}' no existe.")
                    return

            # Verificar que todos los tags existan
            for tag_name in tags:
                tag_name = tag_name.strip()
                if not db.tags.find_one({"name": tag_name}):
                    messagebox.showerror("Error", f"El tag '{tag_name}' no existe.")
                    return

            db.articles.insert_one({
                "TITULO": title,
                "Contenido": content,
                "Id_del_autor": author_id,
                "ID_de_Tags": tags,
                "IDs_de_Categorias": categories
            })
            messagebox.showinfo("Success", "Articulo creado exitosamente")
        else:
            messagebox.showerror("Error", "Por favor completa todos los campos")

    def read_articles(self):
        articles = db.articles.find()
        display_text = "\n".join([f"Titulo: {article.get('TITULO', 'No Title')}, Contenido: {article.get('Contenido', 'No Content')}" for article in articles])
        messagebox.showinfo("Articulos", display_text if display_text else "No se encontraron articulos")

    def update_article(self):
        old_title = simpledialog.askstring("Actualizar Articulo", "Ingrese el titulo del articulo que desea actualizar:")
        if old_title:
            new_title = simpledialog.askstring("Nuevo Titulo", "Ingrese el nuevo titulo del articulo:")
            new_content = simpledialog.askstring("Nuevo Contenido", "Ingrese el nuevo contenido del articulo:")
            if new_title and new_content:
                result = db.articles.update_one({"TITULO": old_title}, {"$set": {"TITULO": new_title, "Contenido": new_content}})
                if result.matched_count:
                    messagebox.showinfo("Success", "Articulo actualizado exitosamente")
                else:
                    messagebox.showerror("Error", "Articulo no encontrado")

    def delete_article(self):
        title = simpledialog.askstring("Eliminar Articulo", "Ingrese el titulo del articulo que desea eliminar:")
        if title:
            result = db.articles.delete_one({"TITULO": title})
            if result.deleted_count:
                messagebox.showinfo("Success", "Articulo eliminado exitosamente")
            else:
                messagebox.showerror("Error", "Articulo no encontrado")




    # Pestana de Comentarios
    def create_comment_tab(self):
        Label(self.comment_tab, text="Nombre del Articulo").pack()
        self.comment_article_id = Entry(self.comment_tab)
        self.comment_article_id.pack()

        Label(self.comment_tab, text="Nombre del Usuario (Autor)").pack()
        self.comment_author_name = Entry(self.comment_tab)
        self.comment_author_name.pack()

        Label(self.comment_tab, text="Texto del Comentario").pack()
        self.comment_text = Text(self.comment_tab, height=5, width=50)
        self.comment_text.pack()

        Button(self.comment_tab, text="Crear Comentario", command=self.create_comment).pack(pady=5)
        Button(self.comment_tab, text="Leer Comentarios", command=self.read_comments).pack(pady=5)
        Button(self.comment_tab, text="Actualizar Comentario", command=self.update_comment).pack(pady=5)
        Button(self.comment_tab, text="Eliminar Comentario", command=self.delete_comment).pack(pady=5)

    # Crear un nuevo comentario
    def create_comment(self):
        article_id = self.comment_article_id.get().strip()
        author_name = self.comment_author_name.get().strip()
        text = self.comment_text.get("1.0", END).strip()

        if article_id and author_name and text:
            # Verificar si el articulo existe
            if not db.articles.find_one({"TITULO": article_id}):
                messagebox.showerror("Error", "El articulo no existe. No se puede agregar el comentario.")
                return

            # Verificar si el usuario existe en la coleccion de usuarios
            if not db.users.find_one({"username": author_name}):
                messagebox.showerror("Error", "El usuario no existe. No se puede agregar el comentario.")
                return

            # Verificar si el comentario ya existe en el articulo para el usuario
            if db.comments.find_one({"article_id": article_id, "author_name": author_name, "text": text}):
                messagebox.showerror("Error", "Este comentario ya existe para el articulo y usuario seleccionados.")
                return

            db.comments.insert_one({"article_id": article_id, "author_name": author_name, "text": text})
            messagebox.showinfo("Success", "Comentario creado exitosamente")
        else:
            messagebox.showerror("Error", "Por favor completa todos los campos")

    # Leer y mostrar todos los comentarios
    def read_comments(self):
        comments = db.comments.find()
        display_text = "\n".join([
            f"ID del Articulo: {comment.get('article_id', 'No ID')}, "
            f"Autor: {comment.get('author_name', 'No Autor')}, "
            f"Texto: {comment.get('text', 'No Content')}" 
            for comment in comments
        ])
        messagebox.showinfo("Comentarios", display_text if display_text else "No se encontraron comentarios")

    # Actualizar un comentario
    def update_comment(self):
        article_id = simpledialog.askstring("Actualizar Comentario", "Ingrese el ID del articulo asociado al comentario:")
        author_name = simpledialog.askstring("Actualizar Comentario", "Ingrese el nombre del autor del comentario:")
        if article_id and author_name:
            new_text = simpledialog.askstring("Nuevo Texto", "Ingrese el nuevo texto del comentario:")
            if new_text:
                result = db.comments.update_one(
                    {"article_id": article_id, "author_name": author_name},
                    {"$set": {"text": new_text}}
                )
                if result.matched_count:
                    messagebox.showinfo("Success", "Comentario actualizado exitosamente")
                else:
                    messagebox.showerror("Error", "Comentario no encontrado")

    # Eliminar un comentario
    def delete_comment(self):
        article_id = simpledialog.askstring("Eliminar Comentario", "Ingrese el ID del articulo asociado al comentario:")
        author_name = simpledialog.askstring("Eliminar Comentario", "Ingrese el nombre del autor del comentario:")
        if article_id and author_name:
            result = db.comments.delete_one({"article_id": article_id, "author_name": author_name})
            if result.deleted_count:
                messagebox.showinfo("Success", "Comentario eliminado exitosamente")
            else:
                messagebox.showerror("Error", "Comentario no encontrado")





    # Pestaña de Usuarios
    def create_user_tab(self):
        Label(self.user_tab, text="Nombre de Usuario").pack()
        self.user_name = Entry(self.user_tab)
        self.user_name.pack()

        Label(self.user_tab, text="Correo Electrónico").pack()
        self.user_email = Entry(self.user_tab)
        self.user_email.pack()

        Button(self.user_tab, text="Crear Usuario", command=self.create_user).pack(pady=5)
        Button(self.user_tab, text="Leer Usuarios", command=self.read_users).pack(pady=5)
        Button(self.user_tab, text="Actualizar Usuario", command=self.update_user).pack(pady=5)
        Button(self.user_tab, text="Eliminar Usuario", command=self.delete_user).pack(pady=5)

    def create_user(self):
        username = self.user_name.get().strip()
        email = self.user_email.get().strip()

        if username and email:
            # Verificar si el nombre de usuario ya está registrado
            if db.users.find_one({"username": username}):
                messagebox.showerror("Error", "El nombre de usuario ya está registrado. Usa un nombre de usuario diferente.")
                return
            
            # Verificar si el correo electrónico ya está en uso
            if db.users.find_one({"email": email}):
                messagebox.showerror("Error", "Este correo electrónico ya está registrado. Usa otro correo.")
                return

            db.users.insert_one({"username": username, "email": email})
            messagebox.showinfo("Success", "Usuario creado exitosamente")
        else:
            messagebox.showerror("Error", "Por favor completa todos los campos")

    def read_users(self):
        users = db.users.find()
        display_text = "\n".join([f"Nombre de Usuario: {user.get('username', 'No Username')}, Email: {user.get('email', 'No Email')}" for user in users])
        messagebox.showinfo("Usuarios", display_text if display_text else "No se encontraron usuarios")

    def update_user(self):
        old_username = simpledialog.askstring("Actualizar Usuario", "Ingrese el nombre de usuario que desea actualizar:")
        if old_username:
            new_username = simpledialog.askstring("Nuevo Nombre de Usuario", "Ingrese el nuevo nombre de usuario:")
            new_email = simpledialog.askstring("Nuevo Correo Electrónico", "Ingrese el nuevo correo electrónico:")
            if new_username and new_email:
                # Validar que el nuevo nombre de usuario y correo no existan ya en otro registro
                if db.users.find_one({"username": new_username, "_id": {"$ne": db.users.find_one({"username": old_username})["_id"]}}):
                    messagebox.showerror("Error", "El nuevo nombre de usuario ya está en uso.")
                    return
                if db.users.find_one({"email": new_email, "_id": {"$ne": db.users.find_one({"username": old_username})["_id"]}}):
                    messagebox.showerror("Error", "El nuevo correo electrónico ya está en uso.")
                    return

                result = db.users.update_one({"username": old_username}, {"$set": {"username": new_username, "email": new_email}})
                if result.matched_count:
                    messagebox.showinfo("Success", "Usuario actualizado exitosamente")
                else:
                    messagebox.showerror("Error", "Usuario no encontrado")

    def delete_user(self):
        username = simpledialog.askstring("Eliminar Usuario", "Ingrese el nombre de usuario que desea eliminar:")
        if username:
            result = db.users.delete_one({"username": username})
            if result.deleted_count:
                messagebox.showinfo("Success", "Usuario eliminado exitosamente")
            else:
                messagebox.showerror("Error", "Usuario no encontrado")

    # Pestaña de Categorías
    def create_category_tab(self):
        Label(self.category_tab, text="Nombre de la Categoría").pack()
        self.category_name = Entry(self.category_tab)
        self.category_name.pack()

        Label(self.category_tab, text="URL de la Categoría").pack()  # Campo de URL
        self.category_url = Entry(self.category_tab)
        self.category_url.pack()

        Button(self.category_tab, text="Crear Categoría", command=self.create_category).pack(pady=5)
        Button(self.category_tab, text="Leer Categorías", command=self.read_categories).pack(pady=5)
        Button(self.category_tab, text="Actualizar Categoría", command=self.update_category).pack(pady=5)
        Button(self.category_tab, text="Eliminar Categoría", command=self.delete_category).pack(pady=5)

    def create_category(self):
        name = self.category_name.get().strip()
        url = self.category_url.get().strip()

        if name and url:
            # Verificar si la categoría ya existe
            if db.categories.find_one({"name": name}):
                messagebox.showerror("Error", "La categoría ya existe.")
                return
            
            db.categories.insert_one({"name": name, "url": url})
            messagebox.showinfo("Success", "Categoría creada exitosamente")
        else:
            messagebox.showerror("Error", "Por favor proporciona un nombre y URL")

    def read_categories(self):
        categories = db.categories.find()
        display_text = "\n".join([f"Nombre: {category.get('name', 'No Name')}, URL: {category.get('url', 'No URL')}" for category in categories])
        messagebox.showinfo("Categorías", display_text if display_text else "No se encontraron categorías")

    def update_category(self):
        old_name = simpledialog.askstring("Actualizar Categoría", "Ingrese el nombre de la categoría que desea actualizar:")
        if old_name:
            new_name = simpledialog.askstring("Nuevo Nombre", "Ingrese el nuevo nombre de la categoría:")
            new_url = simpledialog.askstring("Nuevo URL", "Ingrese el nuevo URL de la categoría:")
            if new_name and new_url:
                # Verificar que el nuevo nombre no esté duplicado
                if db.categories.find_one({"name": new_name, "_id": {"$ne": db.categories.find_one({"name": old_name})["_id"]}}):
                    messagebox.showerror("Error", "El nuevo nombre de categoría ya está en uso.")
                    return
                
                result = db.categories.update_one({"name": old_name}, {"$set": {"name": new_name, "url": new_url}})
                if result.matched_count:
                    messagebox.showinfo("Success", "Categoría actualizada exitosamente")
                else:
                    messagebox.showerror("Error", "Categoría no encontrada")

    def delete_category(self):
        name = simpledialog.askstring("Eliminar Categoría", "Ingrese el nombre de la categoría que desea eliminar:")
        if name:
            result = db.categories.delete_one({"name": name})
            if result.deleted_count:
                messagebox.showinfo("Success", "Categoría eliminada exitosamente")
            else:
                messagebox.showerror("Error", "Categoría no encontrada")

    # Pestaña de Etiquetas
    def create_tag_tab(self):
        Label(self.tag_tab, text="Nombre de la Etiqueta").pack()
        self.tag_name = Entry(self.tag_tab)
        self.tag_name.pack()

        Label(self.tag_tab, text="URL de la Etiqueta").pack()  # Campo de URL
        self.tag_url = Entry(self.tag_tab)
        self.tag_url.pack()

        Button(self.tag_tab, text="Crear Etiqueta", command=self.create_tag).pack(pady=5)
        Button(self.tag_tab, text="Leer Etiquetas", command=self.read_tags).pack(pady=5)
        Button(self.tag_tab, text="Actualizar Etiqueta", command=self.update_tag).pack(pady=5)
        Button(self.tag_tab, text="Eliminar Etiqueta", command=self.delete_tag).pack(pady=5)

    def create_tag(self):
        name = self.tag_name.get().strip()
        url = self.tag_url.get().strip()

        if name and url:
            # Verificar si la etiqueta ya existe
            if db.tags.find_one({"name": name}):
                messagebox.showerror("Error", "La etiqueta ya existe.")
                return
            
            db.tags.insert_one({"name": name, "url": url})
            messagebox.showinfo("Success", "Etiqueta creada exitosamente")
        else:
            messagebox.showerror("Error", "Por favor proporciona un nombre y URL")

    def read_tags(self):
        tags = db.tags.find()
        display_text = "\n".join([f"Nombre: {tag.get('name', 'No Name')}, URL: {tag.get('url', 'No URL')}" for tag in tags])
        messagebox.showinfo("Etiquetas", display_text if display_text else "No se encontraron etiquetas")

    def update_tag(self):
        old_name = simpledialog.askstring("Actualizar Etiqueta", "Ingrese el nombre de la etiqueta que desea actualizar:")
        if old_name:
            new_name = simpledialog.askstring("Nuevo Nombre", "Ingrese el nuevo nombre de la etiqueta:")
            new_url = simpledialog.askstring("Nuevo URL", "Ingrese el nuevo URL de la etiqueta:")
            if new_name and new_url:
                # Verificar que el nuevo nombre no esté duplicado
                if db.tags.find_one({"name": new_name, "_id": {"$ne": db.tags.find_one({"name": old_name})["_id"]}}):
                    messagebox.showerror("Error", "El nuevo nombre de etiqueta ya está en uso.")
                    return
                
                result = db.tags.update_one({"name": old_name}, {"$set": {"name": new_name, "url": new_url}})
                if result.matched_count:
                    messagebox.showinfo("Success", "Etiqueta actualizada exitosamente")
                else:
                    messagebox.showerror("Error", "Etiqueta no encontrada")

    def delete_tag(self):
        name = simpledialog.askstring("Eliminar Etiqueta", "Ingrese el nombre de la etiqueta que desea eliminar:")
        if name:
            result = db.tags.delete_one({"name": name})
            if result.deleted_count:
                messagebox.showinfo("Success", "Etiqueta eliminada exitosamente")
            else:
                messagebox.showerror("Error", "Etiqueta no encontrada")


if __name__ == "__main__":
    app = BlogApp()
    app.mainloop()
