from django import forms
from django.contrib.auth.models import User
from .models import Product, Transaction

# Formulir Registrasi
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Konfirmasi Password")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password dan konfirmasi password tidak cocok.")


# Formulir Login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


# Formulir untuk Produk
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image']


# Formulir untuk Pembayaran dan Bukti Pembayaran
class PaymentForm(forms.Form):
    PAYMENT_METHOD_CHOICES = [
        ('bank', 'Bank Transfer'),
        ('digital_wallet', 'Dompet Digital'),
    ]
    BANK_CHOICES = [
        ('bca', 'ATM BCA'),
        ('bri', 'ATM BRI'),
        ('mandiri', 'ATM Mandiri'),
        ('bni', 'ATM BNI'),
    ]
    EWALLET_CHOICES = [
        ('dana', 'Dana'),
        ('gopay', 'Gopay'),
        ('ovo', 'OVO'),
        ('linkaja', 'LinkAja'),
    ]

    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, widget=forms.RadioSelect, label="Metode Pembayaran")
    bank_choice = forms.ChoiceField(choices=BANK_CHOICES, required=False, label="Pilih Bank")
    ewallet_choice = forms.ChoiceField(choices=EWALLET_CHOICES, required=False, label="Pilih Dompet Digital")
    payment_proof = forms.ImageField(required=True, label="Bukti Pembayaran", widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}))

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')

        # Validasi pemilihan bank atau e-wallet sesuai dengan metode pembayaran yang dipilih
        if payment_method == 'bank':
            if not cleaned_data.get('bank_choice'):
                raise forms.ValidationError("Anda harus memilih bank untuk metode pembayaran Bank Transfer.")
        elif payment_method == 'digital_wallet':
            if not cleaned_data.get('ewallet_choice'):
                raise forms.ValidationError("Anda harus memilih dompet digital untuk metode pembayaran Dompet Digital.")
        
        return cleaned_data
