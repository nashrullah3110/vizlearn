# -*- coding: utf-8 -*-
"""Content for the generated database modules.

The track had twenty-two modules and almost all of them were about writing a
query. Joins, CTEs, window functions and execution order were covered well;
schema design, constraints and concurrency were not covered at all. That is the
wrong half to be missing, because a query that is merely slow gets rewritten
and a schema that permits bad data does not get noticed until it has.

Every page runs real SQLite in the browser, seeded with tables built for the
module. The error messages are the database's own - a foreign key violation
here is the message a reader will meet again in a real connection, not a
paraphrase of it.
"""

TOPICS = []


def topic(slug, title, cat, lead, svg, notes, article, check,
          seed=None, starter=None, variants=None, variants_label=None,
          timeline=None):
    TOPICS.append({
        "slug": slug, "title": title, "cat": cat, "lead": lead, "svg": svg,
        "seed": seed, "starter": starter, "variants": variants,
        "variants_label": variants_label, "timeline": timeline,
        "notes": notes, "article": article, "check": check,
    })


A = "var(--accent-primary)"
M = "var(--text-muted)"
B = "var(--border-subtle)"
S = "var(--bg-surface)"


def _svg(body):
    return '<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full">%s</svg>' % body


def _box(x, y, w, h, fill="none", stroke=B, sw=2, rx=3):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
            'stroke="%s" stroke-width="%s"/>' % (x, y, w, h, rx, fill, stroke, sw))


def _txt(x, y, s, fill=M, size=9, anchor="middle", weight="normal"):
    return ('<text x="%s" y="%s" fill="%s" font-size="%s" font-family="monospace" '
            'text-anchor="%s" font-weight="%s">%s</text>'
            % (x, y, fill, size, anchor, weight, s))


def _line(x1, y1, x2, y2, stroke=A, sw=1.4, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>'
            % (x1, y1, x2, y2, stroke, sw, d))


def _table_icon(x, y, w=44, rows=3):
    out = [_box(x, y, w, 10 + rows * 9, fill=S)]
    out.append(_box(x, y, w, 10, fill=A, stroke=B, sw=1))
    for r in range(rows):
        out.append(_line(x, y + 10 + r * 9, x + w, y + 10 + r * 9, B, 0.8))
    return "".join(out)


# ---------------------------------------------------------------------------
# 1. Primary and foreign keys
# ---------------------------------------------------------------------------
topic(
    "primary_and_foreign_keys",
    "Primary and Foreign Keys",
    "Schema Design",
    "The two constraints that stop a database from holding rows that cannot be "
    "true. Try to break them and watch the insert be refused.",
    _svg(_table_icon(14, 22) + _txt(36, 82, "customers", M, 8)
         + _line(58, 40, 100, 40) + _txt(79, 34, "FK", A, 8)
         + _table_icon(100, 22) + _txt(122, 82, "orders", M, 8)),
    seed="""
CREATE TABLE customers (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL
);

CREATE TABLE orders (
    id           INTEGER PRIMARY KEY,
    customer_id  INTEGER NOT NULL REFERENCES customers(id),
    total        REAL NOT NULL
);

INSERT INTO customers (id, name) VALUES (1, 'Ada'), (2, 'Grace'), (3, 'Alan');
INSERT INTO orders (id, customer_id, total) VALUES
    (1, 1, 42.00), (2, 1, 18.50), (3, 2, 99.99);

PRAGMA foreign_keys = ON;
""",
    starter="""-- Try each of these in turn.

-- 1. A duplicate primary key.
INSERT INTO orders (id, customer_id, total) VALUES (1, 2, 5.00);

-- 2. An order for a customer who does not exist.
-- INSERT INTO orders (id, customer_id, total) VALUES (9, 77, 5.00);

-- 3. Deleting a customer who still has orders.
-- DELETE FROM customers WHERE id = 1;
""",
    notes=[
        "A primary key is two promises in one: the value is unique, and it is "
        "never NULL.",
        "A foreign key says this column's value must already exist in another "
        "table's key column.",
        "The database enforces both on every write. Application code that "
        "checks first still has a race; the constraint does not.",
        "SQLite needs <code class='mono-font'>PRAGMA foreign_keys = ON</code>. "
        "Most engines enforce them by default.",
    ],
    article="""
title: Primary and Foreign Keys
intro: The two constraints that make a row impossible to write if it could not be true.

## A key is a promise about identity

A **primary key** is the column, or set of columns, whose value identifies a
row uniquely and permanently. Declaring one asks the database for two
guarantees at once: no two rows share this value, and no row leaves it NULL.

That second half is easy to overlook and does real work. NULL means unknown. A
row whose identity is unknown cannot be referred to, updated with confidence,
or joined against, so a nullable identifier is not an identifier at all.

Run the first statement in the editor. The insert is refused, and the message
comes from SQLite rather than from anything on this page:
`UNIQUE constraint failed: orders.id`. Nothing in the application had to check
first, and no amount of concurrent traffic can slip a duplicate past it.

## A foreign key is a promise about reference

A **foreign key** says: whatever value sits in this column must already exist
in that column of that table. `orders.customer_id` references `customers.id`,
so an order can only belong to a customer who is really there.

Uncomment the second statement and run it. Order 9 claims customer 77, and
customer 77 does not exist, so the write fails. Without the constraint the row
would be accepted and the problem would surface much later, as a join that
silently returns fewer rows than expected or a report whose totals do not
reconcile.

This is the value of the constraint and it is worth stating plainly: it turns a
data-quality problem, which is discovered weeks later by a human, into a write
error, which is discovered immediately by a machine.

## What happens to the other side

Uncomment the third statement. Deleting customer 1 is refused, because orders 1
and 2 point at that customer and removing it would leave them pointing at
nothing. The database will not create the orphan.

Refusing is one of several available answers, chosen with `ON DELETE`:

| Clause | Behaviour |
|---|---|
| `RESTRICT` / `NO ACTION` | refuse the delete while children exist (the default) |
| `CASCADE` | delete the children too |
| `SET NULL` | keep the children, blank the reference |
| `SET DEFAULT` | point the children at a default row |

`CASCADE` is convenient and worth respecting. Deleting one customer can silently
remove thousands of orders, and a cascade that runs through several tables can
remove a great deal more than the person pressing the button expected.

## Natural against surrogate

Given a table of people, is the primary key the email address or an integer
that means nothing?

An email address is a **natural key**: it comes from the domain and carries
meaning. It is also mutable, occasionally shared, sometimes absent, and awkward
to index. Every row that references it stores a whole string, and a person
changing their address means updating every one of them.

A meaningless integer is a **surrogate key**. It is stable because nothing in
the world can force it to change, compact to store and to index, and safe to
scatter across a dozen referencing tables.

The usual practice is a surrogate primary key plus a `UNIQUE` constraint on the
natural one, which buys stable identity and still refuses two accounts on the
same address.

## Composite keys

A key can span several columns. A table recording which student is enrolled on
which course has a primary key of `(student_id, course_id)`: neither column
alone identifies a row, and the pair does. That declaration also states a
business rule &mdash; a student can enrol on a course once &mdash; which the
database will now enforce for free.

## Where it goes wrong

**Turning foreign keys off for performance.** They cost something on write. The
cost of not having them is discovered in production, in data that no longer
makes sense, and it is much harder to pay.

**Forgetting the pragma.** SQLite ships with foreign key enforcement off for
backwards compatibility. A schema full of `REFERENCES` clauses that were never
enforced looks correct and guarantees nothing.

**Making the primary key meaningful.** Anything that carries meaning can change,
and a primary key that changes has to be chased through every table that
references it.

**Leaving the foreign key column unindexed.** The parent side is indexed by its
primary key automatically. The child side usually is not, and every cascade or
referential check then scans the whole child table.
""",
    check=[
        {"q": "What two guarantees does declaring a primary key give you?",
         "options": ["Uniqueness and an index", "Uniqueness and NOT NULL",
                     "NOT NULL and a default", "Uniqueness and sort order"],
         "answer": 1,
         "why": "No two rows may share the value, and no row may leave it NULL. A row whose identity is unknown cannot be referred to at all."},
        {"q": "Why is a surrogate integer usually preferred over an email address as a primary key?",
         "options": ["Integers sort faster",
                     "Nothing in the world can force it to change, so referencing rows never need updating",
                     "Emails cannot be indexed",
                     "It uses less disk"],
         "answer": 1,
         "why": "A natural key carries meaning and meaning changes. A person changing their email would mean updating every referencing row; a meaningless integer is stable by construction."},
        {"q": "Why does SQLite in particular need `PRAGMA foreign_keys = ON`?",
         "options": ["It has no foreign keys",
                     "Enforcement is off by default for backwards compatibility, so REFERENCES clauses are accepted but ignored",
                     "It only enforces them on DELETE",
                     "The pragma creates the index"],
         "answer": 1,
         "why": "The schema parses and looks correct while guaranteeing nothing, which is worse than having no constraint at all because it invites trust."},
    ],
)


# ---------------------------------------------------------------------------
# 2. Constraints
# ---------------------------------------------------------------------------
topic(
    "constraints_in_sql",
    "Constraints: UNIQUE, CHECK and NOT NULL",
    "Schema Design",
    "Rules the database refuses to break, written once in the schema instead "
    "of everywhere in the application.",
    _svg(_box(20, 26, 120, 40, fill=S)
         + _txt(80, 42, "CHECK (age &gt;= 18)", A, 10)
         + _txt(80, 58, "refused on write", M, 8)
         + _txt(80, 80, "one rule, every client", M, 7)),
    seed="""
CREATE TABLE staff (
    id      INTEGER PRIMARY KEY,
    email   TEXT    NOT NULL UNIQUE,
    age     INTEGER NOT NULL CHECK (age >= 18),
    salary  REAL    NOT NULL CHECK (salary > 0),
    grade   TEXT    NOT NULL DEFAULT 'junior'
                    CHECK (grade IN ('junior', 'mid', 'senior'))
);

INSERT INTO staff (id, email, age, salary, grade) VALUES
    (1, 'ada@example.com',   36, 62000, 'senior'),
    (2, 'grace@example.com', 41, 71000, 'senior'),
    (3, 'alan@example.com',  28, 48000, 'mid');
""",
    starter="""-- Each of these violates exactly one constraint.
-- Run them one at a time and read which one fires.

INSERT INTO staff (id, email, age, salary) VALUES (4, 'ada@example.com', 30, 50000);

-- INSERT INTO staff (id, email, age, salary) VALUES (5, 'new@example.com', 15, 50000);
-- INSERT INTO staff (id, email, age, salary) VALUES (6, 'x@example.com', 30, -1);
-- INSERT INTO staff (id, email, age, salary, grade) VALUES (7, 'y@example.com', 30, 1, 'boss');
-- INSERT INTO staff (id, email, age) VALUES (8, 'z@example.com', 30);
""",
    notes=[
        "<code class='mono-font'>NOT NULL</code> says the value must be known. "
        "<code class='mono-font'>UNIQUE</code> says no other row may hold it.",
        "<code class='mono-font'>CHECK</code> takes an expression that must be "
        "true for every row. It is the general case the others specialise.",
        "A constraint holds regardless of which client wrote the row. "
        "Application validation only holds for the clients that run it.",
        "<code class='mono-font'>UNIQUE</code> permits multiple NULLs in most "
        "engines, because two unknowns are not known to be equal.",
    ],
    article="""
title: Constraints: UNIQUE, CHECK and NOT NULL
intro: Rules written once in the schema, enforced against every client, forever.

## Where a rule should live

"Age must be at least 18" can be written in three places: the form in the
browser, the service that handles the request, or the table itself.

The first two are worth having and neither is sufficient. A browser check is a
courtesy to the user and is bypassed by anything that is not a browser. A
service check holds until someone writes a second service, a migration script,
a bulk import or a manual fix at the console &mdash; and every one of those is
written by someone who was not thinking about the rule at the time.

A constraint in the schema holds for all of them, including the ones that do
not exist yet. It is checked on every write, by the one component every path
must go through.

## The three, and what each says

**NOT NULL** &mdash; the value must be known. NULL is not a value; it is the
absence of one. Allowing it means allowing rows where the question was never
answered, and every query that touches the column then has to decide what to do
about that.

**UNIQUE** &mdash; no other row may hold this value. It is what stops two
accounts sharing an email address without requiring a read-then-write in the
application, which is a race condition even when it looks correct.

**CHECK** &mdash; this expression must be true for every row. It is the general
case that the other two are special instances of, and it takes ordinary SQL:

```
CHECK (age >= 18)
CHECK (salary > 0)
CHECK (grade IN ('junior', 'mid', 'senior'))
CHECK (end_date IS NULL OR end_date > start_date)
```

That last one is worth noticing. A constraint can relate two columns of the same
row, so "an end date, if present, must come after the start date" is enforceable
&mdash; a rule that is otherwise checked nowhere and violated eventually.

## Read the error, not the row count

Run each commented statement in turn. The value of doing so is that every one
fails differently, and the message names the constraint that stopped it:

| Attempt | Message |
|---|---|
| Duplicate email | `UNIQUE constraint failed: staff.email` |
| Age 15 | `CHECK constraint failed` |
| Negative salary | `CHECK constraint failed` |
| Grade `'boss'` | `CHECK constraint failed` |
| Missing salary | `NOT NULL constraint failed: staff.salary` |

Naming constraints explicitly &mdash; `CONSTRAINT staff_age_adult CHECK (...)`
&mdash; makes those messages far more useful, because "CHECK constraint failed"
tells you nothing when a table has six of them.

## The NULL subtlety in UNIQUE

`UNIQUE` allows more than one NULL in almost every engine, and people are
surprised by this until they see the reasoning.

`UNIQUE` forbids two rows being *equal*. Comparing NULL to NULL does not
produce true; it produces NULL, because two unknown values are not known to be
the same. So two NULLs are not equal, and the constraint has nothing to object
to.

The practical consequence is that `UNIQUE` on a nullable column does not
guarantee one row per real-world thing &mdash; it guarantees one row per *known*
value. If that is not what you meant, add `NOT NULL`.

## DEFAULT is not a constraint

`DEFAULT 'junior'` supplies a value when the insert omits the column. It
constrains nothing: an insert that explicitly passes NULL gets NULL, not the
default, unless `NOT NULL` refuses it.

Defaults and constraints are frequently paired for this reason. The default
handles the common case, and the constraint handles the case where someone was
explicit about something they should not have been.

## Where it goes wrong

**Unnamed constraints.** Six `CHECK`s on a table and an error that says only
"CHECK constraint failed" wastes real time. Name them.

**Constraints that encode volatile policy.** A `CHECK` on a VAT rate has to be
migrated when the rate changes, and migrating a constraint on a large table is
not free. Constrain what is structurally true, not what is currently true.

**Assuming UNIQUE means one per thing.** With NULLs allowed it means one per
known value.

**Adding a constraint to a large live table without thinking.** The database has
to verify every existing row before it can accept the constraint, and in most
engines that takes a lock while it does.
""",
    check=[
        {"q": "Why does UNIQUE usually permit several NULLs?",
         "options": ["NULLs are stored separately",
                     "UNIQUE forbids equal values, and two NULLs are not known to be equal",
                     "It is a bug retained for compatibility",
                     "NULL is treated as zero"],
         "answer": 1,
         "why": "Comparing NULL to NULL yields NULL, not true. The constraint only rejects rows it can prove equal, so unknown values slip through - add NOT NULL if that is not what you meant."},
        {"q": "What can a CHECK constraint do that NOT NULL and UNIQUE cannot?",
         "options": ["Run on delete",
                     "Relate two columns of the same row, such as end_date > start_date",
                     "Reference another table",
                     "Supply a default value"],
         "answer": 1,
         "why": "CHECK takes an arbitrary expression over the row, so multi-column rules are enforceable. They are otherwise checked nowhere and violated eventually."},
        {"q": "Why is a constraint stronger than the same rule in application code?",
         "options": ["It runs faster",
                     "It holds for every client, including migrations, imports and consoles that were never written yet",
                     "It cannot be dropped",
                     "It produces better error messages"],
         "answer": 1,
         "why": "Application validation holds only for the code paths that run it. The database is the one component every write must pass through."},
    ],
)


# ---------------------------------------------------------------------------
# 3. Aggregate functions
# ---------------------------------------------------------------------------
topic(
    "aggregate_functions_in_sql",
    "Aggregate Functions and the NULL Trap",
    "Querying",
    "COUNT, SUM, AVG, MIN and MAX over a live table, and the one thing they "
    "all do with NULL that catches people out.",
    _svg("".join(_box(18 + i * 15, 30, 11, 26, fill=S) for i in range(5))
         + _txt(80, 70, "many rows &#8594; one value", M, 8)
         + _txt(80, 22, "SUM  AVG  COUNT", A, 9)),
    seed="""
CREATE TABLE readings (
    id       INTEGER PRIMARY KEY,
    station  TEXT NOT NULL,
    temp_c   REAL          -- deliberately nullable: the sensor sometimes fails
);

INSERT INTO readings (id, station, temp_c) VALUES
    (1, 'north', 12.0), (2, 'north', 14.0), (3, 'north', NULL),
    (4, 'south', 21.5), (5, 'south', NULL),  (6, 'south', 18.5),
    (7, 'west',  NULL),  (8, 'west',  NULL), (9, 'west', 9.0);
""",
    starter="""SELECT COUNT(*)        AS rows_total,
       COUNT(temp_c)   AS rows_with_a_reading,
       SUM(temp_c)     AS total,
       AVG(temp_c)     AS mean,
       MIN(temp_c)     AS coldest,
       MAX(temp_c)     AS warmest
FROM   readings;
""",
    variants_label="Same table, four questions",
    variants=[
        {"label": "The NULL trap",
         "sql": """-- COUNT(*) counts rows. COUNT(col) counts non-NULL values.
-- The gap between them is your missing data, for free.
SELECT COUNT(*) AS rows_total,
       COUNT(temp_c) AS have_reading,
       COUNT(*) - COUNT(temp_c) AS missing
FROM   readings;"""},
        {"label": "AVG ignores NULL",
         "sql": """-- AVG skips NULLs entirely. It is SUM/COUNT(col), not SUM/COUNT(*).
-- Substituting zero for a missing reading gives a different, wrong answer.
SELECT AVG(temp_c)                  AS avg_skipping_nulls,
       AVG(COALESCE(temp_c, 0))     AS avg_treating_null_as_zero,
       SUM(temp_c) / COUNT(*)       AS sum_over_all_rows
FROM   readings;"""},
        {"label": "Per group",
         "sql": """SELECT station,
       COUNT(*)      AS readings,
       COUNT(temp_c) AS usable,
       ROUND(AVG(temp_c), 2) AS mean_c
FROM   readings
GROUP  BY station
ORDER  BY station;"""},
        {"label": "Aggregating over no values at all",
         "sql": """-- Restrict to the rows that have no reading. COUNT(*) is 3, COUNT of
-- the column is 0, and SUM, AVG, MIN and MAX all come back NULL --
-- not zero, and not an error. Only COUNT returns a number.
SELECT COUNT(*)      AS rows_seen,
       COUNT(temp_c) AS values_seen,
       SUM(temp_c)   AS sum_c,
       AVG(temp_c)   AS avg_c,
       MIN(temp_c)   AS min_c,
       MAX(temp_c)   AS max_c
FROM   readings
WHERE  temp_c IS NULL;"""},
    ],
    notes=[
        "An aggregate collapses many rows into one value. Without "
        "<code class='mono-font'>GROUP BY</code> the whole table is one group.",
        "<code class='mono-font'>COUNT(*)</code> counts rows. "
        "<code class='mono-font'>COUNT(col)</code> counts rows where col is not "
        "NULL. The difference is your missing data.",
        "Every other aggregate skips NULL silently. "
        "<code class='mono-font'>AVG</code> divides by the number of values it "
        "actually saw, not by the number of rows.",
        "An aggregate over zero values is NULL, not zero &mdash; except "
        "<code class='mono-font'>COUNT</code>, which is 0.",
    ],
    article="""
title: Aggregate Functions and the NULL Trap
intro: Five functions that collapse many rows into one, and the one behaviour they share that quietly changes your answers.

## Many rows in, one value out

An aggregate function takes a set of rows and returns a single value. With no
`GROUP BY`, the set is the whole table; with one, it is each group in turn.

The five that matter are `COUNT`, `SUM`, `AVG`, `MIN` and `MAX`. Run the
starter query and all five appear side by side over the same nine rows. The
numbers do not agree with each other in the way you might expect, and the reason
is NULL.

## COUNT(*) and COUNT(col) are different functions

This is the single most useful distinction on the page.

`COUNT(*)` counts **rows**. It does not look at any column, cannot be affected
by NULL, and answers "how many records are there".

`COUNT(temp_c)` counts **non-NULL values in that column**. It answers "how many
records actually have a reading".

The table has nine rows and four of them have no temperature. So `COUNT(*)` is
9 and `COUNT(temp_c)` is 5, and the gap between them is a free measure of
missing data:

```
SELECT COUNT(*) - COUNT(temp_c) AS missing FROM readings;
```

That one line is worth reaching for whenever a column's quality is in question.
It needs no subquery, no `IS NULL` filter and no second pass.

## Everything else skips NULL silently

`SUM`, `AVG`, `MIN` and `MAX` all ignore NULL. They do not fail, warn, or
return NULL because a NULL was present &mdash; they behave as though those rows
were not there.

For `SUM`, `MIN` and `MAX` this is almost always what you want. For `AVG` it is
the thing that catches people, because **AVG divides by the count of values, not
the count of rows**:

```
AVG(temp_c)  =  SUM(temp_c) / COUNT(temp_c)
```

Run the second variant. Three numbers appear that all have a claim to being
"the average temperature", and they differ substantially:

| Expression | What it means |
|---|---|
| `AVG(temp_c)` | mean of the readings that exist |
| `AVG(COALESCE(temp_c, 0))` | mean if a broken sensor means zero degrees |
| `SUM(temp_c) / COUNT(*)` | total spread across all rows including the broken ones |

Which is correct depends entirely on what NULL means in your data. If the sensor
failed, the first is right and the others are nonsense &mdash; a broken sensor
is not a reading of zero. If NULL means "no sales that day", the second may well
be right. The database cannot decide this for you, and it will not ask.

## The empty group

Run the fourth variant. It restricts to the rows that have no reading at all,
so there are four rows and zero values, and every aggregate has to say what it
does with nothing.

`COUNT(*)` is 4 and `COUNT(temp_c)` is 0, as expected. `SUM`, `AVG`, `MIN` and
`MAX` all come back **NULL** &mdash; not zero, and not an error. The rule is
that an aggregate over zero values returns NULL, and the single exception is
`COUNT`, which returns 0 because counting nothing genuinely is zero.

This matters when an aggregate feeds arithmetic. `SUM(amount) * 1.2` over a
group with no rows is NULL, and NULL propagates through every operation it
touches until something wraps it in `COALESCE`.

## GROUP BY and the shape of the result

Adding `GROUP BY station` changes the result from one row to one row per
station. The rule that follows is the one beginners trip on: every column in the
`SELECT` list must either be aggregated or appear in the `GROUP BY`.

The reason is that the query has to produce exactly one value per group. Given
three readings for `north`, there is no answer to "what is the id" &mdash;
there are three, and the database will not choose one. Some engines historically
allowed it and returned an arbitrary row, which is worse than an error because
it works until it does not.

## Where it goes wrong

**Using AVG on data where NULL means zero.** The average silently rises. Use
`COALESCE` when absence really is a zero.

**Assuming COUNT(col) is a faster COUNT(*).** They answer different questions.
On a nullable column they return different numbers.

**Filtering aggregates in WHERE.** `WHERE COUNT(*) > 5` is an error &mdash;
`WHERE` runs before grouping, so no counts exist yet. That is what
[HAVING](having_in_sql.html) is for.

**Forgetting that NULL breaks arithmetic.** One NULL anywhere in an expression
makes the whole expression NULL.
""",
    check=[
        {"q": "What is the difference between COUNT(*) and COUNT(temp_c)?",
         "options": ["None, they are aliases",
                     "COUNT(*) counts rows; COUNT(temp_c) counts rows where that column is not NULL",
                     "COUNT(*) is slower",
                     "COUNT(temp_c) counts distinct values"],
         "answer": 1,
         "why": "The gap between them is exactly the number of missing values in the column, which makes it a one-line data-quality check."},
        {"q": "AVG(temp_c) over nine rows, four of them NULL, divides the sum by what?",
         "options": ["9", "5", "4", "It returns NULL"],
         "answer": 1,
         "why": "AVG skips NULLs entirely - it is SUM(col)/COUNT(col). Whether that is the answer you want depends on what NULL means in your data."},
        {"q": "What does SUM return over a group containing no non-NULL values?",
         "options": ["0", "NULL", "An error", "The row count"],
         "answer": 1,
         "why": "Every aggregate except COUNT returns NULL over nothing. That NULL then propagates through any arithmetic it feeds, which is why COALESCE turns up around aggregates so often."},
    ],
)


# ---------------------------------------------------------------------------
# 4. EXISTS vs IN vs JOIN
# ---------------------------------------------------------------------------
topic(
    "exists_vs_in_vs_join",
    "EXISTS, IN and JOIN",
    "Querying",
    "One question written three ways. Two give the same answer, one does not, "
    "and NULL decides which.",
    _svg(_txt(80, 24, "customers who ordered", M, 8)
         + _box(12, 34, 42, 24, fill=S) + _txt(33, 49, "EXISTS", A, 9)
         + _box(59, 34, 42, 24, fill=S) + _txt(80, 49, "IN", A, 9)
         + _box(106, 34, 42, 24, fill=S) + _txt(127, 49, "JOIN", A, 9)
         + _txt(80, 76, "same rows, different traps", M, 7)),
    seed="""
CREATE TABLE customers (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER,       -- nullable on purpose: some orders are anonymous
    total       REAL NOT NULL
);

INSERT INTO customers (id, name) VALUES
    (1, 'Ada'), (2, 'Grace'), (3, 'Alan'), (4, 'Edsger');

INSERT INTO orders (id, customer_id, total) VALUES
    (1, 1, 42.00), (2, 1, 18.50), (3, 2, 99.99), (4, NULL, 7.25);
""",
    starter="""-- Customers who have placed at least one order.
SELECT name
FROM   customers c
WHERE  EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id)
ORDER  BY name;
""",
    variants_label="One question, four ways",
    variants=[
        {"label": "EXISTS",
         "sql": """-- Stops at the first matching row. Correct with NULLs present.
SELECT name
FROM   customers c
WHERE  EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id)
ORDER  BY name;"""},
        {"label": "IN",
         "sql": """-- Same answer here. Fine, because we are asking for a match.
SELECT name
FROM   customers c
WHERE  c.id IN (SELECT customer_id FROM orders)
ORDER  BY name;"""},
        {"label": "JOIN",
         "sql": """-- Careful: a customer with two orders appears twice unless
-- you add DISTINCT. Compare this with the EXISTS version.
SELECT c.name
FROM   customers c
JOIN   orders o ON o.customer_id = c.id
ORDER  BY c.name;"""},
        {"label": "NOT IN - the broken one",
         "sql": """-- The point of the page. NOT IN returns NO ROWS, because the
-- subquery contains a NULL and 'x <> NULL' is unknown, never true.
-- NOT EXISTS gets it right. Run both.
SELECT 'NOT IN' AS form, name FROM customers c
WHERE  c.id NOT IN (SELECT customer_id FROM orders)

UNION ALL

SELECT 'NOT EXISTS', name FROM customers c
WHERE  NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);"""},
    ],
    notes=[
        "<code class='mono-font'>EXISTS</code> asks whether any row matches and "
        "stops at the first one. It never returns the row itself.",
        "<code class='mono-font'>IN</code> compares a value against a list. With "
        "a NULL in that list, <code class='mono-font'>NOT IN</code> can never be "
        "true.",
        "<code class='mono-font'>JOIN</code> multiplies rows: one customer with "
        "three orders becomes three rows unless you aggregate or add "
        "<code class='mono-font'>DISTINCT</code>.",
        "Modern planners often compile all three to the same plan. Correctness "
        "is the reason to choose, not speed.",
    ],
    article="""
title: EXISTS, IN and JOIN
intro: Three ways to ask whether a related row exists, and the one that is quietly wrong.

## The same question

"Which customers have placed an order?" can be written with `EXISTS`, with `IN`,
or as a `JOIN`. Run the first three variants above and all three return Ada and
Grace &mdash; except that the JOIN returns Ada twice.

That difference is the first thing to understand, and the NULL behaviour of the
fourth is the second.

## JOIN multiplies rows

A join does not filter the left table. It pairs every row on the left with every
matching row on the right, so a customer with three orders produces three
result rows.

When you want the orders, that is exactly right. When you want the customers,
it is a bug, and the usual patch is `DISTINCT`. That works, but it is worth
knowing what it costs: the database produced the duplicate rows and then sorted
or hashed them away. `EXISTS` never produces them in the first place.

The rule of thumb: **join when you want columns from the other table, use
EXISTS when you only want to know whether it is there**.

## EXISTS stops early

`EXISTS (subquery)` is true if the subquery returns at least one row. Not how
many, not which &mdash; just whether. That is why `SELECT 1` is the conventional
body: nothing in the select list is ever read, so there is no reason to name a
column.

Because only existence matters, the engine can stop scanning the moment it finds
one match. For a customer with ten thousand orders, `EXISTS` looks at one.

`EXISTS` is also *correlated*: the subquery references `c.id` from the outer
query, so it is conceptually re-evaluated per outer row. Planners rarely execute
it that literally, but writing it that way is what makes the early exit
available.

## Where NOT IN breaks

Run the fourth variant. `NOT IN` returns **no rows at all**, and `NOT EXISTS`
returns Alan and Edsger, which is the correct answer.

Nothing is wrong with the data. Order 4 is anonymous, so its `customer_id` is
NULL, and the subquery returns the list `(1, 1, 2, NULL)`.

`c.id NOT IN (1, 1, 2, NULL)` expands to:

```
c.id <> 1  AND  c.id <> 1  AND  c.id <> 2  AND  c.id <> NULL
```

The final comparison is not false &mdash; it is **unknown**. Alan's id is 3, and
whether 3 differs from an unknown value cannot be determined. `AND` with unknown
gives unknown, `WHERE` keeps only rows that are definitely true, and so nothing
survives. Every row is filtered out, for every customer, silently and without an
error.

`NOT EXISTS` is unaffected because it never compares anything to NULL. It asks
whether a matching row was found, and the answer to that is always yes or no.

This is the practical rule, and it is worth committing to memory:

> **`NOT IN` with a nullable subquery column is a bug.** Use `NOT EXISTS`, or
> add `WHERE customer_id IS NOT NULL` to the subquery.

The positive forms do not have this problem. `IN` returns true as soon as it
finds a real match, and an unknown among the remaining comparisons cannot take
that away.

## What about performance

Twenty years ago these three had genuinely different costs and the advice was
elaborate. Modern planners in PostgreSQL, SQL Server and Oracle recognise all
three shapes and frequently compile them to the same physical plan &mdash;
usually a semi-join, which is precisely "find whether a match exists, do not
duplicate rows".

So performance is rarely the reason to choose. The reasons that survive are:

| Want | Use | Because |
|---|---|---|
| Columns from the other table | `JOIN` | it is the only one that gives them |
| Just to know it exists | `EXISTS` | no duplicates, early exit |
| Absence, nullable column | `NOT EXISTS` | `NOT IN` returns nothing |
| A short literal list | `IN` | `IN (1, 2, 3)` reads better than anything else |

Check the plan when it matters. [EXPLAIN](explain_and_query_plans.html) settles
in ten seconds what a rule of thumb argues about indefinitely.

## Where it goes wrong

**`NOT IN` on anything nullable.** The query returns zero rows and looks like a
data problem.

**`SELECT *` inside `EXISTS`.** Harmless but misleading &mdash; it suggests the
columns are read, and they never are.

**`DISTINCT` as a reflex.** If a join is producing duplicates, ask whether you
wanted the join at all. `DISTINCT` hides the symptom and pays for the rows twice.
""",
    check=[
        {"q": "Why does NOT IN return no rows when the subquery contains a NULL?",
         "options": ["NULL is treated as zero",
                     "The comparison against NULL is unknown rather than false, and WHERE keeps only definitely-true rows",
                     "NOT IN does not support subqueries",
                     "The subquery fails silently"],
         "answer": 1,
         "why": "NOT IN expands to a chain of <> comparisons joined by AND. One unknown makes the whole chain unknown for every row, so nothing survives the WHERE."},
        {"q": "Why does a JOIN sometimes return a customer twice when EXISTS does not?",
         "options": ["JOIN ignores the primary key",
                     "A join pairs each left row with every match, so two orders give two rows",
                     "EXISTS deduplicates automatically",
                     "The join is missing a condition"],
         "answer": 1,
         "why": "That multiplication is what a join is for when you want the other table's columns. EXISTS asks only whether a match is there, so it never produces the extra rows."},
        {"q": "Why is `SELECT 1` conventional inside EXISTS?",
         "options": ["It is faster than SELECT *",
                     "The select list is never read, so naming a column would be misleading",
                     "EXISTS requires a literal",
                     "It avoids a NULL check"],
         "answer": 1,
         "why": "EXISTS tests only whether a row was returned. Writing SELECT * suggests the columns matter, and they do not."},
    ],
)


# ---------------------------------------------------------------------------
# 5. Self-joins
# ---------------------------------------------------------------------------
topic(
    "self_joins_in_sql",
    "Self-Joins",
    "Querying",
    "A table joined to itself, so a row can be compared against another row of "
    "the same kind. Employees and their managers, twice over.",
    _svg(_table_icon(20, 24, 40) + _txt(40, 82, "employees e", M, 7)
         + _table_icon(100, 24, 40) + _txt(120, 82, "employees m", M, 7)
         + _line(60, 40, 100, 40) + _txt(80, 34, "manager_id = id", A, 7)),
    seed="""
CREATE TABLE employees (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    manager_id INTEGER REFERENCES employees(id),
    salary     REAL NOT NULL
);

INSERT INTO employees (id, name, manager_id, salary) VALUES
    (1, 'Ada',    NULL, 120000),
    (2, 'Grace',  1,     98000),
    (3, 'Alan',   1,     95000),
    (4, 'Edsger', 2,     88000),
    (5, 'Barbara',2,    101000),
    (6, 'Donald', 3,     72000);
""",
    starter="""-- Two aliases for one table. e is the employee, m is the manager.
SELECT e.name AS employee,
       m.name AS manager
FROM   employees e
JOIN   employees m ON e.manager_id = m.id
ORDER  BY e.name;
""",
    variants_label="What a self-join can answer",
    variants=[
        {"label": "Employee and manager",
         "sql": """SELECT e.name AS employee, m.name AS manager
FROM   employees e
JOIN   employees m ON e.manager_id = m.id
ORDER  BY e.name;"""},
        {"label": "Keep the one with no manager",
         "sql": """-- Ada reports to nobody. An inner join drops her; LEFT JOIN keeps her
-- with a NULL manager, which is usually what you meant.
SELECT e.name AS employee, m.name AS manager
FROM   employees e
LEFT   JOIN employees m ON e.manager_id = m.id
ORDER  BY e.name;"""},
        {"label": "Paid more than their manager",
         "sql": """-- The comparison a self-join exists for: row against row.
SELECT e.name AS employee, e.salary, m.name AS manager, m.salary AS manager_salary
FROM   employees e
JOIN   employees m ON e.manager_id = m.id
WHERE  e.salary > m.salary;"""},
        {"label": "Pairs, without duplicates",
         "sql": """-- Every pair of colleagues under the same manager. The < in the
-- join condition is what stops (Alan, Grace) and (Grace, Alan) both
-- appearing, and stops anyone pairing with themselves.
SELECT a.name AS one, b.name AS other, a.manager_id AS under
FROM   employees a
JOIN   employees b ON a.manager_id = b.manager_id AND a.id < b.id
ORDER  BY under, one;"""},
    ],
    notes=[
        "There is nothing special about the syntax. It is an ordinary join "
        "where both sides happen to name the same table.",
        "Aliases stop being optional. Without <code class='mono-font'>e</code> "
        "and <code class='mono-font'>m</code> there is no way to say which "
        "<code class='mono-font'>name</code> you mean.",
        "An inner self-join silently drops the top of a hierarchy, because the "
        "root's parent is NULL. <code class='mono-font'>LEFT JOIN</code> keeps it.",
        "<code class='mono-font'>a.id &lt; b.id</code> in the join condition "
        "turns every unordered pair from two rows into one.",
    ],
    article="""
title: Self-Joins
intro: A table joined to itself, and the three questions that need one.

## Nothing new, except the alias

A self-join is an ordinary join in which both sides are the same table. There
is no special keyword and no special execution; the only thing that changes is
that aliases become mandatory.

```
FROM  employees e
JOIN  employees m ON e.manager_id = m.id
```

`e` and `m` are two independent views of the same rows. Without them, `name`
would be ambiguous &mdash; the database has two columns with that name in scope
and no way to guess which was meant.

The mental move that makes this click is to stop thinking of `e` and `m` as one
table used twice, and start thinking of them as two tables that happen to
contain identical data. Everything else about joins then applies unchanged.

## When you need one

Self-joins answer questions that involve **comparing a row to another row of the
same kind**, which SQL otherwise makes awkward.

**Hierarchies stored in one table.** An employee's manager is another employee.
A category's parent is another category. A reply's target is another comment.
Joining the table to itself resolves the reference into real columns.

**Row-to-row comparisons.** "Who earns more than their manager" needs both
salaries available at once. Run the third variant: Barbara earns 101,000 and
reports to Grace on 98,000, and the join is what puts those two numbers in one
row so a `WHERE` can compare them.

**Pairing rows within a group.** "Which colleagues share a manager" pairs the
table with itself on `manager_id`.

## The two conditions that keep pairs sane

The fourth variant contains a detail that looks small and is not:

```
ON a.manager_id = b.manager_id AND a.id < b.id
```

Without `a.id < b.id`, two things go wrong. Every row pairs with **itself**,
because a row trivially shares its own manager. And every genuine pair appears
**twice**, once as (Alan, Grace) and once as (Grace, Alan).

Writing `a.id <> b.id` fixes the first problem and not the second. Writing
`a.id < b.id` fixes both at once, because for any two distinct rows exactly one
ordering satisfies it. That is the standard idiom for "each unordered pair once"
and it is worth recognising on sight.

## The top of the hierarchy disappears

Run the first variant and count the rows: five, not six. Ada is missing.

Ada is the root &mdash; her `manager_id` is NULL &mdash; and an inner join
requires a match on both sides. NULL matches nothing, so her row is dropped
without comment.

The second variant uses `LEFT JOIN` and Ada reappears with a NULL manager. This
is nearly always what was intended, and the failure is quiet enough to reach
production: the query works, returns plausible rows, and is missing exactly the
most senior person in the organisation.

## Depth is where it stops

A self-join resolves **one** level. Employee to manager is one join. Employee to
manager's manager is two, written out by hand:

```
FROM employees e
JOIN employees m  ON e.manager_id = m.id
JOIN employees mm ON m.manager_id = mm.id
```

Three levels needs three, and an arbitrary depth cannot be written this way at
all, because the number of joins would have to depend on the data.

That is the boundary where the technique runs out and
[recursive CTEs](recursive_ctes_in_sql.html) take over. A recursive CTE walks
down as many levels as exist, and it is the correct tool the moment the depth is
not known in advance.

## Where it goes wrong

**Inner join on a nullable parent.** The root vanishes. This is the single most
common self-join bug.

**Forgetting the anti-self condition.** Without `a.id < b.id` every row pairs
with itself, and totals come out roughly double.

**Using one for arbitrary depth.** If the query has four copies of the same
table and someone is about to add a fifth, it wants to be recursive.

**Leaving the join column unindexed.** A self-join reads the table twice. On a
large table with no index on `manager_id`, that is two full scans and a hash in
between.
""",
    check=[
        {"q": "Why does an inner self-join drop the top of a hierarchy?",
         "options": ["The root has no id",
                     "The root's parent reference is NULL and NULL matches nothing",
                     "Inner joins skip the first row",
                     "The alias is missing"],
         "answer": 1,
         "why": "An inner join needs a match on both sides. The root's manager_id is NULL, so no row matches and it is dropped silently - LEFT JOIN keeps it with a NULL manager."},
        {"q": "Why is `a.id < b.id` preferred over `a.id <> b.id` when pairing rows?",
         "options": ["It is faster",
                     "It stops self-pairing and also returns each unordered pair once instead of twice",
                     "<> does not work on integers",
                     "It handles NULLs"],
         "answer": 1,
         "why": "<> removes self-pairs but still returns both (A, B) and (B, A). For two distinct rows exactly one ordering satisfies <, so each pair appears once."},
        {"q": "When does a self-join stop being the right tool?",
         "options": ["When the table is large",
                     "When the depth of the hierarchy is not known in advance",
                     "When the parent column is nullable",
                     "When more than two columns are selected"],
         "answer": 1,
         "why": "Each level costs one written join, so an unknown depth cannot be expressed. That is exactly what a recursive CTE is for."},
    ],
)


# ---------------------------------------------------------------------------
# 6. Recursive CTEs
# ---------------------------------------------------------------------------
topic(
    "recursive_ctes_in_sql",
    "Recursive CTEs",
    "Querying",
    "A query that feeds its own output back in, one level at a time, until "
    "nothing new comes back.",
    _svg(_box(58, 18, 44, 16, fill=S) + _txt(80, 29, "anchor", A, 8)
         + _line(80, 34, 80, 44) + _box(58, 44, 44, 16, fill=S) + _txt(80, 55, "level 2", M, 8)
         + _line(80, 60, 80, 70) + _box(58, 70, 44, 16, fill=S) + _txt(80, 81, "level 3", M, 8)
         + '<path d="M104 52 q18 -14 0 -28" fill="none" stroke="%s" stroke-width="1.2"/>' % A),
    seed="""
CREATE TABLE employees (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    manager_id INTEGER REFERENCES employees(id)
);

INSERT INTO employees (id, name, manager_id) VALUES
    (1, 'Ada',     NULL),
    (2, 'Grace',   1),
    (3, 'Alan',    1),
    (4, 'Edsger',  2),
    (5, 'Barbara', 2),
    (6, 'Donald',  3),
    (7, 'Tony',    4),
    (8, 'Niklaus', 7);
""",
    starter="""WITH RECURSIVE chain(id, name, manager_id, level) AS (
    -- Anchor: where the walk starts.
    SELECT id, name, manager_id, 1
    FROM   employees
    WHERE  manager_id IS NULL

    UNION ALL

    -- Recursive step: everyone reporting to someone already found.
    SELECT e.id, e.name, e.manager_id, c.level + 1
    FROM   employees e
    JOIN   chain c ON e.manager_id = c.id
)
SELECT level, name FROM chain ORDER BY level, name;
""",
    variants_label="Walking a hierarchy",
    variants=[
        {"label": "Down from the top",
         "sql": """WITH RECURSIVE chain(id, name, manager_id, level) AS (
    SELECT id, name, manager_id, 1
    FROM   employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, c.level + 1
    FROM   employees e JOIN chain c ON e.manager_id = c.id
)
SELECT level, name FROM chain ORDER BY level, name;"""},
        {"label": "Up from one person",
         "sql": """-- The same machinery pointed the other way: start at Niklaus and
-- follow manager_id upwards until it runs out.
WITH RECURSIVE up(id, name, manager_id, step) AS (
    SELECT id, name, manager_id, 0
    FROM   employees WHERE name = 'Niklaus'
    UNION ALL
    SELECT m.id, m.name, m.manager_id, u.step + 1
    FROM   employees m JOIN up u ON u.manager_id = m.id
)
SELECT step, name FROM up ORDER BY step;"""},
        {"label": "With the full path",
         "sql": """-- Building a breadcrumb as you go is the usual reason to carry an
-- extra column through the recursion.
WITH RECURSIVE tree(id, name, path, level) AS (
    SELECT id, name, name, 1
    FROM   employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, t.path || ' > ' || e.name, t.level + 1
    FROM   employees e JOIN tree t ON e.manager_id = t.id
)
SELECT level, path FROM tree ORDER BY path;"""},
        {"label": "Counting, not walking",
         "sql": """-- No table involved. The recursion generates its own rows, which is
-- how you produce a series of dates or numbers without a helper table.
WITH RECURSIVE nums(n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM nums WHERE n < 10
)
SELECT n, n * n AS squared FROM nums;"""},
    ],
    notes=[
        "A recursive CTE has two halves joined by "
        "<code class='mono-font'>UNION ALL</code>: an anchor that runs once, and "
        "a step that runs against what the last round produced.",
        "It stops when the step returns no rows. Nothing else stops it.",
        "The step reads only the <em>previous</em> round's rows, not the whole "
        "accumulated set. That is what makes it a level-by-level walk.",
        "A cycle in the data means the step never comes back empty. Carry a "
        "depth column and cap it.",
    ],
    article="""
title: Recursive CTEs
intro: The one construct in SQL that can follow a chain of unknown length.

## Why plain SQL cannot do this

A self-join resolves one level of a hierarchy. Two joins resolve two. To resolve
five you write five, and to resolve "however many there are" you cannot write
anything at all, because the number of joins would have to depend on data the
query has not read yet.

A **recursive CTE** removes that limit. It runs a query, feeds the result back
into itself, and keeps going until a round produces nothing new.

## The two halves

```
WITH RECURSIVE chain(...) AS (
    <anchor>                -- runs once
    UNION ALL
    <recursive step>        -- runs repeatedly, reads `chain`
)
SELECT ... FROM chain;
```

The **anchor** is an ordinary query. It runs once and produces the starting
rows. In the first variant it selects the employee whose `manager_id` is NULL
&mdash; the root.

The **recursive step** is a query that refers to the CTE by name. It runs against
the rows the previous round produced, not against everything accumulated so far.
That distinction is what makes the walk proceed one level at a time.

Execution goes: anchor produces Ada. Step runs against {Ada} and produces Grace
and Alan. Step runs against {Grace, Alan} and produces Edsger, Barbara, Donald.
Step runs against those and produces Tony. Then Niklaus. Then the step finds
nobody reporting to Niklaus, returns no rows, and the recursion halts.

**The empty result is the only stopping condition.** There is no iteration limit
and no depth check unless you write one.

## Carrying state through

The `level` column in the starter query is not special syntax. It is an ordinary
column: the anchor sets it to 1, and the step sets it to `c.level + 1`. Anything
computed the same way rides along with the recursion.

The third variant builds a text path this way, concatenating each name onto the
one before to produce `Ada > Grace > Edsger > Tony`. Ordering by that string
gives a correctly nested listing, which is a small trick worth knowing: sorting
by path sorts a tree into document order.

## Direction is just the join condition

Run the second variant. It starts at Niklaus and walks *up*, and the only thing
that changed is which side of the join condition is which:

```
down:  JOIN chain c ON e.manager_id = c.id
up:    JOIN up    u ON u.manager_id = m.id
```

Same construct, opposite direction. Ancestors and descendants are the same
problem with the arrow reversed.

## Generating rows from nothing

The fourth variant has no table in it. The anchor is `SELECT 1` and the step
adds one until it reaches ten.

This is how you produce a sequence without a helper table: a row per day across
a date range so a report shows zeros for days with no sales, a row per bucket
for a histogram, a numbers table for splitting strings. It is one of the most
useful applications and the one people find last.

## Cycles

Everything above assumes the data is a tree. If someone becomes their own
manager's manager, the step never returns empty and the query runs until the
server stops it.

Real data acquires cycles. The defences, in increasing order of robustness:

- Carry a depth column and add `WHERE level < 50` to the step.
- Carry the path and add `WHERE instr(path, e.name) = 0` to refuse revisiting.
- Use `UNION` instead of `UNION ALL`, which deduplicates &mdash; this stops a
  cycle but costs a comparison against the whole accumulated set each round.
- In PostgreSQL, use the `CYCLE` clause, which does this properly.

A depth cap costs almost nothing and turns a hung query into a wrong-but-finite
answer, which is far easier to notice.

## Where it goes wrong

**No termination guard.** Cyclic data plus `UNION ALL` runs forever.

**An anchor that matches too much.** If the anchor selects every row rather than
the roots, every row is a starting point and the result is enormous.

**Expecting the step to see everything found so far.** It sees the previous
round only. Aggregating across all levels has to happen in the outer query.

**Recursing over a large table without an index on the join column.** Each round
is a join. Without an index each round is a scan.
""",
    check=[
        {"q": "What stops a recursive CTE?",
         "options": ["A fixed iteration limit",
                     "The recursive step returning no rows",
                     "The anchor running out",
                     "A depth column reaching zero"],
         "answer": 1,
         "why": "Nothing else halts it. With cyclic data the step keeps producing rows forever, which is why a depth cap or a path check is worth adding."},
        {"q": "What does the recursive step read on each round?",
         "options": ["The whole accumulated result so far",
                     "Only the rows produced by the previous round",
                     "Only the anchor's rows",
                     "The base table only"],
         "answer": 1,
         "why": "That is exactly what makes it a level-by-level walk. Aggregating across all levels has to happen in the outer query instead."},
        {"q": "How do you turn a descendants query into an ancestors query?",
         "options": ["Add ORDER BY DESC",
                     "Swap which side of the join condition the CTE is on, and start from a different anchor",
                     "Use UNION instead of UNION ALL",
                     "It cannot be done"],
         "answer": 1,
         "why": "Ancestors and descendants are the same walk with the arrow reversed. The construct is unchanged; only the anchor and the join condition move."},
    ],
)


# ---------------------------------------------------------------------------
# 7. EXPLAIN and query plans
# ---------------------------------------------------------------------------
topic(
    "explain_and_query_plans",
    "EXPLAIN and Query Plans",
    "Performance",
    "Ask the database what it intends to do before blaming it for being slow. "
    "Add an index and watch the plan change.",
    _svg(_txt(80, 22, "EXPLAIN QUERY PLAN", A, 9)
         + _box(16, 32, 128, 18, fill=S) + _txt(80, 44, "SCAN orders", M, 8)
         + _txt(80, 60, "&#8594; add an index &#8594;", A, 8)
         + _box(16, 66, 128, 18, fill=S) + _txt(80, 78, "SEARCH orders USING INDEX", M, 8)),
    seed="""
CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    status      TEXT NOT NULL,
    total       REAL NOT NULL
);

-- Enough rows that a scan and a seek are genuinely different work.
WITH RECURSIVE gen(n) AS (
    SELECT 1 UNION ALL SELECT n + 1 FROM gen WHERE n < 5000
)
INSERT INTO orders (id, customer_id, status, total)
SELECT n,
       (n * 7) % 400,
       CASE n % 3 WHEN 0 THEN 'paid' WHEN 1 THEN 'pending' ELSE 'shipped' END,
       (n % 97) + 1.5
FROM   gen;
""",
    starter="""-- No index on customer_id yet, so this has to look at every row.
EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE customer_id = 42;
""",
    variants_label="Watch the plan change",
    variants=[
        {"label": "1. Before the index",
         "sql": """EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE customer_id = 42;"""},
        {"label": "2. Create the index",
         "sql": """CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
SELECT 'index created - now run step 3' AS note;"""},
        {"label": "3. After the index",
         "sql": """-- SCAN has become SEARCH ... USING INDEX. That word is the whole
-- difference between reading 5000 rows and reading about 13.
EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE customer_id = 42;"""},
        {"label": "4. The index it cannot use",
         "sql": """-- Wrapping the column in a function hides it from the index.
-- Back to SCAN, on the same index, for a query that means the same thing.
EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE customer_id + 0 = 42;"""},
    ],
    notes=[
        "<code class='mono-font'>EXPLAIN</code> reports the plan the optimiser "
        "chose. It is the database's own account, not a guess.",
        "<code class='mono-font'>SCAN</code> means every row is read. "
        "<code class='mono-font'>SEARCH ... USING INDEX</code> means it jumped "
        "straight to the matching ones.",
        "The plan depends on statistics as well as indexes. On a tiny table a "
        "scan can genuinely be the better choice.",
        "An index on a column is invisible to a query that wraps that column in "
        "a function.",
    ],
    article="""
title: EXPLAIN and Query Plans
intro: The database will tell you what it plans to do. Very few people ask.

## SQL says what, not how

A query states the result you want. It says nothing about how to get it: which
table to read first, whether to use an index, whether to sort or hash for a
join. All of that is chosen by the **query optimiser**, at runtime, from the
statistics it holds about your data.

Which means that two queries returning identical results can differ by orders of
magnitude in cost, and nothing about the SQL text tells you which is which.
`EXPLAIN` is how you find out, and it takes about ten seconds.

## SCAN against SEARCH

Run the first variant. The plan reads:

```
SCAN orders
```

`SCAN` means the database intends to read **every row** and test each one. Five
thousand rows here; five million in production, at which point the query is a
problem.

Run the second variant to create an index on `customer_id`, then the third. The
plan now reads:

```
SEARCH orders USING INDEX idx_orders_customer (customer_id=?)
```

`SEARCH` means it can jump directly to the matching rows. The query text did not
change. The result does not change. The work changed from thousands of row reads
to a handful.

That contrast is the whole skill: **look for SCAN on a large table where you
expected a lookup.** Other engines use different words &mdash; PostgreSQL says
`Seq Scan` against `Index Scan`, MySQL fills in a `type` column with `ALL`
against `ref` &mdash; but the distinction is the same everywhere.

## The index it will not use

Run the fourth variant. The index still exists, the query means exactly the same
thing, and the plan is back to `SCAN`.

The difference is `customer_id + 0` instead of `customer_id`. An index stores
values of the column, in order. It does not store values of *expressions over*
the column, so the moment the column is wrapped in anything, the ordering the
index provides no longer corresponds to what the query is asking about.

This is the most common way a perfectly good index goes unused, and it hides
inside ordinary-looking SQL:

| Written | Problem | Instead |
|---|---|---|
| `WHERE YEAR(created) = 2026` | function on the column | `WHERE created >= '2026-01-01' AND created < '2027-01-01'` |
| `WHERE LOWER(email) = ?` | function on the column | index on `LOWER(email)`, or store it folded |
| `WHERE id + 0 = 42` | arithmetic on the column | `WHERE id = 42` |
| `WHERE status LIKE '%paid'` | leading wildcard | no index can help; a B-tree is ordered by prefix |

The rule: **keep the indexed column bare on one side of the comparison.**

## A scan is not always wrong

On a table of fifty rows, reading all fifty is cheaper than consulting an index
and then fetching rows one at a time. Optimisers know this and will correctly
ignore an index on a small table.

The same applies to selectivity. A query matching 60% of the rows is usually
better served by a scan, because an index gives a list of row locations that
then have to be fetched individually &mdash; and fetching most of the table one
row at a time costs more than reading it in order.

This is why plans change as tables grow, and why a query that was fast in staging
can be slow in production with the same schema and different statistics.

## Estimated against actual

`EXPLAIN` alone shows what the optimiser *intends*, using row-count estimates.
Those estimates come from statistics that can be stale or simply wrong.

Most engines offer a form that runs the query and reports what really happened
&mdash; `EXPLAIN ANALYZE` in PostgreSQL, `EXPLAIN ANALYZE` in MySQL 8.0.18 and
later. Comparing estimated rows against actual rows is the fastest way to find
out that the optimiser expected 10 rows and got 400,000, which is almost always
the reason a plan is bad.

Two habits follow: run `ANALYZE` after a bulk load so the statistics reflect the
data, and be suspicious of any plan step whose estimate is off by more than an
order of magnitude.

## Where it goes wrong

**Guessing instead of asking.** The plan is one command away and settles the
argument.

**Reading a plan for a query with no data.** Plans on an empty or tiny table
tell you nothing about production.

**Adding indexes until it is fast.** Every index costs write time and space, and
an unused index costs both for nothing. Add the one the plan asks for, then
check the plan again.

**Assuming the plan is stable.** It is recomputed as statistics change. Today's
plan is not a guarantee.
""",
    check=[
        {"q": "In a plan, what does SCAN tell you?",
         "options": ["The query failed",
                     "Every row will be read and tested",
                     "An index is being used",
                     "The table is sorted"],
         "answer": 1,
         "why": "SEARCH ... USING INDEX means it can jump straight to the matches. SCAN on a large table where you expected a lookup is the thing to look for."},
        {"q": "Why does `WHERE customer_id + 0 = 42` stop using an index on customer_id?",
         "options": ["Adding zero changes the value",
                     "The index stores column values, not values of expressions over the column",
                     "Arithmetic is not allowed in WHERE",
                     "The index needs rebuilding"],
         "answer": 1,
         "why": "The index's ordering is on the bare column. Wrap it in anything - a function, arithmetic, a cast - and that ordering no longer corresponds to what is being asked."},
        {"q": "When is a full scan the better plan?",
         "options": ["Never",
                     "On a small table, or when the query matches a large fraction of the rows",
                     "Only when no index exists",
                     "When the table is sorted"],
         "answer": 1,
         "why": "An index yields row locations that must then be fetched individually. Fetching most of a table one row at a time costs more than reading it in order."},
    ],
)


# ---------------------------------------------------------------------------
# 8. Composite and covering indexes
# ---------------------------------------------------------------------------
topic(
    "composite_and_covering_indexes",
    "Composite and Covering Indexes",
    "Performance",
    "Column order in a multi-column index decides which queries can use it. "
    "Watch one query take the index and an almost identical one refuse it.",
    _svg(_box(14, 26, 132, 16, fill=S)
         + _txt(80, 37, "INDEX (status, customer_id)", A, 8)
         + _txt(46, 58, "status = ?", M, 8) + _txt(46, 70, "usable", A, 8)
         + _txt(116, 58, "customer_id = ?", M, 8) + _txt(116, 70, "not usable", M, 8)),
    seed="""
CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    status      TEXT NOT NULL,
    total       REAL NOT NULL
);

WITH RECURSIVE gen(n) AS (
    SELECT 1 UNION ALL SELECT n + 1 FROM gen WHERE n < 5000
)
INSERT INTO orders (id, customer_id, status, total)
SELECT n,
       (n * 7) % 400,
       CASE n % 3 WHEN 0 THEN 'paid' WHEN 1 THEN 'pending' ELSE 'shipped' END,
       (n % 97) + 1.5
FROM   gen;

CREATE INDEX idx_status_customer ON orders(status, customer_id);
""",
    starter="""-- The index is on (status, customer_id), in that order.
-- This query leads with status, so it can use it.
EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE status = 'paid' AND customer_id = 42;
""",
    variants_label="Which queries can use INDEX (status, customer_id)",
    variants=[
        {"label": "Both columns",
         "sql": """EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE status = 'paid' AND customer_id = 42;"""},
        {"label": "Leading column only",
         "sql": """-- Still usable. A prefix of the index is an index.
EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE status = 'paid';"""},
        {"label": "Second column only",
         "sql": """-- Not usable as a seek. The index is sorted by status first, so
-- rows for customer 42 are scattered across the whole of it.
EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE customer_id = 42;"""},
        {"label": "Covering: never touch the table",
         "sql": """-- Every column this query needs is in the index, so the plan says
-- COVERING INDEX and the table itself is never read.
EXPLAIN QUERY PLAN
SELECT status, customer_id FROM orders WHERE status = 'paid';"""},
    ],
    notes=[
        "A composite index is sorted by its first column, then by its second "
        "within each value of the first, and so on.",
        "That makes any <em>leading prefix</em> of the columns usable, and "
        "nothing else. <code class='mono-font'>(a, b)</code> serves "
        "<code class='mono-font'>a</code> and <code class='mono-font'>a, b</code> "
        "&mdash; never <code class='mono-font'>b</code> alone.",
        "A covering index contains every column the query needs, so the table "
        "is never visited at all.",
        "Two single-column indexes are not equivalent to one composite index "
        "over the same columns.",
    ],
    article="""
title: Composite and Covering Indexes
intro: Why column order decides which queries an index can serve, and why one query never touches the table.

## An index is a sorted copy

A single-column index is a sorted list of that column's values, each paired with
a pointer to its row. Sorted means the database can binary-search it instead of
reading everything.

A **composite index** on `(status, customer_id)` is a sorted list too, sorted by
`status` first and, within each status, by `customer_id`. That is the whole
mechanism, and every rule about composite indexes falls out of it.

Think of a phone book ordered by surname then first name. Finding everyone
called Hopper is easy. Finding Grace Hopper is easy. Finding everyone whose
first name is Grace is not &mdash; the Graces are scattered throughout, one per
surname, and you would have to read the lot.

## The leftmost prefix rule

Run the four variants in order and watch the plan.

**Both columns** &mdash; `SEARCH ... USING INDEX`. The index leads with `status`,
narrows to `customer_id` within it, and lands on the rows.

**Leading column only** &mdash; still `SEARCH`. All the `paid` rows are
contiguous, so the index finds the block and reads it. A prefix of the index is
itself a usable index.

**Second column only** &mdash; `SCAN`. This is the important one. The index
exists, `customer_id` is in it, and the query cannot use it for a seek, because
rows for customer 42 are spread across every status value. There is no
contiguous block to find.

**Covering** &mdash; `USING COVERING INDEX`, discussed below.

So an index on `(a, b, c)` can serve queries filtering on `a`, on `a, b`, or on
`a, b, c`. It cannot serve `b`, `c`, or `b, c`. **Leading prefixes only.**

## The ordering rule that follows

Given that, the column order in a composite index is a design decision, not a
detail. Two guidelines:

**Equality before range.** An index on `(status, created_at)` serves
`WHERE status = 'paid' AND created_at > ?` well: the equality picks a block and
the range narrows inside it. Reversed, the range comes first and everything
after it is scattered, so only the range column is really used.

**Order for the queries you actually run.** If most queries filter by customer
and only some also filter by status, lead with customer. Reading the workload is
the only way to decide.

## Covering indexes

The fourth variant selects only `status` and `customer_id` &mdash; both of which
are already stored in the index. The plan says `USING COVERING INDEX`, and the
table is never read at all.

This is worth understanding because of what an index normally costs. An ordinary
index lookup happens in two stages: find the entries in the index, then fetch
each corresponding row from the table. That second stage is random access, and
on a large table it dominates. Returning a thousand rows can mean a thousand
scattered reads.

A covering index removes the second stage entirely. Everything the query needs is
already in the sorted structure it just searched.

Some engines let you add columns purely for coverage without making them part of
the sort key &mdash; PostgreSQL's `INCLUDE`, SQL Server's `INCLUDE`. That keeps
the index narrow where it matters for searching while still avoiding the table.

## Two indexes are not one index

A common mistake is to assume that indexes on `(a)` and `(b)` do the work of an
index on `(a, b)`.

They do not. Given both, a database can search each separately and intersect the
row sets, which some engines will do &mdash; but that means two searches and a
merge, against one search on a composite index. It is materially worse, and for
`ORDER BY a, b` the separate indexes provide no useful ordering at all.

The reverse substitution does work: `(a, b)` covers everything `(a)` alone would
have, so having both is usually redundant.

## The cost side

Indexes are not free. Every one must be updated on every insert, update and
delete of an indexed column, so a table with eight indexes does roughly nine
units of write work instead of one. They take space, they take memory in cache
that data pages could have used, and an index nobody queries costs all of that
for nothing.

The practical loop is: find the slow query, read its
[plan](explain_and_query_plans.html), add the one index the plan asks for, read
the plan again. Not: add indexes and hope.

## Where it goes wrong

**Indexing every column separately.** Expensive on write, and none of them
serves a multi-column filter well.

**Putting the range column first.** Everything after it becomes unusable.

**Forgetting the sort.** `ORDER BY` can use an index too, and a composite index
that matches the ordering removes the sort step entirely.

**Leaving redundant indexes in place.** If `(a, b)` exists, `(a)` is almost
certainly dead weight.
""",
    check=[
        {"q": "An index on (status, customer_id) exists. Which query can use it for a seek?",
         "options": ["WHERE customer_id = 42",
                     "WHERE status = 'paid'",
                     "Neither",
                     "Only queries naming both columns"],
         "answer": 1,
         "why": "The index is sorted by status first, so all the 'paid' rows are contiguous. Rows for customer 42 are scattered across every status, so there is no block to find."},
        {"q": "What does a covering index avoid?",
         "options": ["The sort step",
                     "Fetching rows from the table, because every column needed is already in the index",
                     "Updating on insert",
                     "The index search itself"],
         "answer": 1,
         "why": "An ordinary lookup searches the index and then fetches each row from the table by random access, which usually dominates. A covering index removes that second stage."},
        {"q": "Why should equality columns come before range columns in a composite index?",
         "options": ["Equality is faster to compare",
                     "A range makes everything after it scattered, so only the range column is really used",
                     "Ranges cannot be indexed",
                     "It reduces index size"],
         "answer": 1,
         "why": "An equality narrows to a contiguous block that the next column is sorted within. Once a range opens up, the following columns are no longer in a single ordered run."},
    ],
)


# ---------------------------------------------------------------------------
# 9. Isolation levels
# ---------------------------------------------------------------------------
topic(
    "isolation_levels",
    "Isolation Levels",
    "Concurrency",
    "Two transactions, one schedule, four levels. Step through and watch the "
    "same read return different answers.",
    _svg(_txt(46, 22, "A", A, 10) + _txt(114, 22, "B", A, 10)
         + _line(46, 28, 46, 80, B, 1.2) + _line(114, 28, 114, 80, B, 1.2)
         + "".join(_box(30, 34 + i * 15, 32, 9, fill=S, sw=1) for i in range(3))
         + "".join(_box(98, 41 + i * 15, 32, 9, fill=S, sw=1) for i in range(2))
         + _txt(80, 88, "who sees what, and when", M, 7)),
    timeline={
        "a": "Transaction A (a report)",
        "b": "Transaction B (a payment)",
        "intro": "Pick an isolation level, then step through. The note under "
                 "each step says what A actually sees at that moment.",
        "levels": [
            {"label": "READ UNCOMMITTED", "value": "ru"},
            {"label": "READ COMMITTED", "value": "rc"},
            {"label": "REPEATABLE READ", "value": "rr"},
            {"label": "SERIALIZABLE", "value": "ser"},
        ],
        "steps": [
            {"who": "a", "sql": "BEGIN;",
             "says": {"*": "A opens a transaction. Nothing has been read yet."}},
            {"who": "a", "sql": "SELECT SUM(total) FROM orders;  -- 1000",
             "says": {"*": "A reads 1000. Under every level this first read is the same: it is the committed state of the database."}},
            {"who": "b", "sql": "BEGIN;",
             "says": {"*": "B opens its own transaction alongside A's."}},
            {"who": "b", "sql": "UPDATE orders SET total = total + 500 WHERE id = 1;",
             "says": {"*": "B has changed a row but has NOT committed. The change exists only inside B's transaction."}},
            {"who": "a", "sql": "SELECT SUM(total) FROM orders;",
             "says": {
                 "ru": "A reads 1500. This is a DIRTY READ: A can see a change B has not committed and may still roll back. No mainstream engine defaults to this.",
                 "rc": "A reads 1000. B's change is uncommitted, so A cannot see it. Dirty reads are prevented at this level and above.",
                 "rr": "A reads 1000, for two reasons now: the change is uncommitted, and A is pinned to the snapshot it started with.",
                 "ser": "A reads 1000. The engine is also tracking that A depends on these rows, which matters at the end."}},
            {"who": "b", "sql": "COMMIT;",
             "says": {"*": "B's change is now durable and visible to anything that starts afterwards. The question is whether A sees it."}},
            {"who": "a", "sql": "SELECT SUM(total) FROM orders;",
             "says": {
                 "ru": "A reads 1500.",
                 "rc": "A reads 1500. Its two reads inside one transaction disagree - this is a NON-REPEATABLE READ. Each statement sees the latest committed data.",
                 "rr": "A reads 1000, the same as before. A is pinned to the snapshot taken at its first read, so a committed change elsewhere cannot alter what it sees.",
                 "ser": "A reads 1000, same snapshot as REPEATABLE READ."}},
            {"who": "b", "sql": "INSERT INTO orders VALUES (99, 250); COMMIT;",
             "says": {"*": "B commits a brand new row. This is the case that separates REPEATABLE READ from SERIALIZABLE in the classical definitions."}},
            {"who": "a", "sql": "SELECT COUNT(*) FROM orders;",
             "says": {
                 "ru": "A sees the new row.",
                 "rc": "A sees the new row. Its count has changed mid-transaction.",
                 "rr": "In the SQL standard this is where a PHANTOM READ is permitted: rows matching a condition may appear. PostgreSQL's snapshot prevents it; MySQL's InnoDB uses gap locks to prevent it. The standard allows it, so portable code cannot assume either way.",
                 "ser": "A does not see it, and the engine has recorded a conflict between A and B. Whichever commits second may be rejected and told to retry."}},
            {"who": "a", "sql": "COMMIT;",
             "says": {
                 "ru": "A commits. Anything it decided was based on data that may never have been committed.",
                 "rc": "A commits. Its own reads were inconsistent with each other, and no error was raised.",
                 "rr": "A commits on a consistent snapshot of the moment it began.",
                 "ser": "A may get a serialization failure here instead of a commit. That is not a bug - it is the engine telling you to retry, which is the price of the guarantee."}},
        ],
    },
    notes=[
        "Isolation is a dial between correctness and concurrency. Higher levels "
        "forbid more anomalies and permit less parallelism.",
        "<strong>Dirty read</strong>: seeing uncommitted data. "
        "<strong>Non-repeatable read</strong>: the same row changing mid-"
        "transaction. <strong>Phantom</strong>: new rows appearing.",
        "Defaults differ. PostgreSQL and Oracle default to READ COMMITTED; "
        "MySQL's InnoDB defaults to REPEATABLE READ.",
        "SERIALIZABLE does not queue everything. It detects conflicts and asks "
        "you to retry &mdash; so code using it must handle that error.",
    ],
    article="""
title: Isolation Levels
intro: What one transaction is allowed to see while another is still running.

## The dial

The I in ACID is isolation: the degree to which concurrent transactions are kept
from seeing each other's work in progress.

Perfect isolation is easy to define &mdash; run every transaction one after
another &mdash; and unacceptable in practice, because a database serving one
transaction at a time serves almost nobody. So the standard defines a dial with
four settings, described not by what they do but by which **anomalies** they
permit.

Step through the timeline above at each of the four levels. The schedule never
changes. What A sees changes at nearly every step.

## The three anomalies

**Dirty read.** Transaction A reads a row that B has changed but not committed.
If B rolls back, A acted on data that never existed. Step 5 at READ UNCOMMITTED
shows this: A reads 1500 from a change that is still provisional.

**Non-repeatable read.** A reads a row, B updates it and commits, A reads the
same row again and gets a different value. Step 7 at READ COMMITTED shows it: A
reads 1000 and then 1500 inside one transaction, with no error and no warning.

**Phantom read.** A runs a query, B inserts a row matching its condition and
commits, A runs the same query and gets an extra row. Step 9. The distinction
from a non-repeatable read is that no row A saw has changed &mdash; a new one
has arrived.

## The four levels

| Level | Dirty | Non-repeatable | Phantom |
|---|---|---|---|
| READ UNCOMMITTED | allowed | allowed | allowed |
| READ COMMITTED | prevented | allowed | allowed |
| REPEATABLE READ | prevented | prevented | allowed by the standard |
| SERIALIZABLE | prevented | prevented | prevented |

**READ UNCOMMITTED** is essentially unused. PostgreSQL accepts the syntax and
silently gives you READ COMMITTED instead, because its architecture has no way
to expose uncommitted data.

**READ COMMITTED** is the default in PostgreSQL, Oracle and SQL Server. Each
*statement* sees a fresh view of committed data. It is a sensible default and
the anomaly it permits is real: two queries in one transaction can disagree, so
a report that reads the same table twice can produce internally inconsistent
totals.

**REPEATABLE READ** pins the transaction to a snapshot taken at its first read.
Everything it sees is consistent as of that moment, no matter what commits
elsewhere. It is MySQL InnoDB's default.

**SERIALIZABLE** guarantees the result is equivalent to some serial order.
Modern implementations achieve this without locking everything, by tracking
which transactions read which rows and aborting one when a genuine conflict is
found.

## The thing about SERIALIZABLE that surprises people

It does not make your code wait. It makes your code **fail**.

At step 10 under SERIALIZABLE, A may get a serialization failure instead of a
successful commit. That is not a malfunction &mdash; it is how the guarantee is
delivered. The engine allowed both transactions to proceed optimistically,
found afterwards that no serial order explains what happened, and rejected one.

So any code running at SERIALIZABLE must catch that error and retry the whole
transaction. Code that assumes commit succeeds will fail intermittently under
load, which is the worst kind of bug to diagnose.

## Where the standard stops helping

The standard defines levels by which anomalies are *permitted*, not which are
prevented. An engine is free to prevent more than required, and they do.

PostgreSQL's REPEATABLE READ uses a full snapshot and therefore prevents
phantoms, which the standard does not require. MySQL's InnoDB prevents them at
that level too, by a different mechanism (gap locks). So code that relies on
phantoms being prevented at REPEATABLE READ works on both and is not portable by
the standard, and code that relies on phantoms *appearing* is wrong on both.

This is why "we use REPEATABLE READ" is an incomplete statement about a system's
behaviour. The engine matters.

## Choosing

Most applications should stay on the engine's default and reach for something
stronger where a specific invariant demands it. The pattern that most often
needs it is read-then-write: check a balance, then deduct from it. Between the
check and the write, another transaction can change the balance, and no
isolation level below SERIALIZABLE stops that on its own.

The alternatives are explicit locking (`SELECT ... FOR UPDATE`) or letting the
database enforce the invariant with a constraint, which needs no isolation
reasoning at all.

## Where it goes wrong

**Assuming a default.** They differ between engines, and code written against
one silently changes behaviour on the other.

**Using SERIALIZABLE without retry logic.** Intermittent failures under load.

**Long-running read transactions.** A snapshot held open forces the engine to
retain old row versions, which bloats storage and slows everything.

**Reasoning about isolation instead of using a constraint.** A `UNIQUE`
constraint settles "no two of these" regardless of what any transaction sees.
""",
    check=[
        {"q": "What is a non-repeatable read?",
         "options": ["Reading uncommitted data",
                     "Reading the same row twice in one transaction and getting different values",
                     "A new row appearing between two queries",
                     "A transaction being rolled back"],
         "answer": 1,
         "why": "It is permitted at READ COMMITTED, where each statement sees the latest committed data - so a report reading a table twice can produce internally inconsistent totals."},
        {"q": "How does SERIALIZABLE typically deliver its guarantee in a modern engine?",
         "options": ["By running transactions one at a time",
                     "By detecting conflicts and aborting a transaction, which the application must retry",
                     "By locking every table it touches",
                     "By disabling concurrent writes"],
         "answer": 1,
         "why": "It lets transactions proceed optimistically and rejects one when no serial order explains the outcome. Code that assumes commit always succeeds fails intermittently under load."},
        {"q": "Why is 'we use REPEATABLE READ' an incomplete description of behaviour?",
         "options": ["The level does not exist in all engines",
                     "The standard permits phantoms there, but PostgreSQL and MySQL each prevent them by different mechanisms",
                     "It is the same as SERIALIZABLE",
                     "It only applies to reads"],
         "answer": 1,
         "why": "The standard says which anomalies are permitted, not which are prevented, and engines prevent more than required in different ways. The engine matters as much as the level."},
    ],
)


# ---------------------------------------------------------------------------
# 10. Deadlocks
# ---------------------------------------------------------------------------
topic(
    "deadlocks_in_sql",
    "Deadlocks",
    "Concurrency",
    "Two transactions taking the same two locks in opposite orders. Step "
    "through it and watch the cycle close.",
    _svg(_box(20, 28, 40, 20, fill=S) + _txt(40, 41, "A", A, 10)
         + _box(100, 28, 40, 20, fill=S) + _txt(120, 41, "B", A, 10)
         + '<path d="M60 34 h40" stroke="%s" stroke-width="1.4" fill="none"/>' % A
         + '<path d="M100 44 h-40" stroke="%s" stroke-width="1.4" fill="none"/>' % A
         + _txt(80, 70, "each waits on the other", M, 8)),
    timeline={
        "a": "Transaction A",
        "b": "Transaction B",
        "intro": "Two transactions updating the same two rows. Step through and "
                 "watch which statement blocks.",
        "levels": [
            {"label": "Opposite order (deadlocks)", "value": "bad"},
            {"label": "Same order (safe)", "value": "good"},
        ],
        "steps": [
            {"who": "a", "sql": "BEGIN;",
             "says": {"*": "A starts."}},
            {"who": "b", "sql": "BEGIN;",
             "says": {"*": "B starts, concurrently."}},
            {"who": "a", "sql": "UPDATE accounts SET bal = bal - 100 WHERE id = 1;",
             "says": {"*": "A now holds an exclusive lock on row 1. It keeps it until it commits or rolls back - locks are never released early."}},
            {"who": "b", "sql": "UPDATE accounts SET bal = bal - 50 WHERE id = 2;",
             "says": {
                 "bad": "B locks row 2. So far nothing is wrong: two transactions holding different rows is ordinary concurrency.",
                 "good": "B wants row 1 as well, but under the same-order discipline it asks for row 1 first - and A already holds it. B blocks here, harmlessly."}},
            {"who": "a", "sql": "UPDATE accounts SET bal = bal + 100 WHERE id = 2;",
             "says": {
                 "bad": "A needs row 2, which B holds. A blocks and waits for B to finish.",
                 "good": "A proceeds. It holds both locks, because nobody could overtake it."}},
            {"who": "b", "sql": "UPDATE accounts SET bal = bal + 50 WHERE id = 1;",
             "says": {
                 "bad": "B needs row 1, which A holds. Now A waits on B and B waits on A. The wait-for graph has a cycle, and neither will ever proceed.",
                 "good": "Still blocked, waiting for A. This is a wait, not a deadlock: A is running and will finish."}},
            {"who": "a", "sql": "COMMIT;",
             "says": {
                 "bad": "This never runs. The engine's deadlock detector has already found the cycle and killed one of the two - typically the one that has done less work - with a deadlock error.",
                 "good": "A commits and releases both locks. B unblocks immediately and carries on."}},
            {"who": "b", "sql": "COMMIT;",
             "says": {
                 "bad": "The survivor commits. The victim got an error and must retry its whole transaction from the beginning.",
                 "good": "B commits. Both transactions succeeded, one after the other, with no error and no lost work."}},
        ],
    },
    notes=[
        "A deadlock is a cycle in the wait-for graph: A waits on B, B waits on "
        "A. Waiting alone is not a deadlock.",
        "Locks are held until the transaction ends. There is no way to release "
        "one early.",
        "The database detects the cycle and kills one transaction. It cannot "
        "avoid the cycle for you.",
        "The fix is discipline, not configuration: always take locks in the "
        "same order, everywhere.",
    ],
    article="""
title: Deadlocks
intro: Two transactions, two rows, and the one detail that decides whether they finish.

## Waiting is normal; a cycle is not

When a transaction updates a row it takes an exclusive lock and holds it until
it commits or rolls back. Anything else wanting that row waits.

Waiting is ordinary and self-resolving: the holder finishes, the waiter
proceeds. A **deadlock** is different. It is a *cycle* in who is waiting for
whom, and a cycle cannot resolve itself, because every participant is waiting
for another participant that will never move.

Step through the timeline with "opposite order" selected. Nothing is wrong at
step 4 &mdash; two transactions holding different rows is just concurrency. The
problem appears at step 6, when the second edge closes the loop: A holds row 1
and wants row 2; B holds row 2 and wants row 1. Neither can proceed and neither
will give up what it has.

## The database will break it, badly

Engines run a deadlock detector that periodically looks for cycles in the
wait-for graph. When it finds one it picks a **victim** &mdash; usually the
transaction that has done the least work, so the least is lost &mdash; and kills
it with a deadlock error. The survivor continues.

That resolution is necessary and it is not a fix. The victim's work is gone. If
the application does not catch the error and retry, a user's action simply
failed, and it failed intermittently, under load, in a way that is very hard to
reproduce.

## The fix is ordering

Switch the timeline to "same order" and step through again. The schedule is
almost identical; the only change is that B asks for row 1 before row 2, exactly
as A does.

Now B blocks at step 4 and stays blocked. A proceeds, finishes and releases both
locks. B unblocks and completes. Both transactions succeed, no error is raised,
and nothing is retried.

This is the whole technique: **acquire locks in a consistent order everywhere in
the application.** A cycle requires two transactions to disagree about the order,
so if nobody disagrees, no cycle can form. Ordering by primary key is the usual
choice because it is total, arbitrary and easy to apply mechanically.

The classic case is a transfer between two accounts. Written naively it locks
the source then the destination, and two transfers in opposite directions
deadlock immediately. Written as "lock the lower id first, then the higher" they
queue instead.

## What makes it more likely

**Long transactions.** Locks are held to the end, so the longer a transaction
runs the wider the window in which someone can interleave with it. Do not open a
transaction and then call an external API inside it.

**Broad locks.** A statement without an index may lock far more rows than it
needs, because rows it examines and rejects can still be locked. Adding the index
narrows the query and the locking together, which is why an index sometimes
fixes a deadlock nobody thought was an index problem.

**Escalation.** Some engines convert many row locks into one table lock past a
threshold, turning a narrow conflict into a broad one.

**Mixed access patterns.** Different code paths touching the same tables in
different orders is the underlying cause of most production deadlocks, and it
tends to appear when two features written months apart meet under load.

## Retry properly

Even with good discipline, deadlocks happen. The handling is a small amount of
code and it has to be right:

1. Catch the deadlock error specifically, not every error.
2. Retry the **whole transaction** from the beginning. Re-running the failed
   statement alone is wrong &mdash; the transaction was rolled back entirely.
3. Back off before retrying, with some randomness, so two victims do not
   collide again on the same schedule.
4. Cap the attempts and log what happened, so a genuine design problem does not
   hide behind a retry loop that quietly succeeds on the fourth attempt.

## Where it goes wrong

**Treating it as a database configuration problem.** No setting prevents
deadlocks. The order in which your code takes locks does.

**Retrying the statement instead of the transaction.** The rollback undid
everything, so the retry starts from a state that no longer exists.

**Assuming reads are safe.** `SELECT ... FOR UPDATE` takes locks and
participates in cycles exactly like an update.

**Silently swallowing the retry.** A rising deadlock rate is a signal about the
system's design. Log it.
""",
    check=[
        {"q": "What distinguishes a deadlock from ordinary lock waiting?",
         "options": ["The number of rows involved",
                     "A cycle - each transaction waits for another that is itself waiting",
                     "The isolation level",
                     "How long the wait lasts"],
         "answer": 1,
         "why": "Ordinary waiting resolves itself when the holder commits. A cycle cannot, because every participant is blocked on another participant that will never move."},
        {"q": "What is the reliable way to prevent deadlocks?",
         "options": ["Raise the lock timeout",
                     "Acquire locks in a consistent order everywhere in the application",
                     "Use a lower isolation level",
                     "Add more indexes"],
         "answer": 1,
         "why": "A cycle requires two transactions to disagree about the order. Ordering by primary key is the usual choice because it is total and can be applied mechanically."},
        {"q": "After a deadlock error, what must the application retry?",
         "options": ["The failed statement",
                     "The whole transaction from the beginning",
                     "Nothing, the engine retries it",
                     "The connection"],
         "answer": 1,
         "why": "The victim's transaction was rolled back entirely, so re-running one statement starts from a state that no longer exists."},
    ],
)

CHECKS = {"database/%s.html" % t["slug"]: {"check": t["check"]} for t in TOPICS}
