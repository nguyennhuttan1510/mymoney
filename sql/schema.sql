INSERT INTO category_category (id, name, type, icon, is_default)
VALUES
    (1, 'Giải trí', 'EXPENSE', null, True),
    (2, 'Ăn uống', 'EXPENSE', null, True),
    (3, 'Cà phê', 'EXPENSE', null, True),
    (4, 'Du lịch', 'EXPENSE', null, True),
    (5, 'Đầu tư', 'EXPENSE', null, True),
    (6, 'Quà tặng', 'EXPENSE', null, True),
    (7, 'Ăn ngoài', 'EXPENSE', null, True),
    (8, 'Hóa đơn', 'EXPENSE', null, True),
    (9, 'Mua sắm', 'EXPENSE', null, True),
    (10, 'Điện', 'EXPENSE', null, True),
    (11, 'Nước', 'EXPENSE', null, True),
    (12, 'Internet', 'EXPENSE', null, True),
    (13, 'Điện thoại', 'EXPENSE', null, True),
    (14, 'Xăng', 'EXPENSE', null, True),
    (15, 'Lương', 'INCOME', null, True);


UPDATE category_category SET name = 'Giải trí' WHERE id = 1;
UPDATE category_category SET name = 'Ăn uống' WHERE id = 2;
UPDATE category_category SET name = 'Cà phê' WHERE id = 3;
UPDATE category_category SET name = 'Du lịch' WHERE id = 4;
UPDATE category_category SET name = 'Đầu tư' WHERE id = 5;
UPDATE category_category SET name = 'Quà tặng' WHERE id = 6;
UPDATE category_category SET name = 'Ăn ngoài' WHERE id = 7;
UPDATE category_category SET name = 'Hóa đơn' WHERE id = 8;
UPDATE category_category SET name = 'Mua sắm' WHERE id = 9;
UPDATE category_category SET name = 'Điện' WHERE id = 10;
UPDATE category_category SET name = 'Nước' WHERE id = 11;
UPDATE category_category SET name = 'Internet' WHERE id = 12;
UPDATE category_category SET name = 'Điện thoại' WHERE id = 13;
UPDATE category_category SET name = 'Xăng' WHERE id = 14;
UPDATE category_category SET name = 'Lương' WHERE id = 15;
