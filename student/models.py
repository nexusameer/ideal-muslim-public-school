from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from . import *
from django.utils import timezone


# Create your models here.
def generate_student_roll_no():
    current_date = timezone.now()
    current_year = str(current_date.year)[-2:]
    base_serial_number = f"{current_year}"
    if Student.objects.filter(roll_no__startswith=base_serial_number).exists():
        serial_suffix = Student.objects.filter(roll_no__startswith=base_serial_number).count() + 1
    else:
        serial_suffix = 1
    roll_no = f"{base_serial_number}{str(serial_suffix).zfill(4)}"
    while Student.objects.filter(roll_no=roll_no).exists():
        serial_suffix += 1
        roll_no = f"{base_serial_number}{str(serial_suffix).zfill(4)}"
    return roll_no


def validate_cnic(value):
    if value:
        cleaned = value.replace('-', '')

        if not cleaned.isdigit() or len(cleaned) != 13:
            raise ValidationError("CNIC must have 13 Digits")

        if '-' not in value:
            value = f"{cleaned[:5]}-{cleaned[5:12]}-{cleaned[12]}"
    return value


def age_of_student(self):
    today = date.today()
    age = today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    return age


class Class(models.Model):
    name = models.CharField(max_length=50, unique=True)
    label = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    # student information
    roll_no = models.CharField(max_length=20, unique=True, blank=True, null=True, default=generate_student_roll_no)

    student_name = models.CharField(max_length=256)
    # gender = models.CharField(max_length=64, choices=GENDER_CHOICES)
    form_b_no = models.CharField(max_length=15, unique=True, verbose_name="Form B #", validators=[validate_cnic])
    date_of_birth = models.DateField()
    age_of_student = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    # student_section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)

    # student other infraction
    religion = models.CharField(max_length=256, null=True, blank=True, default='Islam')
    father_name = models.CharField(max_length=256)
    father_cnic = models.CharField(max_length=15, validators=[validate_cnic])
    father_guardian_occupation = models.CharField(max_length=15)
    # father_guardian_occupation = models.ForeignKey(Category, on_delete=models.PROTECT)
    mother_name = models.CharField(max_length=256)
    mother_cnic = models.CharField(max_length=15, validators=[validate_cnic], null=True, blank=True)
    parent_email_address = models.EmailField(null=True, blank=True)
    contact_number = models.CharField(max_length=256, null=True, blank=True)
    emergency_contact_number = models.CharField(max_length=256, null=True, blank=True)

    # enrollment
    # student_status = models.CharField(max_length=256, choices=STUDENT_STATUS_CHOICES)
    date_of_admission = models.DateField(default=timezone.now)
    # admission_type = models.CharField(max_length=64, choices=ADMISSION_TYPE_CHOICES, null=True, blank=True)
    # child_status = models.CharField(max_length=64, choices=CHILD_CHOICES)
    # student_fee_structure = models.ForeignKey(FeeStructure, on_delete=models.SET_NULL, null=True, blank=True)
    # fee_in_accounts = models.PositiveIntegerField(default=0)
    # advance = models.PositiveIntegerField(default=0)
    # arrears = models.PositiveIntegerField(default=0)
    # fine = models.PositiveIntegerField(default=0)
    # paid_admission_fee = models.PositiveIntegerField(default=0)
    # remaining_admission_fee = models.PositiveIntegerField(default=0)
    # paid_security = models.PositiveIntegerField(default=0)
    # remaining_security = models.PositiveIntegerField(default=0)
    # prospectus_fee = models.IntegerField(default=350)
    # total = models.IntegerField(default=0)

    # verification
    is_verified = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.student_name} ({self.form_b_no})"

    def save(self, *args, **kwargs):
        today = date.today()
        self.age_of_student = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        super().save(*args, **kwargs)

