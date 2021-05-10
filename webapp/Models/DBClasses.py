from webapp.main import db


class Items(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(50), nullable=False)
    item_cost = db.Column(db.Integer, nullable=False)

    def __init__(self, name, cost):
        self.item_name = name
        self.item_cost = cost


class Manufacturer(db.Model):
    manufacturer_id = db.Column(db.Integer, primary_key=True)
    manufacturer_name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        self.manufacturer_name = name

