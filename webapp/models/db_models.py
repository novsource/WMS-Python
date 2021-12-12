from webapp.main import db


class Item(db.Model):
    __tablename__ = 'Item'

    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String)

    item_manufacturer = db.relationship('ItemManufacturer', backref='item_manufacturer')

    def __init__(self, item_name):
        self.item_name = item_name

    def __repr__(self):
        return self

    def __str__(self):
        return [self.item_id, self.item_name]


class Manufacturer(db.Model):
    __tablename__ = 'Manufacturer'

    manufacturer_id = db.Column(db.Integer, primary_key=True)
    manufacturer_name = db.Column(db.String)

    def __init__(self, name):
        self.manufacturer_name = name

    def __repr__(self):
        return self

    def __str__(self):
        return [self.manufacturer_id, self.manufacturer_name]


class Storage(db.Model):
    __tablename__ = 'Storage'

    storage_id = db.Column(db.Integer, primary_key=True)
    storage_square = db.Column(db.Float)

    shop_storage = db.relationship('Shop', backref='shop')

    storage_item = db.relationship('ItemStorage', backref='item_storage')

    storage_arrived = db.relationship('ItemArrived', backref='item_arrived')

    def __init__(self, square):
        self.storage_square = square

    def __repr__(self):
        return self

    def __str__(self):
        return [self.storage_id, self.storage_square]


class Shop(db.Model):
    __tablename__ = 'Shop'

    shop_id = db.Column(db.Integer, primary_key=True)
    shop_address = db.Column(db.String)
    shop_square = db.Column(db.Float)

    storage_id = db.Column(db.Integer, db.ForeignKey('Storage.storage_id'))

    def __init__(self, address, square):
        self.shop_address = address
        self.shop_square = square

    def __repr__(self):
        return self

    def __str__(self):
        return [self.storage_id, self.shop_address, self.shop_square]


class ItemManufacturer(db.Model):
    __tablename__ = 'Item_Manufacturer'

    item_id = db.Column(db.Integer, db.ForeignKey('Item.item_id'))
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('Manufacturer.manufacturer_id'))
    item_cost = db.Column(db.Float)

    item_storage = db.relationship('ItemStorage', backref='item_storage')
    manufacturer_storage = db.relationship('ItemStorage', backref='item_storage')

    item_arrived = db.relationship('ItemArrived', backref='item_arrived')
    manufacturer_arrived = db.relationship('ItemArrived', backref='item_arrived')

    item_criteria = db.relationship('Criteria', backref='criteria')
    manufacturer_criteria = db.relationship('Criteria', backref='criteria')

    def __init__(self, item_id, manufacturer_id, cost):
        self.item_id = item_id
        self.manufacturer_id = manufacturer_id
        self.item_cost = cost

    def __repr__(self):
        return self

    def __str__(self):
        return [self.item_id, self.manufacturer_id, self.item_cost]


class ItemStorage(db.Model):
    __tablename__ = 'Item_Storage'

    item_storage_id = db.Column(db.Integer, primary_key=True)
    item_count = db.Column(db.Integer)

    item_id = db.Column(db.Integer, db.ForeignKey('ItemManufacturer.item_id'))
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('ItemManufacturer.manufacturer_id'))
    storage_id = db.Column(db.Integer, db.ForeignKey('Storage.storage_id'))

    def __init__(self, item_id, manufacturer_id, storage_id, item_count):
        self.item_id = item_id
        self.manufacturer_id = manufacturer_id
        self.storage_id = storage_id
        self.item_count = item_count

    def __repr__(self):
        return self

    def __str__(self):
        return [self.item_storage_id, self.item_id, self.manufacturer_id, self.storage_id, self.item_count]