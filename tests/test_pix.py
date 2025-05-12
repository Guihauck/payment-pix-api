import sys
sys.path.append("../")
import pytest
import os
from payment.pix import Pix

def test_create_payment():
    pix_instance = Pix()
    informations_pix = pix_instance.create_payment(base_dir="../")
    assert "bank_payment_id" in informations_pix
    assert "qr_code_path" in informations_pix
    qr_code_path = informations_pix["qr_code_path"]
    assert os.path.isfile(f"../static/img/{qr_code_path}.png")

