/* Adding in a few random names. */
INSERT INTO listings.person(name, givenname, familyname, email)
  VALUES('Tang Yao Zu',      'Yao Zu',    'Tang',      'yzt@coolemail.com'),
        ('Bandar Ramzi Ba',  'Bandar',    'Ba',        'thisemail@thatemail.com'),
        ('Reggie Schoen',    'Reggie',    'Schoen',    'schoen@mytown.ca'),
        ('Una Suzuki',       'Una',       'Suzuki',    NULL),
        ('Kimberley Cada',   'Kimberly',  'Cada',      'kcada@thisemail.com'),
        ('Kasha Sollers',    'Kasha',     'Sollers',   'ksollers@heresmyemail.ca'),
        ('Francesco Abrev',  'Francesco', 'Abrev',     'lovetosql@databaseguy.eu'),
        ('Marhta Niswander', 'Marhta',    'Niswander', 'niswander@onlymarhtas.co.uk');

INSERT INTO listings.property(streetaddress, addresslocality, postalcode,
                              floorsize, floorsizeunits, numberofrooms)
  VALUES('350 2033 TRIUMPH STREET',  'Vancouver', 'V5L4X3', 44.5, 'm^2', 3),
        ('1007 1003 PACIFIC STREET', 'Vancouver', 'V2N1E2', 35, 'm^2', 1),
        ('809 13380 108 AVENUE',     'Surrey', 'V3T0E7', 44.5, 'm^2', 4),
        ('642 SOUTHBOROUGH DRIVE', 'West Vancouver', 'V7S1M6', 1340, 'm^2', 4);

INSERT INTO listings.agency(agency, address, areaserved, contactpoint)
  VALUES('West Vancouver Super Agents', '115 COOLSTREET DRIVE', 'West Vancouver', 'info@wvsa.ca'),
        ('Vancouver Really Real Estate', '3134 SOUTH CRUMMY STREET', 'Vancouver', 'info@sillyagency.ca'),
        ('Surry Apartment Hunters', '22-313 HORSEGIVENS CR', 'Surry', 'surry@apthunt.rl');

  /* Relates a person to a real estate agency */
INSERT INTO listings.agent(pid, agcyid)
  VALUES((SELECT pid    FROM listings.person AS pr WHERE pr.email LIKE 'yzt@coolemail.com'),
         (SELECT agcyid FROM listings.agency AS agcy WHERE agcy.agency LIKE 'West Vancouver Super Agents')),
        ((SELECT pid    FROM listings.person AS pr WHERE pr.email LIKE 'niswander@onlymarhtas.co.uk'),
         (SELECT agcyid FROM listings.agency AS agcy WHERE agcy.agency LIKE 'Vancouver Really Real Estate')),
        ((SELECT pid    FROM listings.person AS pr WHERE pr.email LIKE 'lovetosql@databaseguy.eu'),
         (SELECT agcyid FROM listings.agency AS agcy WHERE agcy.agency LIKE 'Surry Apartment Hunters'));

INSERT INTO listings.listing(agent, pid, propid, listingdate, listingprice, url, open)
VALUES((SELECT pid    FROM listings.person   AS pr WHERE pr.email LIKE 'yzt@coolemail.com'),
       (SELECT pid    FROM listings.person   AS pr WHERE pr.email LIKE 'schoen@mytown.ca'),
       (SELECT propid FROM listings.property AS pp WHERE pp.streetaddress LIKE '642 SOUTHBOROUGH DRIVE'),
       '2018-09-10', 3243323, NULL, True),
      ((SELECT pid    FROM listings.person   AS pr WHERE pr.email LIKE 'niswander@onlymarhtas.co.uk'),
       (SELECT pid    FROM listings.person   AS pr WHERE pr.email LIKE 'ksollers@heresmyemail.ca'),
       (SELECT propid FROM listings.property AS pp WHERE pp.streetaddress LIKE '1007 1003 PACIFIC STREET'),
       '2018-09-09', 1435214, NULL, True);

INSERT INTO listings.offer(agent, pid, listid,
                           validfrom,
                           pricevaliduntil,
                           price, notes)
  VALUES((SELECT pid    FROM listings.person AS pr WHERE pr.email LIKE 'lovetosql@databaseguy.eu'),
         (SELECT pid    FROM listings.person AS pr WHERE pr.email LIKE 'ksollers@heresmyemail.ca'),
         (SELECT listid FROM listings.listing AS ls
            WHERE ls.agent = (SELECT pid FROM listings.person AS pr WHERE pr.email LIKE 'yzt@coolemail.com')
            AND ls.pid = (SELECT pid FROM listings.person AS pr WHERE pr.email LIKE 'schoen@mytown.ca')),
         '2018-09-09', '2018-09-16',
         3000000,
         'Have requested that the owners fix the hole in the roof.'),
         ((SELECT pid    FROM listings.person AS pr WHERE pr.email LIKE 'yzt@coolemail.com'),
          (SELECT pid    FROM listings.person AS pr WHERE pr.email LIKE 'kcada@thisemail.com'),
          (SELECT listid FROM listings.listing AS ls
            WHERE ls.agent = (SELECT pid FROM listings.person AS pr WHERE pr.email LIKE 'yzt@coolemail.com')
            AND ls.pid = (SELECT pid FROM listings.person AS pr WHERE pr.email LIKE 'schoen@mytown.ca')),
          '2018-09-09', '2018-09-16',
          3100000, 'Have requested that the owners close the skylight.'),
         ((SELECT pid    FROM listings.person AS pr WHERE pr.email LIKE 'lovetosql@databaseguy.eu'),
          (SELECT pid    FROM listings.person AS pr WHERE pr.email LIKE 'thisemail@thatemail.com'),
          (SELECT listid FROM listings.listing AS ls
            WHERE ls.agent = (SELECT pid FROM listings.person AS pr WHERE pr.email LIKE 'niswander@onlymarhtas.co.uk')
            AND ls.pid = (SELECT pid FROM listings.person AS pr WHERE pr.email LIKE 'ksollers@heresmyemail.ca')),
          '2018-09-09', '2018-09-16',
          1300000, 'The buyers have requested that the apartment be bigger.');
