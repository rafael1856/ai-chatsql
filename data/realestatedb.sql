/* Uncomment the next section if you are creating the 
   database and schema from the commandline. */

/*
CREATE DATABASE realestate
  WITH
    OWNER = postgres;

CREATE SCHEMA listings
  AUTHORIZATION postgres; 
*/

/* Based on schema https://schema.org/Person */
CREATE TABLE listings.person(  pid SERIAL             PRIMARY KEY,
                              name CHARACTER VARYING,
                         givenname CHARACTER VARYING,
                        familyname CHARACTER VARYING,
                    additionalname CHARACTER VARYING,
                             email CHARACTER VARYING);

/* Based on schema https://schema.org/House and https://schema.org/Accommodation*/
CREATE TABLE listings.property(propid SERIAL             PRIMARY KEY,
                        streetaddress CHARACTER VARYING,
                      addresslocality CHARACTER VARYING,
                           postalcode CHARACTER VARYING,
                            floorsize NUMERIC,
                       floorsizeunits CHARACTER VARYING DEFAULT 'm^2',
                        numberofrooms NUMERIC);

/* Based on https://schema.org/Organization */
CREATE TABLE listings.agency(agcyid SERIAL            PRIMARY KEY,
                             agency CHARACTER VARYING,
                            address CHARACTER VARYING,
                         areaserved CHARACTER VARYING,
                       contactpoint CHARACTER VARYING);

/* Relates a person to a real estate agency */
CREATE TABLE listings.agent(agtid SERIAL  PRIMARY KEY,
                              pid INTEGER REFERENCES listings.person,
                           agcyid INTEGER REFERENCES listings.agency);

CREATE TABLE listings.listing(listid SERIAL PRIMARY KEY,
                               agent INTEGER           REFERENCES listings.person,
                                 pid INTEGER           REFERENCES listings.person,
                              propid INTEGER           REFERENCES listings.property,
                         listingdate DATE,
                        listingprice NUMERIC,
                                 url CHARACTER VARYING,
                                open BOOLEAN           DEFAULT true);

/* From https://schema.org/Offer */
CREATE TABLE listings.offer(offerid SERIAL PRIMARY KEY,
                              agent INTEGER           REFERENCES listings.person,
                                pid INTEGER           REFERENCES listings.person,
                             listid INTEGER           REFERENCES listings.listing,
                          validfrom DATE,
                    pricevaliduntil DATE,
                              price NUMERIC CONSTRAINT get_positive_price CHECK (price > 0),
                      pricecurrency CHARACTER VARYING DEFAULT 'CAD',
                              notes TEXT,
                           accepted BOOLEAN           DEFAULT false);
