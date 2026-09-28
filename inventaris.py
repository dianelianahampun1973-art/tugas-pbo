"""
Pemrograman Berorientasi Objek - Pertemuan 05
Property Visibility & Enkapsulasi di Python 3.12

Bagian 1 (Live Code)  : class Product & Account
Bagian 2 (Tugas Mandiri): class Company (+ class Employee)
"""


# =====================================================================
# BAGIAN 1 - LIVE CODE: Product & Account
# =====================================================================
class Product:
    """Aturan 2: harga (__price) dilindungi dan diakses via @property."""

    def __init__(self, name, price, stock=0):
        self.name = name
        self.price = price          # memicu setter (validasi)
        self.stock = stock

    @property
    def price(self):                # pengganti getter
        return self.__price

    @price.setter
    def price(self, value):         # pengganti setter
        if value < 0:
            raise ValueError("Harga tidak boleh negatif!")
        self.__price = value

    def __str__(self):
        return f"{self.name} | Rp{self.price:,.0f} | stok: {self.stock}"


class Account:
    """Aturan 1: saldo (__balance) private dan tidak boleh negatif."""

    def __init__(self, balance=0):
        self.balance = balance      # memicu setter (validasi)

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, amount):
        if amount < 0:
            raise ValueError("Saldo tidak boleh negatif!")
        self.__balance = amount

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Jumlah deposit harus lebih dari 0!")
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError("Saldo tidak cukup!")
        self.balance -= amount

    def purchase_product(self, product, quantity=1):
        """Aturan 3: validasi kecukupan __balance SEBELUM memodifikasi data."""
        if not isinstance(product, Product):
            raise TypeError("Input harus object Product!")
        total = product.price * quantity
        if total > self.__balance:
            raise ValueError(
                f"Saldo tidak cukup! Butuh Rp{total:,.0f}, "
                f"saldo Rp{self.__balance:,.0f}"
            )
        self.balance -= total       # baru diubah setelah lolos validasi
        return total


# =====================================================================
# BAGIAN 2 - TUGAS MANDIRI: Employee & Company
# =====================================================================
class Employee:
    def __init__(self, name, position, salary):
        self.name = name
        self.position = position
        self.salary = salary

    def __str__(self):
        return f"{self.name} | {self.position} | Rp{self.salary:,.0f}"


class Company:
    def __init__(self, name, capital=0):
        self.name = name
        self.__employees = []           # WAJIB: array data karyawan (private)
        self.__inventory = []           # daftar produk (dari Live Code)
        self.__account = Account(capital)  # kas perusahaan

    # ---------- Karyawan ----------
    def add_employee(self, employee):
        """Validasi tipe dengan isinstance() sebelum masuk ke list."""
        if not isinstance(employee, Employee):
            raise TypeError(
                f"Input harus object Employee, bukan {type(employee).__name__}"
            )
        self.__employees.append(employee)

    def get_employees(self):
        return list(self.__employees)   # salinan, data asli aman

    # ---------- Inventaris ----------
    def restock_product(self, product, quantity):
        """Beli produk memakai kas perusahaan lalu tambah ke inventaris."""
        cost = self.__account.purchase_product(product, quantity)  # validasi di Account
        product.stock += quantity
        if product not in self.__inventory:
            self.__inventory.append(product)
        return cost

    def get_inventory(self):
        return list(self.__inventory)

    # ---------- Payroll ----------
    def get_total_payroll(self):
        """Pintu publik untuk method private."""
        return self.__calculate_payroll()

    def pay_payroll(self):
        """Bayar gaji dari kas perusahaan."""
        total = self.__calculate_payroll()
        self.__account.withdraw(total)  # error jika kas tidak cukup
        return total

    def __calculate_payroll(self):
        """WAJIB: private method, hanya bisa dipanggil dari dalam class."""
        return sum(emp.salary for emp in self.__employees)

    @property
    def cash(self):
        return self.__account.balance


# =====================================================================
# PENGUJIAN
# =====================================================================
if __name__ == "__main__":
    print("=== BAGIAN 1: Live Code ===")
    akun = Account(100)
    try:
        akun.balance = -50
    except ValueError as e:
        print("Setter memblokir:", e)

    p = Product("Laptop", 8_000_000)
    try:
        p.price = -1
    except ValueError as e:
        print("Setter harga memblokir:", e)

    print("\n=== BAGIAN 2: Company ===")
    c = Company("PT Maju Jaya", capital=50_000_000)

    c.add_employee(Employee("Budi", "Staff IT", 5_000_000))
    c.add_employee(Employee("Sari", "Akuntan", 6_000_000))
    for e in c.get_employees():
        print(" -", e)
    print("Total payroll :", f"Rp{c.get_total_payroll():,.0f}")

    # Uji isinstance
    try:
        c.add_employee("bukan employee")
    except TypeError as e:
        print("isinstance memblokir:", e)

    # Uji inventaris + saldo
    laptop = Product("Laptop", 8_000_000)
    c.restock_product(laptop, 3)
    print("Kas setelah beli laptop:", f"Rp{c.cash:,.0f}")
    print("Stok:", laptop)

    try:
        c.restock_product(Product("Server", 100_000_000), 1)
    except ValueError as e:
        print("Pembelian ditolak:", e)

    c.pay_payroll()
    print("Kas setelah gajian    :", f"Rp{c.cash:,.0f}")

    # Uji enkapsulasi
    for attr in ("__employees", "__calculate_payroll"):
        try:
            getattr(c, attr)
        except AttributeError:
            print(f"Akses c.{attr} dari luar -> AttributeError")

    # Bukti name mangling (bukan keamanan sejati!)
    print("Via mangling :", len(c._Company__employees), "karyawan (bisa ditembus)")
