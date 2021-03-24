# -*- coding: utf-8 -*-
"""Define the quadraticlands views.

Copyright (C) 2020 Gitcoin Core

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

"""

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _

class QuadLandsFAQ(models.Model):
    '''Table for storing quadlands FAQ items'''
    position = models.IntegerField(blank=False, unique=True)
    created_on = models.DateTimeField(auto_now=True)
    question = models.TextField(default='', blank=True)
    answer = models.TextField(default='', blank=True)
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.question}'


class Uint256Field(models.DecimalField):
    description = _("Ethereum uint256 number")
    '''
    Field to store ethereum uint256 values. Uses Decimal db type without decimals to store
    in the database, but retrieve as `int` instead of `Decimal` (https://docs.python.org/3/library/decimal.html)
    https://github.com/gnosis/gnosis-py/blob/master/gnosis/eth/django/models.py
    '''
    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = 79  # 2 ** 256 is 78 digits
        kwargs['decimal_places'] = 0
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_digits']
        del kwargs['decimal_places']
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return int(value)

class InitialTokenDistribution(models.Model):
    '''Table for storing the initial gitcoin retroactive token distribution details'''
    profile = models.ForeignKey(
        'dashboard.Profile', related_name='initial_distribution', on_delete=models.CASCADE
    ) 
    created_on = models.DateTimeField(auto_now=True)
    claim_total = Uint256Field(default=0)
    distribution = JSONField(default=dict)
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.profile.handle}, {self.claim_total}, , {self.created_on}, {self.distribution}'

class MissionStatus(models.Model):
    ''' Track which missions a given user has completed'''
    profile = models.ForeignKey(
        'dashboard.Profile', related_name='mission_status', on_delete=models.CASCADE
    )
    proof_of_use = models.BooleanField(default=False)
    proof_of_receive = models.BooleanField(default=False)
    proof_of_knowledge = models.BooleanField(default=False)
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.profile.handle}, {self.proof_of_use}, {self.proof_of_receive}, {self.proof_of_knowledge}'
