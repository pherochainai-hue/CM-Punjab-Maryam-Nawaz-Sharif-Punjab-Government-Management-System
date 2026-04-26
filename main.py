import sqlite3

class GovernmentEntity:

    def __init__(self, name, department):
        self.name = name
        self.department = department

    def display_info(self):
        raise NotImplementedError("Punjab Goverement  must implement this method")


class Project(GovernmentEntity):

    def __init__(self, name, department, budget):
        super().__init__(name, department)
        self.budget = budget

    def display_info(self):
        return f"[Project] {self.name} | {self.department} | Budget: {self.budget}"


class Scheme(GovernmentEntity):

    def __init__(self, name, department, beneficiaries):
        super().__init__(name, department)
        self.beneficiaries = beneficiaries

    def display_info(self):
        return f"[Scheme] {self.name} | {self.department} | Beneficiaries: {self.beneficiaries}"


def connect_db():
    return sqlite3.connect("punjab_govt.db")


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            department TEXT,
            budget REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schemes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            department TEXT,
            beneficiaries INTEGER
        )
    """)

    conn.commit()
    conn.close()


def add_project(project):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO projects (name, department, budget) VALUES (?, ?, ?)",
        (project.name, project.department, project.budget)
    )

    conn.commit()
    conn.close()


def view_projects():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT name, department, budget FROM projects")
    rows = cursor.fetchall()
    conn.close()

    return [Project(*row) for row in rows]


def add_scheme(scheme):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO schemes (name, department, beneficiaries) VALUES (?, ?, ?)",
        (scheme.name, scheme.department, scheme.beneficiaries)
    )

    conn.commit()
    conn.close()


def view_schemes():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT name, department, beneficiaries FROM schemes")
    rows = cursor.fetchall()
    conn.close()

    return [Scheme(*row) for row in rows]


def total_budget():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(budget) FROM projects")
    result = cursor.fetchone()[0]
    conn.close()

    return result or 0


def menu():
    print("\n=== CM Punjab Maryam Nawaz Govt System ===")
    print("1. Add Project")
    print("2. View Projects")
    print("3. Add Scheme")
    print("4. View Schemes")
    print("5. Total Budget")
    print("6. Exit")


def main():
    create_tables()

    while True:
        menu()
        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Project Name: ")
            dept = input("Department: ")
            budget = float(input("Budget: "))
            project = Project(name, dept, budget)
            add_project(project)
            print("Project added successfully!")

        elif choice == "2":
            projects = view_projects()
            print("\n--- Projects ---")
            for p in projects:
                print(p.display_info())

        elif choice == "3":
            name = input("Scheme Name: ")
            dept = input("Department: ")
            beneficiaries = int(input("Beneficiaries: "))
            scheme = Scheme(name, dept, beneficiaries)
            add_scheme(scheme)
            print("Scheme added successfully!")

        elif choice == "4":
            schemes = view_schemes()
            print("\n--- Schemes ---")
            for s in schemes:
                print(s.display_info())

        elif choice == "5":
            print("\nTotal Budget:", total_budget())

        elif choice == "6":
            print("Exiting system...")
            break

        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()