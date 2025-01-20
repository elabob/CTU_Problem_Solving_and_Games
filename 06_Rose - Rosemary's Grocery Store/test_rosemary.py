from rosemary import Item, update

# Aged Brie Tests
def test_aged_brie_increases_quality():
    item = Item('Aged Brie', days_left=5, quality=10)
    update(item)
    return item.quality == 11

def test_aged_brie_quality_max_50():
    item = Item('Aged Brie', days_left=5, quality=50)
    update(item)
    return item.quality == 50

def test_aged_brie_increases_quality_after_expiry():
    item = Item('Aged Brie', days_left=0, quality=10)
    update(item)
    return item.quality == 11

def test_aged_brie_quality_does_not_exceed_50():
    item = Item('Aged Brie', days_left=5, quality=49)
    update(item)
    return item.quality == 50  # Quality shouldn't exceed 50

def test_aged_brie_quality_does_not_exceed_50_quality_2():
    item = Item('Aged Brie', days_left=0, quality=49)
    update(item)
    return item.quality == 50  # Quality +2, but stops at 50

# Diamond Tests
def test_diamond_quality_constant():
    item = Item('Diamond', days_left=100, quality=100)
    update(item)
    return item.quality == 100

def test_diamond_days_left_constant():
    item = Item ('Diamond', days_left = 100, quality = 100)
    update (item)
    return item.days_left == 100

# Normal Item Tests
def test_normal_item_quality_never_negative():
    item = Item('Bread', days_left=1, quality=1)
    update(item)
    return item.quality == 0

def test_normal_item_quality_never_negative_0days() :
    item = Item('Bread', days_left=0, quality=1)
    update(item)
    return item.quality == 0

def test_normal_item_decreases_days_left():
    item = Item('Bread', days_left=3, quality=5)
    update(item)
    return item.days_left == 2

def test_normal_item_decreases_quality():
    item = Item('Bread', days_left=3, quality=5)
    update(item)
    return item.quality == 4

def test_normal_item_quality_drops_twice_as_fast_after_expiry():
    item = Item('Bread', days_left=0, quality=5)
    update(item)
    return item.quality == 3

def test_normal_item_quality_never_negative_general():
    item = Item('Bread', days_left=3, quality=0)
    update(item)
    return item.quality == 0

# Tickets Tests
def test_tickets_quality_for_50_days_left():
    item = Item('Tickets', days_left=50, quality=20)
    update(item)
    return item.quality == 21

def test_tickets_increase_quality_by_2_from_10_to_6_days():
    for days in range(6, 11):
        item = Item('Tickets', days_left=days, quality=20)
        update(item)
        assert item.quality == 22

def test_tickets_increase_quality_by_3_from_5_to_1_days():
    for days in range(1, 6):
        item = Item('Tickets', days_left=days, quality=20)
        update(item)
        assert item.quality == 23

def test_tickets_quality_after_event() :
    for days in range (-5, 0):
        item = Item ('Tickets', days_left = days, quality = 50)
        update (item)
        assert item.quality == 0

def test_tickets_quality_for_51_days_left():
    item = Item('Tickets', days_left=51, quality=21)
    update(item)
    return item.quality == 22

def test_tickets_quality_for_49_days_left():
    item = Item('Tickets', days_left=49, quality=48)
    update(item)
    return item.quality == 49

def test_tickets_quality_for_10_days_left():
    item = Item('Tickets', days_left=10, quality=20)
    update(item)
    return item.quality == 22

def test_tickets_quality_for_5_days_left():
    item = Item('Tickets', days_left=5, quality=48)
    update(item)
    return item.quality == 50

def test_tickets_quality_for_5_days_left_quality_3():
    item = Item('Tickets', days_left=5, quality=10)
    update(item)
    return item.quality == 13

def test_tickets_quality_for_3_days_left():
    item = Item('Tickets', days_left=3, quality=49)
    update(item)
    return item.quality == 50

def test_tickets_quality_for_1_day_left():
    item = Item('Tickets', days_left=1, quality=50)
    update(item)
    return item.quality == 50

def test_tickets_quality_for_0_days_left():
    item = Item('Tickets', days_left=0, quality=50)
    update(item)
    return item.quality == 0
