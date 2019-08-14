CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE shopping_cart(
    user_id uuid default uuid_generate_v4() primary key
);

CREATE TABLE item(
    name varchar(50) primary key,
    cost decimal not null
);

CREATE TABLE shopping_cart_item(
    user_id uuid,
    item_name varchar(50),
    quantity int not null,
    primary key(user_id, item_name),
    foreign key (user_id) references shopping_cart(user_id),
    foreign key (item_name) references item(name) 
);

insert into item values ('socks', 50.05),
    ('apple', 1),
    ('shirt', 15.99),
    ('thing', 10);