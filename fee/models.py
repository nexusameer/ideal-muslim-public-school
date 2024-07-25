from django.db import models
from student.models import *


# Create your models here.

class StudentFeeVoucher(models.Model):
    voucher_number = models.CharField(max_length=10)
    student = models.ForeignKey(Student, on_delete=models.CASCADE())
    time_generated = models.DateTimeField(auto_now_add=True)
    # dev_fund = models.PositiveIntegerField(default=0)
    # misc_fee = models.PositiveIntegerField(default=0)
    admission_fee = models.PositiveIntegerField(default=0)
    prospectus_fee = models.PositiveIntegerField(default=0)
    arrears = models.PositiveIntegerField(default=0)
    advance = models.PositiveIntegerField(default=0)
    due_date = models.DateField(default=get_due_date)
    late_payment_fine = models.PositiveIntegerField(default=300)
    extra_charges = models.PositiveIntegerField(default=0)
    extra_charges_note = models.CharField(max_length=64, blank=True, null=True)
    total_fee = models.IntegerField(blank=True, null=True)
    total_fee_after_due_date = models.IntegerField(blank=True, null=True)
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.PROTECT)
    arrears_tuition_fee = models.PositiveIntegerField(default=0)
    arrears_development_fund = models.PositiveIntegerField(default=0)
    arrears_misc = models.PositiveIntegerField(default=0)
    arrears_fine = models.PositiveIntegerField(default=0)
    arrears_others = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    partial_paid = models.BooleanField(default=False)
    amount_paid = models.PositiveIntegerField(default=0)
    date_paid = models.DateField(blank=True, null=True)

    is_security_voucher = models.BooleanField(default=False)
    is_admission_voucher = models.BooleanField(default=False)
    admission = models.ForeignKey(Admission, null=True, blank=True, on_delete=models.PROTECT)
    form_b_no = models.CharField(max_length=15, null=True, blank=True)
