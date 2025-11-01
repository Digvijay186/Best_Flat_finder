"""
django_signal_tests.py
Author: Digvijay Daspute
Description: Demonstrates Django signal behavior and custom class iteration.
"""

import time
import threading
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# ---------- Question 1: Are Django signals synchronous? ----------
@receiver(post_save, sender=User)
def slow_signal_handler(sender, instance, **kwargs):
    print("[Signal] Started processing...")
    time.sleep(3)
    print("[Signal] Finished processing.")

def test_synchronous_signal():
    print("\n=== Test 1: Synchronous Signal ===")
    print("Creating user...")
    User.objects.create(username="sync_test_user")
    print("User created successfully — after signal completed.\n")


# ---------- Question 2: Do signals run in the same thread? ----------
@receiver(post_save, sender=User)
def thread_check(sender, instance, **kwargs):
    print(f"[Signal] Thread ID: {threading.get_ident()}")

def test_thread_signal():
    print("\n=== Test 2: Thread Check ===")
    print(f"[Main] Thread ID: {threading.get_ident()}")
    User.objects.create(username="thread_test_user")
    print("Both thread IDs should match — same thread.\n")


# ---------- Question 3: Do signals share the same DB transaction? ----------
from django.db import models

# Dummy model for test
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    # Create profile inside signal
    Profile.objects.create(user=instance)
    print("[Signal] Profile created inside same transaction")

def test_transaction_signal():
    print("\n=== Test 3: Transaction Behavior ===")
    try:
        with transaction.atomic():
            user = User.objects.create(username="rollback_user")
            # Trigger rollback
            raise Exception("Force rollback after signal")
    except Exception as e:
        print("[Main] Exception caught:", e)

    print("Profiles in DB after rollback:", Profile.objects.count())
    print("If 0 → Signal ran in same transaction.\n")


# ---------- Custom Classes in Python ----------
class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}

def test_rectangle_iteration():
    print("\n=== Test 4: Custom Rectangle Class ===")
    rect = Rectangle(10, 5)
    for item in rect:
        print(item)
    print()


# ---------- Run All Tests ----------
def run_all_tests():
    test_synchronous_signal()
    test_thread_signal()
    test_transaction_signal()
    test_rectangle_iteration()


if __name__ == "__main__":
    print(">>> Django Signals and Python Custom Class Tests <<<")
    print("Run these functions individually inside Django shell:\n")
    print("    from yourapp.django_signal_tests import run_all_tests")
    print("    run_all_tests()\n")
