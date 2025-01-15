from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CartItem, Product, Transaction
from django.http import Http404
from .forms import PaymentForm


# Login
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username atau password salah.')

    return render(request, 'registration/login.html')


# Register
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Username sudah digunakan.')
        else:
            messages.error(request, 'Password dan konfirmasi password tidak cocok.')

    return render(request, 'registration/register.html')


# Logout
def logout_user(request):
    auth_logout(request)
    return redirect('login')


# Home Page
@login_required
def home(request):
    products = Product.objects.all()
    return render(request, 'tampilan/home.html', {'products': products})


# Add Product to Cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Cek apakah stok cukup
    if product.stock <= 0:
        return redirect('out_of_stock')  # Atau tampilkan pesan stok habis

    # Menambahkan produk ke keranjang atau mengupdate jumlahnya
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}  # Set default quantity for new items
    )
    if not created:  # Jika item sudah ada, tambahkan quantity
        cart_item.quantity += 1
        cart_item.save()

    # Mengurangi stok produk saat ditambahkan ke keranjang
    product.stock -= 1
    product.save()

    return redirect('cart_detail')


# View Cart@login_required
@login_required
def cart_detail(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("quantity_"):
                item_id = key.split("_")[1]  # Ambil ID item dari name input
                new_quantity = int(value)    # Ambil jumlah baru
                cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
                cart_item.quantity = new_quantity
                cart_item.save()
        return redirect('cart_detail')  # Reload halaman keranjang
    
    cart_items = CartItem.objects.filter(user=request.user)  # Data keranjang
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    # Buat transaksi di database (jika ada)
    transaction = None
    if cart_items:
        transaction = Transaction.objects.create(
            user=request.user,
            total_amount=total_price,
            status='pending'
        )

    return render(request, 'keranjang/cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'transaction': transaction,  # Kirim ke template
    })





# Checkout
@login_required
def checkout(request, product_id):
    if request.method == 'POST':
        if product_id:
            product = get_object_or_404(Product, id=product_id)

            # Validasi stok produk
            if product.stock <= 0:
                messages.error(request, 'Produk ini sudah habis.')
                return redirect('home')

            # Proses pembelian langsung untuk satu produk
            total_price = product.price
            quantity = int(request.POST.get('quantity', 1))

            # Mengurangi stok produk
            product.stock -= quantity
            product.save()

            # Buat transaksi baru dengan status 'pending'
            transaction = Transaction.objects.create(
                user=request.user,
                total_amount=total_price * quantity,
                status='pending'
            )

            # Redirect ke halaman pembayaran
            return redirect('payment_page', transaction_id=transaction.id)

        # Jika checkout dari keranjang
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items:
            raise Http404("Keranjang tidak ditemukan")

        # Menghitung total harga
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Membuat transaksi baru dengan status 'pending'
        transaction = Transaction.objects.create(user=request.user, total_amount=total_price, status='pending')

        # Redirect ke halaman pembayaran
        return redirect('payment_page', transaction_id=transaction.id)

    return render(request, 'checkout/checkout.html')


# Payment Page
 # Import form baru yang akan Anda buat

# Payment Page

@login_required
def payment_page(request, transaction_id):
    print(f"Attempting to access transaction with ID: {transaction_id}")
    # Cek apakah transaksi dengan ID tersebut milik pengguna yang sedang login
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user, status='pending')

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')  # Ambil metode pembayaran
        # Simulasi pembayaran
        payment_successful = process_payment(transaction.total_amount)

        if payment_successful:
            transaction.status = 'completed'
            transaction.payment_method = payment_method
            transaction.save()

            # Kosongkan keranjang setelah transaksi berhasil
            CartItem.objects.filter(user=request.user).delete()
            messages.success(request, 'Pembayaran berhasil! Terima kasih atas pembelian Anda.')
            return redirect('checkout_success')
        else:
            messages.error(request, 'Pembayaran gagal. Silakan coba lagi.')

    return render(request, 'checkout/payment_page.html', {'transaction': transaction})





# Checkout Success
@login_required
def checkout_success(request):
    return render(request, 'checkout/checkout_success.html')


# Menampilkan daftar produk
def product_list(request):
    products = Product.objects.all()  # Ambil semua produk yang ada
    return render(request, 'keranjang/product_list.html', {'products': products})


# Fungsi untuk memproses pembayaran (simulasi atau koneksi ke API)
def process_payment(amount):
    # Simulasi pembayaran, Anda dapat menggantinya dengan gateway pembayaran nyata
    return True
