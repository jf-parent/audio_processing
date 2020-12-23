#! /usr/bin/env python

from cookiecutter.main import cookiecutter
from faker import Faker

fake = Faker()
hrn = "the_{name}_effect".format(name=fake.name().lower().replace(' ', '_'))

cookiecutter(
    './template',
    extra_context={'hrn': hrn},
)
