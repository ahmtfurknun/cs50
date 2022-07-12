-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT * FROM crime_scene_reports WHERE month = 7 AND day = 28 AND street = "Chamberlin Street"; -- 10.15 am
SELECT * FROM interviews WHERE month = 7 AND day = 28; -- atm, withdraw, Fifer Street, less than a minute
SELECT license_plate FROM courthouse_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND 25 >= minute AND minute >= 15; -- 5P2BI95 94KL13X 6P58WS2 G412CB7 L93JTIZ 322W7JE 0NTHK55
SELECT account_number FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw";


SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60;

SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw");

SELECT passport_number FROM passengers WHERE flight_id IN
(SELECT id FROM flights WHERE origin_airport_id IN
(SELECT id FROM airports WHERE city = "Fiftyville") AND month = 7 AND day = 29 ORDER BY hour LIMIT 1);



SELECT name, id FROM people WHERE phone_number IN
(SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60) AND license_plate IN
(SELECT license_plate FROM courthouse_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND 25 >= minute AND minute >= 15) AND id IN
(SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw"))
AND passport_number IN
(SELECT passport_number FROM passengers WHERE flight_id IN
(SELECT id FROM flights WHERE origin_airport_id IN
(SELECT id FROM airports WHERE city = "Fiftyville") AND month = 7 AND day = 29 ORDER BY hour LIMIT 1)); -- Thief is Ernest 686048

SELECT * FROM people WHERE id = 686048; --Ernest

SELECT receiver FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60 AND caller =
(SELECT phone_number FROM people WHERE id = 686048); -- Phone number of person who helped.

SELECT name FROM people WHERE phone_number =
(SELECT receiver FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60 AND caller =
(SELECT phone_number FROM people WHERE id = 686048)); -- Name of the person who helped.


SELECT city FROM airports WHERE id =
(SELECT destination_airport_id FROM flights WHERE origin_airport_id IN
(SELECT id FROM airports WHERE city = "Fiftyville") AND month = 7 AND day = 29 ORDER BY hour LIMIT 1); -- Where he escaped