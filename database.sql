CREATE TABLE food (
    id SERIAL,
    name TEXT NOT NULL,
    protein INTEGER NOT NULL,
    carbohydrates INTEGER NOT NULL,
    fat INTEGER NOT NULL,
    calories INTEGER NOT NULL
);

CREATE TABLE food_date (
    food_id SERIAL,
    log_date_id INTEGER NOT NULL,
    PRIMARY KEY(food_id, log_date_id)
);

CREATE TABLE log_date (
    id SERIAL,
    entry_date DATE NOT NULL
);