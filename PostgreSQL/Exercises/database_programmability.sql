create function fn_full_name(first_name varchar, last_name varchar)
    returns varchar as
$$
declare
    full_name varchar;
begin
    select initcap(concat(first_name, ' ', last_name))
    into full_name;
    return full_name;

end;
$$
    LANGUAGE plpgsql;


create or replace function fn_calculate_future_value(initial_sum numeric, yearly_interest_rate numeric,
                                                     number_of_years numeric)
    returns varchar as
$$
declare
    roi numeric;
begin
    select initial_sum * ((1 + yearly_interest_rate) ^ number_of_years)
    into roi;
    return trunc(roi, 4);
end;
$$
    LANGUAGE plpgsql;


create or replace function fn_is_word_comprised(set varchar(50), word varchar(50))
    returns boolean
as
$$
begin
    return trim(lower(word), lower(set)) = '';
end;
$$
    language plpgsql;


CREATE OR REPLACE FUNCTION fn_is_game_over(
    is_game_over BOOLEAN
)
    RETURNS TABLE
            (
                name         VARCHAR(50),
                game_type_id INT,
                is_finished  BOOLEAN
            )
AS
$$
BEGIN
    RETURN QUERY
        SELECT g.name,
               g.game_type_id,
               g.is_finished
        FROM games AS "g"
        WHERE g.is_finished = is_game_over;
END;
$$
    LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION fn_difficulty_level(
    level INT
)
    RETURNS VARCHAR
AS
$$
DECLARE
    difficulty_level VARCHAR;
BEGIN
    IF level <= 40 THEN
        difficulty_level := 'Normal Difficulty';
    ELSIF level BETWEEN 41 AND 60 THEN
        difficulty_level := 'Nightmare Difficulty';
    ELSIF level > 60 THEN
        difficulty_level := 'Hell Difficulty';
    END IF;

    RETURN difficulty_level;
END;
$$
    LANGUAGE plpgsql;


SELECT user_id,
       level,
       cash,
       fn_difficulty_level(level)
FROM users_games
ORDER BY user_id;


CREATE OR REPLACE PROCEDURE sp_deposit_money(
    account_id INT,
    money_amount NUMERIC(4)
)
AS
$$
BEGIN
    UPDATE accounts
    SET balance = balance + money_amount
    WHERE id = account_id;

    COMMIT;
END;
$$
    LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE sp_withdraw_money(
    account_id INT,
    money_amount NUMERIC(4)
)
AS
$$
DECLARE
    account_balance NUMERIC;
BEGIN
    SELECT balance
    FROM accounts
    WHERE id = account_id
    INTO account_balance;

    IF account_balance - money_amount >= 0 THEN
        UPDATE accounts
        SET balance = balance - money_amount
        WHERE id = account_id;

        COMMIT;
    ELSE
        RAISE NOTICE 'Insufficient balance to withdraw %', account_balance;
    END IF;
END;
$$
    LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE sp_transfer_money(
    sender_id INT,
    receiver_id INT,
    amount NUMERIC(4)
)
AS
$$
BEGIN
    CALL sp_withdraw_money(sender_id, amount);
    CALL sp_deposit_money(receiver_id, amount);

    IF (SELECT balance FROM accounts WHERE id = sender_id) >= 0 THEN
        COMMIT;
    ELSE
        ROLLBACK;
    END IF;
END;
$$
    LANGUAGE plpgsql;


DROP PROCEDURE sp_retrieving_holders_with_balance_higher_than;


CREATE TABLE logs
(
    id         SERIAL PRIMARY KEY,
    account_id INT,
    old_sum    NUMERIC,
    new_sum    NUMERIC
);

CREATE OR REPLACE FUNCTION trigger_fn_insert_new_entry_into_logs()
    RETURNS TRIGGER
AS
$$
BEGIN
    INSERT INTO logs (account_id, old_sum, new_sum)
    VALUES (OLD.id, OLD.balance, NEW.balance);

    RETURN NEW;
END;
$$
    LANGUAGE plpgsql;


CREATE TRIGGER tr_account_balance_change
    AFTER UPDATE OF balance
    ON accounts
    FOR EACH ROW
    WHEN (NEW.balance <> OLD.balance)
EXECUTE FUNCTION trigger_fn_insert_new_entry_into_logs();


CREATE TABLE notification_emails
(
    id           SERIAL PRIMARY KEY,
    recipient_id INT,
    subject      VARCHAR,
    body         VARCHAR
);


CREATE OR REPLACE FUNCTION trigger_fn_send_email_on_balance_change()
    RETURNS TRIGGER
AS
$$
BEGIN
    INSERT INTO notification_emails (recipient_id, subject, body)
    VALUES (NEW.account_id,
            'Balance change for account: %', NEW.account_id,
            'On % your balance was changed from % to %', DATE(), NEW.old_sum, NEW.new_sum);
END;
$$
    LANGUAGE plpgsql;


CREATE TRIGGER tr_send_email_on_balance_change
    AFTER UPDATE
    ON logs
    FOR EACH ROW
    WHEN (OLD.new_sum <> OLD.new_sum)
EXECUTE FUNCTION trigger_fn_send_email_on_balance_change();