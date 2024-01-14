
DROP TABLE IF EXISTS properties;
CREATE TABLE properties (
    id serial NOT NULL PRIMARY KEY,
    title varchar(200) NOT NULL,
    img_url varchar(400) NOT NULL
);

    