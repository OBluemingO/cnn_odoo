import pytz
import tensorflow as tf
import numpy as np
from datetime import datetime
from odoo import models, fields, api, _
from tensorflow import keras
from keras.models import load_model
from PIL import Image
from decimal import Decimal
import cv2
from odoo.exceptions import ValidationError
from .utils import *
from pathlib import Path


class LabTest(models.Model):
    _name = "ir.lab_test"

    request_id = fields.Many2one('ir.lab')

    lab_diagnosticresults = fields.Selection(
        selection=[
            ("normal", "Normal"),
            ("tuberculosis", "TUBERCULOSIS"),
        ],
        string="Diagnostic Result",
        readonly=True,
        store=True,
    )

    lab_diagnosticresults_Complications = fields.Selection(
        [
            ("Lung abscess", "ฝีในปอด"),
            ("pleural effusion", "ภาวะน้ำในช่องหุ้มปอด"),
        ],
        string="Complications Result",
    )

    lab_img = fields.Binary(
        string='Imagie',
        required=True
    )

    img_preview = fields.Binary(
        related='lab_img'
    )

    lab_probility = fields.Float(
        string='Probility',
        digits=(6, 2)
    )

    path_project = Path.cwd()
    path = Path(
        path_project / 'custom_addons/PJ_TB/static/model_h5/clasification_lr_model.h5')
    model = load_model(path)

    @api.depends('request_id.lab_type')
    def _compute_select_lab(self):
        pass

    @api.onchange('lab_img')
    def analysis_cnn_model(self):
        if self.lab_img:
            label = ['Normal', 'TB']
            file_name = decoding_img(self.lab_img)
            img = cv2.imread(file_name)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (180, 180))
            img_array = np.array(img).astype('float32')
            img_array = np.expand_dims(img_array, 0)
            images = np.vstack([img_array])
            predictions = self.model.predict(images)
            result = label[np.argmax(predictions)]
            percentage = max(predictions[0]*100)
            decimal_val = float(Decimal("%.2f" % percentage))

            if decimal_val > 80:
                if str(result) == 'TB':
                    self.lab_diagnosticresults = 'tuberculosis'
                    self.lab_probility = decimal_val
                else:
                    self.lab_diagnosticresults = 'normal'
                    self.lab_probility = decimal_val
            else:
                raise ValidationError(_('input image is invalid'))
        else:
            self.lab_probility = 0
            self.lab_diagnosticresults = ''
