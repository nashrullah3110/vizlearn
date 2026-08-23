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


def _grid_rows(x, y, w, h, n, accent=A):
    """Stacked horizontal bands - a row store, where a row is contiguous."""
    return "".join(_box(x, y + i * (h + 3), w, h,
                        fill=(S if i else "none"),
                        stroke=(accent if i == 0 else B), sw=1.4, rx=2)
                   for i in range(n))


def _grid_cols(x, y, w, h, n, accent=A):
    """Side-by-side vertical bands - a column store, where a column is."""
    return "".join(_box(x + i * (w + 3), y, w, h,
                        fill=(S if i else "none"),
                        stroke=(accent if i == 0 else B), sw=1.4, rx=2)
                   for i in range(n))


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

# ---------------------------------------------------------------------------
# 11. MVCC
# ---------------------------------------------------------------------------
topic(
    "mvcc_in_databases",
    "MVCC: How Readers Avoid Blocking Writers",
    "Concurrency",
    "Keep the old version of a row alongside the new one, and a reader never "
    "has to wait for a writer.",
    _svg(_box(14, 22, 44, 20, fill=S) + _txt(36, 36, "v1", M, 8)
         + _box(14, 48, 44, 20, fill=S, stroke=A) + _txt(36, 62, "v2", A, 8)
         + _line(64, 44, 88, 44, B, 1.2)
         + _txt(112, 34, "reader sees v1", M, 7)
         + _txt(112, 54, "writer made v2", M, 7)),
    [
        "A write does not overwrite. It writes a new version of the row and "
        "leaves the old one for whoever is still reading it.",
        "Each transaction gets a snapshot: a rule for which versions it is "
        "allowed to see, fixed at the moment it started.",
        "Readers never block writers and writers never block readers. Two "
        "writers to the <em>same row</em> still conflict.",
        "The cost is garbage: dead versions accumulate and something has to "
        "clean them up. In PostgreSQL that is <code class='mono-font'>VACUUM</code>.",
    ],
    """
title: MVCC: How Readers Avoid Blocking Writers
intro: The idea that lets a long report run while the database keeps taking writes.

## The problem with locks

The simple way to keep transactions from interfering is locking: a reader takes
a shared lock, a writer takes an exclusive one, and the two cannot be held at
once.

It is correct, and on a busy system it is miserable. A report that scans a large
table holds read locks for its whole run, so every write to that table waits.
Meanwhile a long write transaction blocks every reader. The database spends its
time queueing rather than working, and the symptom is an application that is fast
until it is inexplicably not.

## Versions instead of locks

**Multi-version concurrency control** removes the conflict by refusing to destroy
anything. A write does not overwrite a row; it creates a *new version* of it, and
the old version stays until nobody can still need it.

Every transaction is given a **snapshot** &mdash; effectively a rule saying which
versions count as visible &mdash; fixed at the moment it starts, or at the moment
each statement starts, depending on the
[isolation level](isolation_levels.html).

A reader that began before a write simply continues to see the older version.
Nothing waits.

## What each version carries

Conceptually each row version records which transaction created it and which
transaction deleted it:

```
id  | balance | created_by | deleted_by
----+---------+------------+-----------
7   |   1000  |    100     |    142
7   |    850  |    142     |    NULL
```

Transaction 142 changed the balance. It did not edit the first line; it marked it
deleted and appended the second. A transaction with a snapshot older than 142 is
shown the first version, a newer one the second. Visibility becomes an arithmetic
comparison of transaction ids rather than a queue.

## What MVCC does not solve

This is the part that gets missed. MVCC eliminates reader/writer conflicts. It
does **not** eliminate writer/writer conflicts.

Two transactions updating the same row still contend: the second must wait for
the first to commit or roll back, because they would otherwise both produce a new
version from the same old one and one update would vanish. That is the
[lost update](isolation_levels.html) problem, and MVCC's answer to it is either a
lock on that row or a serialisation failure at commit.

So the rule is: **readers never wait, writers to the same row still do.**

## The cost: garbage

Old versions accumulate. Something has to decide when a version can no longer be
seen by any live snapshot and reclaim the space.

In PostgreSQL that job is `VACUUM`, usually run by autovacuum. When it cannot
keep up &mdash; typically because a very old transaction is still open and
pinning every version created since &mdash; tables **bloat**: the row count is
unchanged while the file grows, and every scan reads more pages for the same
data.

The practical consequence is worth stating plainly: **a transaction left open
does damage even when it is doing nothing**, because it holds back cleanup for
the whole database. An idle-in-transaction connection is a bug, not a small
inefficiency.

Different engines pay this differently. PostgreSQL keeps old versions in the
table itself and vacuums them. MySQL's InnoDB keeps them in a separate undo log
and purges it. Oracle uses undo segments, and the same open-transaction problem
appears as `ORA-01555 snapshot too old` &mdash; the old version needed was
already discarded.

## Where it goes wrong

**Long-running transactions.** They pin versions across the entire database.
Keep them short, and never leave one open across a user interaction.

**Assuming no waiting at all.** Writers to the same row still contend, and the
error surfaces as a lock wait or a serialisation failure.

**Treating table bloat as a disk problem.** It is a symptom of vacuum not
keeping up, and adding disk hides it rather than fixing it.

**Counting rows to check for bloat.** The row count is right; the file size is
the thing that grew.
""",
    [
        {"q": "What does a write do under MVCC?",
         "options": ["Overwrites the row in place and takes a lock",
                     "Creates a new version, leaving the old one for transactions still reading it",
                     "Blocks all readers until it commits",
                     "Copies the whole table"],
         "answer": 1,
         "why": "Nothing is destroyed while a live snapshot might still need it, which is exactly why a reader that began earlier never has to wait."},
        {"q": "Which conflict does MVCC NOT remove?",
         "options": ["Reader against writer", "Writer against reader",
                     "Two writers updating the same row", "Two readers"],
         "answer": 2,
         "why": "Both would produce a new version from the same old one and one update would be lost. The second waits, or fails at commit with a serialisation error."},
        {"q": "Why does an idle-in-transaction connection cause table bloat?",
         "options": ["It holds an exclusive lock",
                     "Its snapshot pins every version created since it began, so cleanup cannot reclaim them",
                     "It writes new versions continuously",
                     "It disables autovacuum"],
         "answer": 1,
         "why": "Vacuum can only reclaim a version no live snapshot can still see. One old open transaction holds back cleanup for the whole database."},
    ],
    timeline={
        "a": "Transaction A (a long report)",
        "b": "Transaction B (a payment)",
        "intro": "Step through and watch what A sees. Under MVCC it never waits, "
                 "and it never sees B's change - because A's snapshot predates it.",
        "levels": [
            {"value": "mvcc", "label": "MVCC (snapshot)"},
            {"value": "lock", "label": "Two-phase locking"},
        ],
        "steps": [
            {"who": "a", "sql": "BEGIN;",
             "says": {"mvcc": "A takes a snapshot. Everything committed before this instant is visible to A for its whole run.",
                      "lock": "A opens a transaction. No locks held yet."}},
            {"who": "a", "sql": "SELECT balance FROM accounts WHERE id = 7;  -- 1000",
             "says": {"mvcc": "A reads 1000. No lock is taken - MVCC reads do not lock.",
                      "lock": "A reads 1000 and takes a shared lock on row 7, which it will hold until commit."}},
            {"who": "b", "sql": "BEGIN;",
             "says": {"*": "B opens its own transaction."}},
            {"who": "b", "sql": "UPDATE accounts SET balance = 850 WHERE id = 7;",
             "says": {"mvcc": "B writes a NEW version of row 7. The old version stays, because A's snapshot still needs it. B does not wait.",
                      "lock": "B needs an exclusive lock, but A holds a shared lock on row 7. B BLOCKS here until A commits."}},
            {"who": "b", "sql": "COMMIT;",
             "says": {"mvcc": "B commits. The new version is now the current one for anyone starting after this point.",
                      "lock": "Still blocked. B cannot reach its COMMIT until A releases."}},
            {"who": "a", "sql": "SELECT balance FROM accounts WHERE id = 7;  -- ?",
             "says": {"mvcc": "A reads 1000 again - the old version. Its snapshot predates B's commit, so B's write is invisible to it. A is consistent with itself.",
                      "lock": "A reads 1000, because B has been waiting this whole time and has not written anything yet."}},
            {"who": "a", "sql": "COMMIT;",
             "says": {"mvcc": "A finishes. Now that no snapshot needs the old version of row 7, cleanup can reclaim it - VACUUM in PostgreSQL, purge in InnoDB.",
                      "lock": "A releases its locks. Only now can B proceed - it has been idle for the entire length of A's report."}},
        ],
    },
)


# ---------------------------------------------------------------------------
# 12. Partitioning
# ---------------------------------------------------------------------------
topic(
    "partitioning_in_databases",
    "Partitioning by Range and Hash",
    "Scale",
    "One logical table, several physical pieces. The query planner skips the "
    "pieces it can prove are irrelevant.",
    _svg(_box(12, 24, 40, 42, fill=S, stroke=A) + _txt(32, 78, "2024", M, 7)
         + _box(60, 24, 40, 42, fill=S) + _txt(80, 78, "2025", M, 7)
         + _box(108, 24, 40, 42, fill=S) + _txt(128, 78, "2026", M, 7)
         + _txt(80, 16, "one table, three files", M, 7)),
    [
        "Partitioning splits one table into pieces by a rule on a column. The "
        "table still looks like one table.",
        "<strong>Range</strong> partitions by an ordered value, usually a date. "
        "<strong>Hash</strong> spreads rows evenly by hashing a key.",
        "The win is <strong>partition pruning</strong>: a query with a predicate "
        "on the partition key touches only the partitions that can match.",
        "Dropping a partition is instant. Deleting the equivalent rows is not, "
        "which is why time-series data is almost always range-partitioned.",
    ],
    """
title: Partitioning by Range and Hash
intro: Cutting one table into pieces the planner can skip, and the choice of where to cut.

## One table, several files

Partitioning splits a table into physical pieces by a rule on one or more
columns. Applications keep querying the single logical table; the engine decides
which pieces are involved.

This is **not** sharding. Every partition lives in the same database on the same
server. [Sharding](sharding_in_databases.html) spreads data across separate
machines and is a much larger commitment.

The query above builds three range partitions and a view that unions them, which
is the shape a partitioned table has underneath. Run the variants to see what
each strategy costs.

## Range partitioning

Pick an ordered column &mdash; almost always a timestamp &mdash; and give each
partition a bounded interval.

```
orders_2024  :  order_date >= '2024-01-01' AND < '2025-01-01'
orders_2025  :  order_date >= '2025-01-01' AND < '2026-01-01'
orders_2026  :  order_date >= '2026-01-01' AND < '2027-01-01'
```

A query with `WHERE order_date >= '2026-01-01'` can be proved to need only the
last partition, so the engine reads one file instead of three. That proof is
**partition pruning**, and it is where nearly all the benefit is.

The second benefit is administrative and, for time-series data, often the bigger
one. Deleting a year of orders with `DELETE` writes a row version per deleted
row, generates enormous WAL traffic, and leaves the table bloated. `DROP TABLE
orders_2024` unlinks a file. Retention policies are the standard reason to
partition.

## Hash partitioning

Hash the key, take the remainder modulo the partition count, and store the row
there. Rows spread evenly regardless of what the values look like.

This is the right choice when there is no natural ordering to exploit and the
goal is to spread contention &mdash; many concurrent writers hitting one hot
page, for instance.

The trade-off is that **hash partitioning prunes only on equality**. A query for
one `customer_id` reaches one partition; a query for a *range* of customer ids
reaches all of them, because hashing destroys order. Range partitioning is the
opposite: it prunes ranges beautifully and can leave you with one very hot
partition if recent data is where all the traffic goes.

| | Range | Hash |
|---|---|---|
| Prunes equality | yes | yes |
| Prunes ranges | yes | **no** |
| Even distribution | no | yes |
| Drop old data instantly | yes | no |
| Typical key | timestamp | id |

## Choosing the key

The partition key must appear in the `WHERE` clause of the queries you care
about. This is the whole game, and it is where partitioning schemes go wrong.

Partition by `order_date` and then run reports by `customer_id`, and every report
reads every partition &mdash; you have added complexity and gained nothing. Worse
than nothing: each partition has its own indexes, so a query that scans them all
does more index work than it would have on a single table.

A second constraint follows: a unique constraint has to include the partition
key, because the engine cannot cheaply enforce uniqueness across pieces it is
trying not to read.

## Sizing

Too few partitions and pruning barely helps. Too many and planning cost grows,
because the planner considers each one. Somewhere between a few dozen and a few
hundred is the usual advice, with monthly partitions over a couple of years
landing naturally in that band.

Partitions can also be **subpartitioned** &mdash; range by month, then hash by
customer within each month &mdash; when both access patterns matter.

## Where it goes wrong

**Partitioning a small table.** Under a few million rows, a good index is
simpler and usually faster.

**A partition key the queries do not filter on.** No pruning, more index
overhead.

**Hash partitioning then querying ranges.** Every partition, every time.

**Forgetting the default partition.** A row that matches no partition is an error
unless a catch-all exists, and a data-loading job that fails at midnight on New
Year's Day is the classic version of this.
""",
    [
        {"q": "What is partition pruning?",
         "options": ["Deleting old partitions automatically",
                     "The planner proving a query cannot match certain partitions and skipping them",
                     "Compressing partitions that are rarely read",
                     "Merging small partitions"],
         "answer": 1,
         "why": "It requires the partition key in the WHERE clause. Without it every partition is read, and the scheme costs more than it saves."},
        {"q": "Why can hash partitioning not prune a range query?",
         "options": ["Hashes are too slow",
                     "Hashing destroys order, so adjacent key values land in unrelated partitions",
                     "Ranges are not supported",
                     "It has too few partitions"],
         "answer": 1,
         "why": "That is the trade for even distribution. Range partitioning prunes ranges well but can leave one partition hot when recent data gets all the traffic."},
        {"q": "Why is time-series data almost always range-partitioned?",
         "options": ["Timestamps hash badly",
                     "Dropping an old partition is instant, while deleting the equivalent rows writes a version each and bloats the table",
                     "Range partitions compress better",
                     "Hash partitioning cannot use timestamps"],
         "answer": 1,
         "why": "Retention is usually the bigger win over pruning. DROP TABLE unlinks a file; DELETE generates enormous WAL traffic and leaves bloat behind."},
    ],
    seed="""CREATE TABLE orders_2024 (id INTEGER, order_date TEXT, customer_id INTEGER, total REAL);
CREATE TABLE orders_2025 (id INTEGER, order_date TEXT, customer_id INTEGER, total REAL);
CREATE TABLE orders_2026 (id INTEGER, order_date TEXT, customer_id INTEGER, total REAL);

INSERT INTO orders_2024 VALUES
  (1,'2024-03-11',101,120.0),(2,'2024-07-02',102,64.5),(3,'2024-11-19',101,310.0);
INSERT INTO orders_2025 VALUES
  (4,'2025-01-08',103,45.0),(5,'2025-06-23',101,220.0),(6,'2025-12-30',104,99.9);
INSERT INTO orders_2026 VALUES
  (7,'2026-02-14',102,150.0),(8,'2026-05-05',103,72.4),(9,'2026-08-01',101,410.0);

CREATE VIEW orders AS
  SELECT * FROM orders_2024
  UNION ALL SELECT * FROM orders_2025
  UNION ALL SELECT * FROM orders_2026;
""",
    starter="""-- The view is the logical table. Underneath are three partitions.
-- This query has a predicate on the partition key, so only one
-- partition can possibly match.
SELECT * FROM orders WHERE order_date >= '2026-01-01';
""",
    variants_label="Compare the access patterns",
    variants=[
        {"label": "Prunes to one partition",
         "sql": "-- order_date is the partition key, so 2024 and 2025 can be\n"
                "-- proved irrelevant. A real partitioned table reads one file.\n"
                "SELECT * FROM orders WHERE order_date >= '2026-01-01';"},
        {"label": "Prunes nothing",
         "sql": "-- customer_id is NOT the partition key. Every partition has to\n"
                "-- be read, and each has its own indexes to work through.\n"
                "SELECT * FROM orders WHERE customer_id = 101;"},
        {"label": "Reading one partition directly",
         "sql": "-- What pruning amounts to: touch one piece, ignore the rest.\n"
                "SELECT COUNT(*), SUM(total) FROM orders_2026;"},
        {"label": "Dropping a year",
         "sql": "-- Retention on a partitioned table. Instant, and it leaves no\n"
                "-- bloat behind. Compare with DELETE FROM orders WHERE ...\n"
                "DROP TABLE orders_2024;\n"
                "SELECT COUNT(*) AS rows_left FROM orders_2025;"},
    ],
)


# ---------------------------------------------------------------------------
# 13. Sharding
# ---------------------------------------------------------------------------
topic(
    "sharding_in_databases",
    "Sharding",
    "Scale",
    "Splitting one dataset across separate machines, and the queries that stop "
    "being possible once you do.",
    _svg(_box(10, 30, 34, 34, fill=S, stroke=A) + _txt(27, 76, "node 1", M, 7)
         + _box(58, 30, 34, 34, fill=S, stroke=A) + _txt(75, 76, "node 2", M, 7)
         + _box(106, 30, 34, 34, fill=S, stroke=A) + _txt(123, 76, "node 3", M, 7)
         + _txt(80, 20, "one dataset, three servers", M, 7)),
    [
        "Partitioning splits a table across files on one server. Sharding "
        "splits it across <em>servers</em>, each with its own copy of the engine.",
        "A <strong>shard key</strong> decides which server holds a row. Every "
        "query that names it goes to one node; every query that does not fans out.",
        "Joins across shards, global unique constraints and cross-shard "
        "transactions all become hard or impossible.",
        "Shard last. Indexes, read replicas, caching and partitioning are all "
        "cheaper and reversible; sharding is neither.",
    ],
    """
title: Sharding
intro: The last resort of scaling, what it buys, and the four things it takes away.

## What it is

Sharding splits a dataset across independent database servers. Each **shard**
holds a subset of the rows and knows nothing about the others.

The distinction from [partitioning](partitioning_in_databases.html) is the
machine boundary, and it is the whole difficulty. Partitions share a query
planner, a transaction manager and a lock table. Shards share nothing, so
anything that needed a global view has to be rebuilt in the application or given
up.

## The shard key

One column decides where a row lives. Usually the key is hashed and the remainder
taken modulo the shard count, so a routing rule might be
`shard = hash(customer_id) % 4`.

The query above computes exactly that for a set of customers, and the variants
show what different access patterns cost.

The consequence is stark and worth stating as a rule:

**A query that names the shard key touches one node. A query that does not
touches all of them.**

A lookup by `customer_id` is a single-node request and stays fast as the fleet
grows. A report grouped by `product_id` has to be sent to every shard and the
partial results merged &mdash; a *scatter-gather*, whose latency is the slowest
shard's, not the average.

So the shard key is not a schema detail. It is a decision about which queries
stay cheap forever and which never will, and it is extremely expensive to change
afterwards.

## What you give up

**Cross-shard joins.** Customers on shard 1, orders on shard 3, and no engine can
join them. Either the join moves into the application, or related data is
deliberately placed together &mdash; sharding orders by `customer_id` so a
customer's orders live beside them.

**Global uniqueness.** `UNIQUE(email)` cannot be enforced across independent
servers. The usual answers are a separate lookup service that owns emails, or
generating ids that are unique by construction &mdash; UUIDs, or Snowflake-style
ids with a shard number embedded.

**Cross-shard transactions.** ACID stops at the shard boundary. Spanning shards
means two-phase commit, which is slow and introduces a coordinator that can fail
mid-protocol, or sagas, which are eventually consistent with explicit
compensation. Most teams design so that transactions never span shards.

**`AUTO_INCREMENT`.** Every shard would start at 1. Ids must come from elsewhere.

## Rebalancing

Adding a shard when the rule is `hash(key) % 4` changes it to `% 5`, and almost
every row's destination moves. Migrating the whole dataset while serving traffic
is the single worst part of operating a sharded system.

Two designs avoid it. **Consistent hashing** places shards on a ring so adding
one moves only the keys in its arc, rather than reshuffling everything.
**Virtual buckets** hash keys into a fixed large number of buckets &mdash; say
1024 &mdash; and map buckets to physical shards; adding a shard moves a few
buckets and the hash rule never changes. The bucket approach is what most modern
systems use, because moving is then a matter of copying a bucket and updating a
map.

## Do the cheaper things first

Sharding is close to irreversible and touches every part of the application.
Before it:

1. **Index properly.** A great many "we need to shard" conversations end at a
   missing [composite index](composite_and_covering_indexes.html).
2. **Read replicas**, if reads dominate. Cheap, and reversible.
3. **Caching**, for the hot small set.
4. **Partitioning**, if one table is the problem.
5. **A bigger machine.** Unglamorous, and modern hardware goes a very long way.

Shard when writes exceed what one machine can take, or the working set no longer
fits in memory anywhere, and not before.

## Where it goes wrong

**A shard key with skew.** Sharding by country puts most of the traffic on one
node. Check the distribution of real values.

**Sharding by a key the queries do not use.** Every query becomes
scatter-gather, and you have bought distributed-systems problems for no
throughput.

**Assuming transactions still work.** They work within a shard. Across shards
they do not, and code written before sharding usually assumes otherwise.

**Forgetting the slowest shard sets the latency.** One degraded node makes every
fan-out query slow.
""",
    [
        {"q": "What is the difference between partitioning and sharding?",
         "options": ["Sharding uses hashing, partitioning uses ranges",
                     "Partitions live in one database; shards live on separate servers that share no planner, lock table or transaction manager",
                     "Sharding is for reads only",
                     "Partitioning requires a shard key"],
         "answer": 1,
         "why": "The machine boundary is the whole difficulty. Anything that needed a global view - joins, unique constraints, transactions - has to be rebuilt or given up."},
        {"q": "What happens to a query that does not name the shard key?",
         "options": ["It fails",
                     "It is sent to every shard and the results merged, with latency set by the slowest one",
                     "It is routed to shard 0",
                     "It runs on a replica"],
         "answer": 1,
         "why": "Scatter-gather. This is why the shard key is a decision about which queries stay cheap forever, not a schema detail."},
        {"q": "Why do virtual buckets make rebalancing easier?",
         "options": ["They compress the data",
                     "Keys hash to a fixed large number of buckets, so adding a shard moves a few buckets rather than changing the hash rule for every row",
                     "They remove the need for a shard key",
                     "They allow cross-shard joins"],
         "answer": 1,
         "why": "With a plain hash(key) % N rule, adding a shard changes almost every row's destination. Consistent hashing solves the same problem by moving only one arc of the ring."},
    ],
    seed="""CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, country TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER, total REAL);

INSERT INTO customers VALUES
  (101,'Ada','UK'),(102,'Bo','US'),(103,'Cy','US'),(104,'Di','IN'),
  (105,'Ed','US'),(106,'Fi','UK'),(107,'Gu','US'),(108,'Hal','DE');

INSERT INTO orders VALUES
  (1,101,900,120.0),(2,102,901,64.5),(3,101,902,310.0),(4,103,900,45.0),
  (5,105,901,220.0),(6,104,900,99.9),(7,102,903,150.0),(8,107,902,72.4),
  (9,101,900,410.0),(10,108,901,58.0),(11,106,903,131.0),(12,103,900,26.5);
""",
    starter="""-- The routing rule, made visible. In a real sharded system this
-- arithmetic happens in the application or a proxy, and decides which
-- SERVER the query is sent to.
SELECT id, name, country, id % 4 AS shard
FROM   customers
ORDER  BY shard, id;
""",
    variants_label="What each access pattern costs",
    variants=[
        {"label": "Single-shard lookup",
         "sql": "-- The query names the shard key, so the router knows the answer\n"
                "-- lives on one node. This stays fast however many shards exist.\n"
                "SELECT id % 4 AS shard, id, name FROM customers WHERE id = 103;"},
        {"label": "Scatter-gather",
         "sql": "-- No shard key. Every node has to be asked and the partial\n"
                "-- results merged. Latency is the SLOWEST shard's, not the mean.\n"
                "SELECT product_id, COUNT(*) AS orders, SUM(total) AS revenue\n"
                "FROM   orders\n"
                "GROUP  BY product_id\n"
                "ORDER  BY revenue DESC;"},
        {"label": "Co-located join",
         "sql": "-- Sharding orders by customer_id puts a customer's orders on the\n"
                "-- same node as the customer, so this join never crosses a shard.\n"
                "SELECT c.id % 4 AS shard, c.name, COUNT(o.id) AS orders\n"
                "FROM   customers c JOIN orders o ON o.customer_id = c.id\n"
                "GROUP  BY c.id\n"
                "ORDER  BY shard, c.id;"},
        {"label": "A skewed shard key",
         "sql": "-- Sharding by country looks reasonable and is not: the load\n"
                "-- follows the data, and the data is not evenly spread.\n"
                "SELECT country, COUNT(*) AS customers\n"
                "FROM   customers GROUP BY country ORDER BY customers DESC;"},
    ],
)


# ---------------------------------------------------------------------------
# 14. Replication and replication lag
# ---------------------------------------------------------------------------
topic(
    "replication_and_lag",
    "Replication, Read Replicas and Lag",
    "Scale",
    "Copies of the database that serve reads, and the window in which they are "
    "wrong.",
    _svg(_box(16, 20, 42, 22, fill=S, stroke=A) + _txt(37, 34, "primary", A, 7)
         + _line(58, 31, 96, 31, B, 1.2) + _line(58, 31, 96, 58, B, 1.2)
         + _box(100, 20, 42, 22, fill=S) + _txt(121, 34, "replica", M, 7)
         + _box(100, 48, 42, 22, fill=S) + _txt(121, 62, "replica", M, 7)
         + _txt(80, 82, "reads scale, freshness does not", M, 7)),
    [
        "One primary takes the writes and streams its log to replicas, which "
        "apply it and serve reads.",
        "<strong>Replication lag</strong> is the delay between a commit on the "
        "primary and its arrival on a replica. It is never zero.",
        "The classic bug: write, redirect, read from a replica, and the user "
        "does not see their own change.",
        "Synchronous replication removes the lag and adds a network round trip "
        "to every commit. That is the trade, and it cannot be avoided.",
    ],
    """
title: Replication, Read Replicas and Lag
intro: How to serve more reads than one machine can, and the staleness that comes with it.

## The arrangement

One server &mdash; the **primary** &mdash; accepts every write. It records each
change in a log, and streams that log to one or more **replicas**, which apply
the changes to their own copies and serve read queries.

The appeal is that most workloads are overwhelmingly reads. Adding replicas
multiplies read capacity without any change to the data model, and unlike
[sharding](sharding_in_databases.html) it is reversible: a replica that is not
helping can simply be removed.

Replicas also serve as warm standbys. If the primary fails, one is promoted.

## Lag

A change committed on the primary is not instantly present on a replica. It has
to be written to the log, sent over a network, received, and applied. The gap is
**replication lag**, and it is never zero.

Under normal conditions it is milliseconds. Under load it is not, and the reasons
matter:

**A large write.** A single statement updating a million rows produces a great
deal of log to ship and apply.

**Single-threaded apply.** Some engines apply the log serially even though the
primary generated it with many concurrent connections. The replica simply cannot
keep up with a busy primary.

**A long query on the replica.** Applying a change that conflicts with a running
read forces a choice between cancelling the query and pausing replication. Both
happen, depending on configuration.

**Network.** A cross-region replica has a floor set by the speed of light.

## The bug this causes

The failure mode is specific and extremely common:

```
1. User updates their profile        -> primary
2. Application redirects to profile  ->
3. Profile page reads                -> replica, 200ms behind
4. User sees their OLD profile
```

Nothing errored. The user changed something, was shown the previous value, and
reasonably concluded the save failed.

The standard fixes, in rough order of preference:

**Read-your-writes routing.** After a write, send that user's reads to the
primary for a short window. Simple and effective.

**Route by criticality.** Anything the user just affected reads from the primary;
dashboards and search read from replicas.

**Wait for the log position.** Record the primary's log position at commit and
have the replica wait until it has applied at least that far. Correct, and
requires engine support.

**Do not redirect to a read.** Render the result from what was just written.

## Synchronous replication

The lag can be removed. `synchronous_commit` in PostgreSQL, semi-sync in MySQL:
the primary does not acknowledge a commit until at least one replica confirms it
has the change.

The cost is unavoidable and appears on every write: a commit now includes a
network round trip. Throughput falls, and latency rises by the distance to the
replica. If the synchronous replica becomes unreachable, writes stall entirely
unless a fallback is configured.

This is a direct instance of the [CAP](cap_theorem.html) trade: consistency
across replicas costs availability and latency, and no configuration escapes it.
The usual compromise is one synchronous replica nearby for durability, and
asynchronous replicas further away for read capacity.

## Failover and lost writes

If the primary fails while a replica is 200ms behind, promoting that replica
loses 200ms of committed writes. They were acknowledged to clients and are gone.

Which is why durability requirements and replication mode are the same decision.
Asynchronous replication means accepting that a failover can lose the most recent
writes.

## Where it goes wrong

**Assuming replicas are current.** They are not, and the window is where the bugs
live.

**Sending a write to a replica.** It is read-only; the error is confusing when
routing is implicit.

**Monitoring lag in bytes only.** Bytes behind does not translate to seconds
behind. Track both.

**Using replicas for locking or counters.** Anything read-then-write must go to
the primary, or two clients read the same stale value.
""",
    [
        {"q": "Why does a user sometimes not see their own change after saving?",
         "options": ["The write failed silently",
                     "The read went to a replica that has not yet applied the change",
                     "The cache was stale",
                     "The transaction rolled back"],
         "answer": 1,
         "why": "Nothing errored. Read-your-writes routing - sending that user's reads to the primary briefly after a write - is the usual fix."},
        {"q": "What does synchronous replication cost?",
         "options": ["Extra disk on the replica",
                     "A network round trip on every commit, so writes get slower and stall if the replica is unreachable",
                     "The ability to add more replicas",
                     "Read capacity"],
         "answer": 1,
         "why": "It is a direct instance of the CAP trade: consistency across replicas costs availability and latency, and no configuration escapes it."},
        {"q": "What happens if a primary fails while a replica is 200ms behind?",
         "options": ["The replica catches up first",
                     "Promoting it loses 200ms of writes that were already acknowledged to clients",
                     "Writes are replayed from the client",
                     "The failover is rejected"],
         "answer": 1,
         "why": "Those writes were confirmed and are gone. Durability requirements and replication mode are therefore the same decision."},
    ],
    timeline={
        "a": "Primary (takes the write)",
        "b": "Replica (serves the read)",
        "intro": "Step through a save-then-view. Choose the routing strategy and "
                 "watch whether the user sees their own change.",
        "levels": [
            {"value": "async", "label": "Async replica, read from replica"},
            {"value": "sticky", "label": "Async replica, read-your-writes"},
            {"value": "sync", "label": "Synchronous replication"},
        ],
        "steps": [
            {"who": "a", "sql": "UPDATE profiles SET bio = 'new bio' WHERE id = 7;",
             "says": {"*": "The write lands on the primary. Replicas know nothing about it yet."}},
            {"who": "a", "sql": "COMMIT;",
             "says": {"async": "The primary acknowledges immediately. The change is queued for shipping to the replica.",
                      "sticky": "The primary acknowledges immediately, and the application notes that this user just wrote.",
                      "sync": "The primary does NOT acknowledge yet. It waits for a replica to confirm - this is the round trip synchronous commit adds to every write."}},
            {"who": "b", "sql": "-- replication stream in flight --",
             "says": {"async": "The change is travelling. The replica is currently behind by however long this takes.",
                      "sticky": "The change is travelling, and the replica is behind - but the application is not going to ask it yet.",
                      "sync": "The replica applies the change and confirms. Only now does the primary tell the client the commit succeeded."}},
            {"who": "b", "sql": "SELECT bio FROM profiles WHERE id = 7;",
             "says": {"async": "The read goes to the replica, which has not applied the change yet. It returns the OLD bio. The user thinks the save failed.",
                      "sticky": "The application routes this read to the PRIMARY, because this user wrote recently. The new bio comes back. The replica is still behind - it just is not being asked.",
                      "sync": "The replica already has the change, because the commit did not complete until it did. The new bio comes back."}},
            {"who": "b", "sql": "-- a few hundred milliseconds later --",
             "says": {"async": "The replica catches up. A refresh now shows the new bio - which is why this bug is so often dismissed as unreproducible.",
                      "sticky": "The replica catches up, and the sticky window expires. Reads for this user go back to the replica safely.",
                      "sync": "Nothing to catch up on. The cost was paid at commit time instead, on every write whether it mattered or not."}},
        ],
    },
)


# ---------------------------------------------------------------------------
# 15. CAP theorem
# ---------------------------------------------------------------------------
topic(
    "cap_theorem",
    "The CAP Theorem",
    "Distributed",
    "When the network splits, a distributed store can stay correct or stay "
    "answering. It cannot do both.",
    _svg('<circle cx="52" cy="40" r="24" fill="none" stroke="%s" stroke-width="1.6"/>' % B
         + '<circle cx="84" cy="40" r="24" fill="none" stroke="%s" stroke-width="1.6"/>' % B
         + '<circle cx="68" cy="62" r="24" fill="none" stroke="%s" stroke-width="1.6"/>' % A
         + _txt(38, 32, "C", M, 9) + _txt(100, 32, "A", M, 9) + _txt(68, 80, "P", A, 9)
         + _txt(130, 44, "pick 2", M, 8)),
    [
        "The theorem is about what happens <em>during a network partition</em>. "
        "With no partition there is no trade to make.",
        "<strong>CP</strong>: refuse to answer rather than answer wrongly. "
        "<strong>AP</strong>: answer from what this node knows and reconcile later.",
        "'Pick two of three' is the famous phrasing and a misleading one. "
        "Partitions are not optional, so the real choice is C or A.",
        "PACELC extends it: <em>else</em>, when there is no partition, the trade "
        "is latency against consistency &mdash; and that one is always live.",
    ],
    """
title: The CAP Theorem
intro: The most quoted and most misquoted result in distributed data, and what it actually constrains.

## What the three letters mean

**Consistency** here means *linearisability*: every read sees the most recent
write, as if there were one copy. It is not the C in ACID, which is about
constraints being satisfied. Two different ideas, one letter, endless confusion.

**Availability** means every request to a non-failed node gets a non-error
response. Not "mostly up" &mdash; every request, every working node.

**Partition tolerance** means the system keeps operating when the network drops
or delays messages between nodes.

## The theorem, stated properly

The popular phrasing &mdash; "pick two of three" &mdash; is memorable and wrong
in a way that matters.

Partitions are not a design choice. Networks fail: cables are cut, switches
reboot, a cloud availability zone becomes unreachable. Any system spanning more
than one machine will be partitioned eventually, so **P is not optional**.

What the theorem actually says is narrower and more useful:

> When a partition occurs, you must choose between consistency and availability.

That is it. When the network is healthy, a system can be both consistent and
available, and most are. The theorem constrains behaviour during a specific,
temporary failure.

## The choice, concretely

Two nodes can no longer talk. A write arrives at one of them.

**CP &mdash; refuse.** Return an error, because acknowledging a write the other
side cannot see risks two different answers to the same question. Correct, and
temporarily unavailable to whoever cannot reach a quorum.

Choose this when a wrong answer is worse than no answer: account balances,
inventory that must not oversell, anything involving money or safety.

**AP &mdash; accept.** Take the write locally, serve reads from local state, and
reconcile when the partition heals. Always answering, and during the partition
two clients can see different values.

Choose this when an answer now is worth more than a perfectly current one: a
shopping cart, a social feed, a view counter, a DNS record. Amazon's original
Dynamo paper made this argument for carts explicitly &mdash; a cart that
occasionally resurrects a deleted item is better business than a cart that is
sometimes unavailable.

Step the timeline above through both settings and the difference is one decision
made at one moment.

## Reconciling afterwards

An AP system must resolve conflicting versions once the network returns.
**Last-write-wins** is simple and silently discards data when clocks disagree.
**Vector clocks** detect concurrent writes and hand the conflict to the
application. **CRDTs** are data types designed so concurrent updates merge
deterministically &mdash; which is why counters, sets and collaborative text
editors are the AP success stories.

## PACELC, which is the more useful version

CAP only describes partitions, and partitions are rare. Daniel Abadi's extension
covers the rest of the time:

> **if P**artition then **A**vailability or **C**onsistency, **E**lse
> **L**atency or **C**onsistency.

The second half is the one engineers meet daily. With the network healthy, a
system can still choose to confirm every write with remote replicas &mdash;
consistent and slower &mdash; or acknowledge locally and replicate afterwards
&mdash; faster and briefly stale.

That is exactly the [synchronous versus asynchronous replication
choice](replication_and_lag.html), and unlike CAP's trade it is live on every
request.

## Where it goes wrong

**"We chose AP, so we gave up consistency."** You gave up linearisability during
partitions. Most of the time the system is consistent.

**Confusing CAP's C with ACID's C.** Different properties.

**Calling a single-node database CP.** With one node there is no partition and
the theorem does not apply.

**Treating the labels as fixed.** Many systems are tunable per query &mdash;
Cassandra's consistency levels, DynamoDB's strongly consistent reads &mdash; so
the choice belongs to the operation, not the product.
""",
    [
        {"q": "What is wrong with 'pick two of three'?",
         "options": ["There are actually four properties",
                     "Partitions are not optional, so the real choice is between C and A when one occurs",
                     "Consistency and availability are the same thing",
                     "It only applies to SQL databases"],
         "answer": 1,
         "why": "Networks fail eventually, so P must be tolerated. The theorem constrains behaviour during that specific temporary failure, not design in general."},
        {"q": "A CP system during a partition will:",
         "options": ["Answer from local state and reconcile later",
                     "Return an error rather than risk two different answers to the same question",
                     "Elect a new primary",
                     "Queue writes indefinitely"],
         "answer": 1,
         "why": "Correct, and temporarily unavailable to anyone who cannot reach a quorum. The right choice when a wrong answer is worse than no answer."},
        {"q": "What does the 'ELC' half of PACELC describe?",
         "options": ["Error handling during partitions",
                     "The latency-against-consistency trade when the network is healthy, which is live on every request",
                     "Eventual consistency guarantees",
                     "Leader election"],
         "answer": 1,
         "why": "Confirm every write with remote replicas and be slower, or acknowledge locally and be briefly stale. It is the synchronous-versus-asynchronous replication choice."},
    ],
    timeline={
        "a": "Node A (client 1 writes here)",
        "b": "Node B (client 2 reads here)",
        "intro": "The network between the two nodes is about to fail. Pick a "
                 "strategy and step through to see what each client experiences.",
        "levels": [
            {"value": "cp", "label": "CP - refuse rather than diverge"},
            {"value": "ap", "label": "AP - answer and reconcile later"},
        ],
        "steps": [
            {"who": "a", "sql": "SELECT stock FROM items WHERE id = 1;  -- 5",
             "says": {"*": "Network healthy. Both nodes agree: 5 in stock. With no partition, the system is consistent AND available."}},
            {"who": "b", "sql": "-- network partition begins --",
             "says": {"*": "A and B can no longer reach each other. Neither has failed; they simply cannot talk. Every message between them is lost."}},
            {"who": "a", "sql": "UPDATE items SET stock = 4 WHERE id = 1;",
             "says": {"cp": "Node A cannot reach a quorum, so it REFUSES the write and returns an error. The client is told the system is unavailable - which is true, and better than a lie.",
                      "ap": "Node A accepts the write locally. Its stock is now 4. It has no way to tell B, and it proceeds anyway."}},
            {"who": "b", "sql": "SELECT stock FROM items WHERE id = 1;",
             "says": {"cp": "Node B also cannot reach a quorum. It refuses the read too. Nobody gets a wrong answer, and nobody gets an answer.",
                      "ap": "Node B answers from what it knows: 5. This is now WRONG - A has it at 4 - and B has no way to find that out. Two clients, two truths."}},
            {"who": "b", "sql": "-- partition heals --",
             "says": {"cp": "The nodes reconnect. There is nothing to reconcile, because nothing was written during the split. The system becomes available again, still correct.",
                      "ap": "The nodes reconnect and discover they disagree. Something must resolve it: last-write-wins (which can silently discard data), vector clocks, or a CRDT designed to merge deterministically."}},
            {"who": "a", "sql": "SELECT stock FROM items WHERE id = 1;",
             "says": {"cp": "5 - and the update never happened, so the client must retry. Consistency was preserved by refusing service for the duration.",
                      "ap": "4, once reconciliation picks a winner. The system never stopped answering; it was briefly wrong instead. For a shopping cart that is the right trade. For a bank balance it is not."}},
        ],
    },
)


# ---------------------------------------------------------------------------
# 16. Document model
# ---------------------------------------------------------------------------
topic(
    "document_model_vs_rows",
    "The Document Model against Rows",
    "Data Models",
    "The same data as normalised tables and as nested documents, and what each "
    "shape makes easy.",
    _svg(_table_icon(12, 24, 42) + _txt(33, 76, "rows", M, 7)
         + _txt(66, 46, "vs", M, 8)
         + _box(84, 22, 58, 46, fill=S, stroke=A)
         + _txt(113, 36, "{ order:", A, 7) + _txt(113, 48, "  items:[..]", M, 7)
         + _txt(113, 60, "}", A, 7)),
    [
        "A document stores related data together, nested. A relational schema "
        "stores it apart and joins on demand.",
        "Documents win when the access pattern is 'give me this whole thing' "
        "&mdash; one read, no joins.",
        "Rows win when the data is queried from several directions, or when the "
        "same fact appears in many documents and has to stay consistent.",
        "SQLite, PostgreSQL and MySQL all have JSON columns, so the choice is "
        "per-column now rather than per-database.",
    ],
    """
title: The Document Model against Rows
intro: One order, stored two ways, and an honest account of which questions each shape answers well.

## The same order, two shapes

Run the query above and then the variants. The identical order is stored as
normalised rows and as a single JSON document, and both are queried in the same
session &mdash; because modern SQL engines support both.

**Relational**: an `orders` row, several `order_items` rows referring back to it,
a `customers` row. Each fact recorded once, joined when needed.

**Document**: one record containing the order, its items nested inside it, and
the customer details copied in.

## What documents make easy

**One read for one thing.** Fetching an order means retrieving one document.
No joins, no round trips, and the data is contiguous on disk. For a
read-this-whole-object access pattern, this is genuinely faster and the gap
widens as the object gets more parts.

**A shape that matches the code.** The document deserialises straight into an
object. No object-relational mapping layer reassembling a graph from five result
sets.

**Schema flexibility.** Adding a field to some documents and not others requires
no migration. For genuinely heterogeneous data &mdash; product catalogues where
a book and a fridge share almost no attributes &mdash; this is a real advantage
rather than laziness.

## What rows make easy

**Querying from any direction.** "Which customers bought product 902" is
straightforward relationally and awkward in a document store, because the data
is organised around orders, not products. Documents optimise one access path and
make the others harder.

**Updating a shared fact once.** If the customer's address is copied into every
order document, changing it means finding and rewriting every one. Relationally
it is a single `UPDATE`. This is the classic normalisation argument and it has
not stopped being true.

**Integrity the database enforces.** Foreign keys, uniqueness and check
constraints are declared once and cannot be bypassed. In a document store these
usually become application code, which means they hold until some other code
path forgets.

**Ad-hoc analysis.** Aggregating across documents means either a scan or a
purpose-built index, and the queries are harder to write.

## Denormalisation is the actual trade

Nesting the items inside the order is fine &mdash; an order item belongs to
exactly one order and is never queried independently. That is not duplication,
just co-location.

Copying the customer's name and address into every order is duplication, and it
buys read speed at the cost of update cost and the risk of divergence. Sometimes
that is right: an invoice arguably *should* record the address as it was at the
time, in which case it is not duplication at all but a historical fact.

The question is always whether the copies must agree. If they must, storing them
separately means keeping them in sync forever.

## The distinction has mostly dissolved

PostgreSQL's `jsonb` is indexable, queryable and transactional. MySQL and SQLite
have JSON functions &mdash; the queries on this page use SQLite's, in the same
session as ordinary tables.

So the modern answer is usually neither purely one nor the other: relational
tables for the entities that are queried from several directions and must stay
consistent, and a JSON column for the parts that are genuinely variable and only
ever read alongside their parent.

What a dedicated document database still offers is horizontal scaling and
operational tooling built around that model from the start. What it gives up is
joins and multi-document transactions &mdash; though MongoDB has had the latter
since 4.0, which narrowed the gap considerably.

## Where it goes wrong

**Choosing documents to avoid schema design.** The schema still exists; it has
moved into the application, where nothing enforces it.

**Unbounded arrays.** A document that grows without limit &mdash; every event
appended to one record &mdash; eventually exceeds the size limit and rewrites
the whole thing on every append.

**Duplicating a fact that must stay consistent.** Fine for a historical snapshot,
a slow disaster for live data.

**Using JSON columns for well-structured data.** If every row has the same
fields, they are columns. Putting them in JSON gives up type checking and
constraints for nothing.
""",
    [
        {"q": "When does the document model genuinely beat normalised rows?",
         "options": ["Always, for reads",
                     "When the access pattern is fetching one whole object, since it is a single read with no joins",
                     "When data must be strongly consistent",
                     "When the same fact appears in many places"],
         "answer": 1,
         "why": "The data is contiguous and deserialises straight into an object. The gap widens as the object gains parts - and closes when queries come from other directions."},
        {"q": "What is the real cost of copying a customer's address into every order document?",
         "options": ["Disk space",
                     "Every change means finding and rewriting every copy, and any missed copy diverges",
                     "Slower reads",
                     "It breaks JSON indexing"],
         "answer": 1,
         "why": "The question is whether the copies must agree. On an invoice the address arguably should be a historical fact, in which case it is not duplication at all."},
        {"q": "Why has the relational/document distinction largely dissolved?",
         "options": ["Document stores added SQL",
                     "PostgreSQL, MySQL and SQLite all have indexable, queryable, transactional JSON columns, so the choice is per-column",
                     "Documents turned out to be slower",
                     "Normalisation was abandoned"],
         "answer": 1,
         "why": "Tables for entities queried from several directions, a JSON column for genuinely variable parts read only alongside their parent - in one database, in one transaction."},
    ],
    seed="""CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, placed TEXT);
CREATE TABLE order_items (order_id INTEGER, product TEXT, qty INTEGER, price REAL);

INSERT INTO customers VALUES (101,'Ada','Leeds'),(102,'Bo','Bristol');
INSERT INTO orders VALUES (1,101,'2026-08-01'),(2,102,'2026-08-03');
INSERT INTO order_items VALUES
  (1,'keyboard',1,45.0),(1,'cable',2,6.5),(1,'mouse',1,22.0),
  (2,'monitor',1,180.0),(2,'cable',1,6.5);

CREATE TABLE order_docs (id INTEGER PRIMARY KEY, doc TEXT);
INSERT INTO order_docs VALUES
 (1,'{"id":1,"placed":"2026-08-01","customer":{"id":101,"name":"Ada","city":"Leeds"},"items":[{"product":"keyboard","qty":1,"price":45.0},{"product":"cable","qty":2,"price":6.5},{"product":"mouse","qty":1,"price":22.0}]}'),
 (2,'{"id":2,"placed":"2026-08-03","customer":{"id":102,"name":"Bo","city":"Bristol"},"items":[{"product":"monitor","qty":1,"price":180.0},{"product":"cable","qty":1,"price":6.5}]}');
""",
    starter="""-- The relational shape: three tables, joined on demand.
SELECT c.name, o.id AS order_id, i.product, i.qty, i.price
FROM   orders o
JOIN   customers   c ON c.id = o.customer_id
JOIN   order_items i ON i.order_id = o.id
ORDER  BY o.id, i.product;
""",
    variants_label="The same data, both ways",
    variants=[
        {"label": "Relational: join three tables",
         "sql": "-- Each fact stored once. Reassembled at query time.\n"
                "SELECT c.name, o.id AS order_id, i.product, i.qty, i.price\n"
                "FROM   orders o\n"
                "JOIN   customers   c ON c.id = o.customer_id\n"
                "JOIN   order_items i ON i.order_id = o.id\n"
                "ORDER  BY o.id, i.product;"},
        {"label": "Document: one read, no joins",
         "sql": "-- The whole order in one row. This is the access pattern\n"
                "-- documents are good at.\n"
                "SELECT json_extract(doc,'$.customer.name') AS customer,\n"
                "       json_extract(doc,'$.id')            AS order_id,\n"
                "       json_extract(value,'$.product')     AS product,\n"
                "       json_extract(value,'$.qty')         AS qty\n"
                "FROM   order_docs, json_each(order_docs.doc,'$.items')\n"
                "ORDER  BY order_id, product;"},
        {"label": "Querying the other way round",
         "sql": "-- 'Who bought a cable?' is natural relationally...\n"
                "SELECT c.name, i.qty\n"
                "FROM   order_items i\n"
                "JOIN   orders o    ON o.id = i.order_id\n"
                "JOIN   customers c ON c.id = o.customer_id\n"
                "WHERE  i.product = 'cable';"},
        {"label": "...and awkward as documents",
         "sql": "-- ...but the documents are organised around orders, so this has\n"
                "-- to unnest every one of them to find the same answer.\n"
                "SELECT json_extract(d.doc,'$.customer.name') AS name,\n"
                "       json_extract(value,'$.qty')           AS qty\n"
                "FROM   order_docs d, json_each(d.doc,'$.items')\n"
                "WHERE  json_extract(value,'$.product') = 'cable';"},
        {"label": "The duplicated fact",
         "sql": "-- Ada moves to York. Relationally that is one row. In the\n"
                "-- documents her city is copied into every order she ever placed.\n"
                "UPDATE customers SET city = 'York' WHERE id = 101;\n"
                "SELECT (SELECT city FROM customers WHERE id=101)          AS relational,\n"
                "       json_extract(doc,'$.customer.city')                AS in_document\n"
                "FROM   order_docs WHERE id = 1;"},
    ],
)


# ---------------------------------------------------------------------------
# 17. Key-value and graph models
# ---------------------------------------------------------------------------
topic(
    "key_value_and_graph_models",
    "Key-Value and Graph Models",
    "Data Models",
    "Two models at opposite ends: one that does almost nothing very fast, and "
    "one built entirely around following relationships.",
    _svg(_box(10, 28, 46, 18, fill=S) + _txt(33, 40, "key &#8594; value", M, 7)
         + _txt(33, 60, "no queries", M, 7)
         + '<circle cx="92" cy="30" r="6" fill="none" stroke="%s" stroke-width="1.4"/>' % A
         + '<circle cx="122" cy="46" r="6" fill="none" stroke="%s" stroke-width="1.4"/>' % A
         + '<circle cx="92" cy="62" r="6" fill="none" stroke="%s" stroke-width="1.4"/>' % A
         + _line(98, 33, 116, 43, B, 1) + _line(98, 59, 116, 50, B, 1)
         + _txt(107, 80, "edges are the point", M, 7)),
    [
        "A key-value store supports get, put and delete on an opaque value. "
        "That is the entire interface.",
        "The narrowness is the feature: no query planner, no joins, and a "
        "lookup that is a hash away.",
        "A graph model makes relationships first-class. Traversing them costs "
        "the same whether the graph is small or huge.",
        "In SQL, a graph traversal is a recursive CTE &mdash; possible, and "
        "verbose enough to show why a dedicated model exists.",
    ],
    """
title: Key-Value and Graph Models
intro: The simplest data model and the most relationship-centred one, and when each is worth leaving SQL for.

## Key-value: doing less on purpose

The interface is three operations:

```
get(key)  ->  value
put(key, value)
delete(key)
```

The value is opaque &mdash; a blob the store does not interpret. You cannot query
by its contents, sort by it, or join on it. There is no schema and no query
language.

That poverty is the point. With no query planner, no join algorithms and no
secondary indexes to maintain, a lookup is a hash and a read. Redis, Memcached,
DynamoDB in its simplest mode and etcd all live here, and they are fast in a way
a general-purpose database cannot match, because they have far less to do.

The cost is that every access path must be designed in advance, encoded in the
key. Fetching a user by id means `user:1234`. Fetching them by email means
maintaining a second key, `email:ada@example.com -> 1234`, and keeping the two in
step yourself &mdash; there is no unique constraint and no transaction spanning
them.

The first variant above shows the shape: a two-column table used as nothing but a
key lookup.

**Where it fits.** Caches, sessions, feature flags, rate limiters, leaderboards,
service discovery. Anything with one obvious access path and a strong preference
for speed.

**Where it does not.** Anything needing an ad-hoc question. "How many active
sessions are from Leeds" is not answerable without scanning every key, which the
model is not built for.

## Graph: relationships as the primary thing

A graph model stores **nodes** and **edges**, and both can carry properties. The
edges are not derived from matching values, as a foreign key is; they are stored
objects, and traversing one is following a pointer.

The difference shows up in queries about *paths*. "Who reports to Ada, directly
or indirectly, to any depth" is one traversal in a graph and a recursive CTE in
SQL &mdash; run the variant and compare it against the ordinary join beside it.

The gap widens with depth. Each level of a relational traversal is another join,
and the planner's estimates degrade as they compound; a graph engine follows
edges directly, and cost scales with the number of edges actually visited rather
than with the size of the tables.

**Where it fits.** Social networks, org charts, fraud rings, dependency graphs,
recommendation paths, network topology, knowledge graphs. The test is whether
your interesting questions are about connections rather than about attributes.

**Where it does not.** Aggregating over millions of rows. A graph engine is
usually worse at "total revenue by month" than any relational database.

## The honest comparison

| | Key-value | Relational | Graph |
|---|---|---|---|
| Lookup by id | fastest | fast | fast |
| Ad-hoc queries | no | yes | limited |
| Joins | no | yes | native, as traversal |
| Variable-depth paths | no | recursive CTE | native |
| Aggregation | no | yes | weak |
| Schema enforcement | none | strong | usually light |

## Do you need to leave SQL?

Frequently not, and the variants above are the argument.

A key-value table in Postgres &mdash; a primary key and a `jsonb` column &mdash;
gets you most of the model with transactions and the option of querying the
value later. Redis wins on raw latency; if that is not the binding constraint,
the simpler operational story usually is.

Recursive CTEs handle graph traversal, and for a few hundred thousand edges at
modest depth they are perfectly good. Dedicated graph engines start winning at
deep traversals over large graphs, and at query *expressibility* &mdash; Cypher
and Gremlin say in one line what a recursive CTE says in fifteen.

The strong argument for a separate store is when the workload is
overwhelmingly of one shape. The weak argument is that the model is fashionable.

## Where it goes wrong

**Using a key-value store as the system of record without a plan for secondary
access.** The second access path is your problem, forever.

**Assuming a graph database is faster at everything.** It is faster at
traversals and often slower at aggregates.

**Recursive CTEs without a depth limit.** A cycle in the data is an infinite
loop; the variant here carries a guard for exactly that reason.

**Modelling everything as a graph.** If the questions are about attributes rather
than connections, a table is the better graph.
""",
    [
        {"q": "Why is a key-value store fast?",
         "options": ["It keeps everything in memory",
                     "It has no query planner, joins or secondary indexes to maintain, so a lookup is a hash and a read",
                     "It compresses values",
                     "It skips durability"],
         "answer": 1,
         "why": "The narrow interface is the feature. The cost is that every access path must be designed in advance and encoded in the key."},
        {"q": "How does a graph edge differ from a SQL foreign key?",
         "options": ["It is faster to write",
                     "It is a stored object followed like a pointer, rather than a value matched at query time",
                     "It can only connect two node types",
                     "It cannot carry properties"],
         "answer": 1,
         "why": "This is why traversal cost scales with edges visited rather than table size, and why the gap against joins widens with depth."},
        {"q": "What is a graph database usually worse at than a relational one?",
         "options": ["Variable-depth traversal",
                     "Aggregating over millions of rows, such as total revenue by month",
                     "Storing properties on relationships",
                     "Finding shortest paths"],
         "answer": 1,
         "why": "The test for reaching for a graph model is whether your interesting questions are about connections rather than about attributes."},
    ],
    seed="""CREATE TABLE kv (key TEXT PRIMARY KEY, value TEXT);
INSERT INTO kv VALUES
  ('user:1234','{"name":"Ada","email":"ada@example.com"}'),
  ('user:1235','{"name":"Bo","email":"bo@example.com"}'),
  ('email:ada@example.com','1234'),
  ('email:bo@example.com','1235'),
  ('session:abc','{"user":1234,"expires":"2026-08-25T10:00:00"}');

CREATE TABLE people (id INTEGER PRIMARY KEY, name TEXT, role TEXT);
CREATE TABLE reports_to (person INTEGER, manager INTEGER);

INSERT INTO people VALUES
  (1,'Ada','CTO'),(2,'Bo','Eng Manager'),(3,'Cy','Eng Manager'),
  (4,'Di','Engineer'),(5,'Ed','Engineer'),(6,'Fi','Engineer'),
  (7,'Gu','Intern'),(8,'Hal','Engineer');

INSERT INTO reports_to VALUES
  (2,1),(3,1),(4,2),(5,2),(6,3),(7,4),(8,3);
""",
    starter="""-- The key-value model, in its entirety: get by key.
-- No query language, no joins, no way to ask about the value.
SELECT value FROM kv WHERE key = 'user:1234';
""",
    variants_label="Both models, and the SQL equivalents",
    variants=[
        {"label": "Key-value: get",
         "sql": "-- The whole interface. Fast because there is nothing to plan.\n"
                "SELECT value FROM kv WHERE key = 'user:1234';"},
        {"label": "Key-value: the second access path",
         "sql": "-- Wanting users by email means maintaining a SECOND key yourself,\n"
                "-- and keeping the two in step without a constraint to help.\n"
                "SELECT k2.value AS user_json\n"
                "FROM   kv k1\n"
                "JOIN   kv k2 ON k2.key = 'user:' || k1.value\n"
                "WHERE  k1.key = 'email:ada@example.com';"},
        {"label": "Graph: one hop",
         "sql": "-- Direct reports. A single join - relational SQL is fine here.\n"
                "SELECT m.name AS manager, p.name AS reports\n"
                "FROM   reports_to r\n"
                "JOIN   people p ON p.id = r.person\n"
                "JOIN   people m ON m.id = r.manager\n"
                "WHERE  m.name = 'Ada';"},
        {"label": "Graph: any depth",
         "sql": "-- Everyone under Ada, however deep. In Cypher this is one line.\n"
                "-- The depth guard is not decoration: a cycle in the data would\n"
                "-- otherwise loop forever.\n"
                "WITH RECURSIVE chain(id, name, depth) AS (\n"
                "    SELECT id, name, 0 FROM people WHERE name = 'Ada'\n"
                "  UNION ALL\n"
                "    SELECT p.id, p.name, c.depth + 1\n"
                "    FROM   chain c\n"
                "    JOIN   reports_to r ON r.manager = c.id\n"
                "    JOIN   people p     ON p.id = r.person\n"
                "    WHERE  c.depth < 10\n"
                ")\n"
                "SELECT depth, name FROM chain WHERE depth > 0 ORDER BY depth, name;"},
        {"label": "Graph: path to the top",
         "sql": "-- The other direction: the chain of command above one person.\n"
                "WITH RECURSIVE up(id, name, depth) AS (\n"
                "    SELECT id, name, 0 FROM people WHERE name = 'Gu'\n"
                "  UNION ALL\n"
                "    SELECT m.id, m.name, u.depth + 1\n"
                "    FROM   up u\n"
                "    JOIN   reports_to r ON r.person = u.id\n"
                "    JOIN   people m     ON m.id = r.manager\n"
                "    WHERE  u.depth < 10\n"
                ")\n"
                "SELECT depth, name FROM up ORDER BY depth;"},
    ],
)


# ---------------------------------------------------------------------------
# 18. OLTP vs OLAP and columnar storage
# ---------------------------------------------------------------------------
topic(
    "oltp_vs_olap_columnar",
    "OLTP, OLAP and Columnar Storage",
    "Analytics",
    "Two workloads that want opposite things from disk, and the storage layout "
    "that serves each.",
    _svg(_grid_rows(12, 24, 44, 12, 3, A) + _txt(34, 78, "row store", M, 7)
         + _grid_cols(94, 24, 12, 36, 3, A) + _txt(116, 78, "column store", M, 7)),
    [
        "<strong>OLTP</strong>: many small transactions touching whole rows. "
        "<strong>OLAP</strong>: few huge queries touching a few columns.",
        "A row store keeps a row's fields together, so reading one row is one "
        "page read. Reading one column reads every page.",
        "A column store keeps each column together, so an aggregate reads only "
        "the columns it names.",
        "Columns of one type compress far better than mixed rows &mdash; often "
        "ten times &mdash; and less data read is the actual speed-up.",
    ],
    """
title: OLTP, OLAP and Columnar Storage
intro: Why the database that runs your application is the wrong one for your dashboards.

## Two workloads

**OLTP** &mdash; online transaction processing &mdash; is the application
database. Many concurrent connections, each doing something small: fetch this
order, insert this payment, update this status. Queries touch few rows and
usually want all of a row's columns. Latency per query matters enormously.

**OLAP** &mdash; online analytical processing &mdash; is the reporting workload.
Few concurrent users, each asking something enormous: revenue by region by month
for three years. Queries touch millions of rows and usually want three or four
columns out of fifty. Throughput matters; a query taking two seconds instead of
two hundred milliseconds is fine.

These want opposite things, and the disagreement is about physical layout.

## How rows are stored

A **row store** keeps each row's fields contiguously:

```
[1|Ada|Leeds|2026-08-01|120.00][2|Bo|Bristol|2026-08-03|64.50]...
```

Fetching order 2 is a single page read, and everything needed is there. Perfect
for OLTP.

Now compute the average of `total` over ten million orders. Every page has to be
read, because the totals are scattered one per row, separated by all the other
columns. To read 8 bytes of interest you read a 200-byte row, and 96% of the I/O
is waste.

## How columns are stored

A **column store** keeps each column contiguously:

```
ids:     [1][2][3][4]...
names:   [Ada][Bo][Cy][Di]...
totals:  [120.00][64.50][45.00][220.00]...
```

That average now reads only the `totals` region. Reading a fiftieth of the data
is roughly a fiftieth of the time, and the advantage grows with the width of the
table.

Two further wins follow from the layout rather than being added to it.

**Compression.** A column holds one type, and often few distinct values. A
`country` column across ten million rows compresses to almost nothing with
dictionary encoding; a sorted date column run-length encodes brilliantly. Mixed
row data does none of this. Ten-times ratios are ordinary, and the speed-up is
mostly the reduced I/O.

**Vectorised execution.** Values of one type packed contiguously can be processed
in batches with SIMD instructions, instead of one row at a time through a tuple
interface.

The cost is the mirror image: fetching one whole row means one read per column
and reassembly, and inserting a row means writing into fifty places. Columnar
stores are therefore usually append-oriented and batch-loaded, not
update-in-place.

## Choosing

| | Row store | Column store |
|---|---|---|
| Fetch a whole row | fast | slow |
| Aggregate one column | slow | fast |
| Insert or update one row | fast | slow |
| Bulk load | fine | ideal |
| Compression | poor | excellent |
| Examples | PostgreSQL, MySQL | ClickHouse, BigQuery, DuckDB, Snowflake |

## Do not run both on one database

The usual mistake is analytics against the production OLTP database. A report
scanning ten million rows evicts the working set from the buffer cache, and every
application query afterwards goes to disk. The dashboard is slow *and* the
checkout is slow.

The standard arrangement separates them: OLTP handles the application, data is
copied into an analytical store on a schedule or a stream, and reports run there
with a [star schema](star_schema.html) shaped for them. The copy is stale by
minutes or hours, which is almost always acceptable for reporting and is the
price of not having the two workloads fight.

The variants above make the difference concrete: the same table queried the OLTP
way and the OLAP way, with a note on how much of each row each one actually
needs.

## Where the line has blurred

**DuckDB** is columnar, embedded and single-file &mdash; analytical power with no
cluster. **Postgres** has columnar extensions and can query Parquet through
foreign data wrappers. **Parquet** itself has made columnar a file format rather
than a database, so the same data can be read by many engines.

The result is that "we need a data warehouse" is a much bigger claim than it was.
For datasets under a few hundred gigabytes, DuckDB over Parquet on one machine
frequently outperforms a cluster.

## Where it goes wrong

**Reporting off the primary.** Cache eviction makes the application slow, and the
cause is not obvious from the application's own metrics.

**Row-by-row inserts into a columnar store.** They are built for batches; single
inserts are pathologically slow.

**`SELECT *` on a column store.** It gives up the entire advantage.

**Assuming you need a cluster.** Measure on one machine first.
""",
    [
        {"q": "Why is a row store slow at averaging one column over ten million rows?",
         "options": ["It cannot use indexes",
                     "The values are scattered one per row, so every page must be read to collect a small fraction of each",
                     "Averages require a full sort",
                     "Row stores do not compress"],
         "answer": 1,
         "why": "To read 8 bytes of interest you read the whole 200-byte row. A column store reads only the region holding that column."},
        {"q": "Why do column stores compress so much better?",
         "options": ["They use a stronger algorithm",
                     "A column holds one type and often few distinct values, so dictionary and run-length encoding work extremely well",
                     "They discard nulls",
                     "They store less data"],
         "answer": 1,
         "why": "Ten-times ratios are ordinary, and since the bottleneck is I/O, less data read is most of the speed-up."},
        {"q": "What goes wrong when reports run against the production OLTP database?",
         "options": ["The reports return stale data",
                     "A large scan evicts the working set from the buffer cache, so application queries afterwards go to disk",
                     "The reports lock the tables",
                     "Transactions fail"],
         "answer": 1,
         "why": "The dashboard is slow and the checkout is slow, and the cause is not visible in the application's own metrics."},
    ],
    seed="""CREATE TABLE orders (
  id INTEGER PRIMARY KEY, customer TEXT, country TEXT, region TEXT,
  placed TEXT, channel TEXT, status TEXT, total REAL, tax REAL, shipping REAL);

INSERT INTO orders VALUES
 (1,'Ada','UK','EMEA','2026-01-14','web','shipped',120.0,24.0,4.5),
 (2,'Bo','US','AMER','2026-01-22','app','shipped',64.5,5.2,3.0),
 (3,'Cy','US','AMER','2026-02-03','web','shipped',45.0,3.6,3.0),
 (4,'Di','IN','APAC','2026-02-18','app','returned',220.0,39.6,6.0),
 (5,'Ed','US','AMER','2026-03-07','web','shipped',99.9,8.0,3.0),
 (6,'Fi','UK','EMEA','2026-03-29','web','shipped',150.0,30.0,4.5),
 (7,'Gu','DE','EMEA','2026-04-11','app','shipped',72.4,13.8,4.5),
 (8,'Hal','US','AMER','2026-05-02','web','cancelled',410.0,32.8,3.0),
 (9,'Ada','UK','EMEA','2026-06-19','app','shipped',58.0,11.6,4.5),
 (10,'Bo','US','AMER','2026-07-25','web','shipped',131.0,10.5,3.0);
""",
    starter="""-- OLTP: fetch one whole order. A row store has every field of this
-- row on one page, so this is a single read.
SELECT * FROM orders WHERE id = 4;
""",
    variants_label="The two workloads on one table",
    variants=[
        {"label": "OLTP: one row, all columns",
         "sql": "-- What the application does thousands of times a second.\n"
                "-- Row storage is exactly right for this.\n"
                "SELECT * FROM orders WHERE id = 4;"},
        {"label": "OLAP: all rows, three columns",
         "sql": "-- What a dashboard does. Ten of the table's columns are\n"
                "-- irrelevant, and a row store reads them anyway.\n"
                "SELECT region, COUNT(*) AS orders, ROUND(SUM(total),2) AS revenue\n"
                "FROM   orders\n"
                "WHERE  status = 'shipped'\n"
                "GROUP  BY region\n"
                "ORDER  BY revenue DESC;"},
        {"label": "How much of each row is wasted",
         "sql": "-- The aggregate above names 3 of 10 columns. On a row store the\n"
                "-- other 7 are read from disk regardless; a column store skips them.\n"
                "SELECT 10 AS columns_in_table,\n"
                "        3 AS columns_the_query_needs,\n"
                "       '70%' AS io_a_row_store_wastes;"},
        {"label": "Why a column compresses",
         "sql": "-- One column, one type, few distinct values. This is what\n"
                "-- dictionary encoding exploits, and why columnar files are small.\n"
                "SELECT COUNT(*) AS rows,\n"
                "       COUNT(DISTINCT region)  AS distinct_regions,\n"
                "       COUNT(DISTINCT channel) AS distinct_channels,\n"
                "       COUNT(DISTINCT total)   AS distinct_totals\n"
                "FROM   orders;"},
    ],
)


# ---------------------------------------------------------------------------
# 19. Star schema
# ---------------------------------------------------------------------------
topic(
    "star_schema",
    "Star Schema: Facts and Dimensions",
    "Analytics",
    "One narrow table of things that happened, surrounded by wide tables "
    "describing them. The shape warehouses are built in.",
    _svg(_box(58, 34, 44, 22, fill=S, stroke=A) + _txt(80, 48, "facts", A, 8)
         + _box(10, 12, 34, 16, fill=S) + _txt(27, 23, "date", M, 7)
         + _box(116, 12, 34, 16, fill=S) + _txt(133, 23, "product", M, 7)
         + _box(10, 62, 34, 16, fill=S) + _txt(27, 73, "store", M, 7)
         + _box(116, 62, 34, 16, fill=S) + _txt(133, 73, "customer", M, 7)
         + _line(44, 24, 62, 36, B, 1) + _line(116, 24, 98, 36, B, 1)
         + _line(44, 66, 62, 54, B, 1) + _line(116, 66, 98, 54, B, 1)),
    [
        "The <strong>fact</strong> table holds measurements &mdash; one row per "
        "event, mostly numbers and foreign keys. It is long and narrow.",
        "<strong>Dimension</strong> tables describe the context &mdash; dates, "
        "products, stores. Short and wide, full of text.",
        "Every query is the same shape: join the fact table to whichever "
        "dimensions the question mentions, group, aggregate.",
        "It is deliberately denormalised. A snowflake schema normalises the "
        "dimensions and trades query simplicity for tidiness.",
    ],
    """
title: Star Schema: Facts and Dimensions
intro: The one schema design that analytical databases are actually optimised for.

## Two kinds of table

A star schema splits everything into facts and dimensions, and the split is
sharper than it first sounds.

A **fact** is a measurement of something that happened. One row per sale, per
click, per sensor reading. It contains numbers you want to aggregate &mdash;
quantity, amount, duration &mdash; and foreign keys pointing at the dimensions.
Almost nothing else. Fact tables are enormous and narrow.

A **dimension** describes the context of a fact. The product dimension holds the
name, category, brand, supplier; the date dimension holds the day, month,
quarter, day of week, whether it was a holiday. Dimension tables are small and
wide, and mostly text.

Drawn out, the fact table sits in the middle with dimensions radiating from it,
which is where the name comes from.

## Why it is shaped that way

Every analytical question has the same form: *aggregate some measure, sliced by
some attributes, filtered by others*. Revenue by category by month for one
region. Units sold by store by weekday.

In a star schema every such query is the same join: fact table to the dimensions
the question mentions, group by their attributes, aggregate the fact's measures.
Run the variants above and they are all that shape.

That uniformity has three consequences worth having.

**Query planners handle it well.** The pattern is recognisable enough that
analytical engines have a dedicated *star join* optimisation: filter the small
dimensions first, use the result to restrict the fact-table scan, and never
materialise a large intermediate.

**Analysts can write the queries.** Adding a slice means adding a join and a
group-by column. No investigation of a normalised graph is required.

**BI tools generate them.** Tableau, Looker and Power BI all assume this model,
and produce good SQL against it and poor SQL against anything else.

## The date dimension

A table of dates looks redundant &mdash; a database has date functions. It earns
its place anyway, because it holds things no function knows: your fiscal
calendar, public holidays in the markets you sell in, which weeks were promotion
periods, whether a day was a weekday in the local sense.

`WHERE d.is_holiday` and `GROUP BY d.fiscal_quarter` are then ordinary joins
rather than a growing pile of `CASE` expressions.

## Grain

The most consequential decision is the **grain**: what exactly one fact row
represents.

"One row per order line" and "one row per order" are different grains, and mixing
them corrupts every aggregate &mdash; sum a per-order total across order lines
and you have multiplied the revenue by the number of lines. This is the most
common defect in real warehouses, and it is silent.

State the grain in one sentence before creating the table, and make every measure
consistent with it.

## Slowly changing dimensions

A product moves category. Do historical facts belong to the old category or the
new one?

**Type 1**: overwrite. Simple, and history is rewritten &mdash; last year's
report changes.

**Type 2**: add a new dimension row with validity dates and point new facts at
it. History is preserved and the dimension grows. This is the usual choice, and
it is why dimension tables have surrogate keys rather than using the natural
business key.

**Type 3**: keep a `previous_category` column. Enough for one level of history,
rarely enough in practice.

## Star against snowflake

Normalising the dimensions &mdash; splitting `product` into product, category and
supplier tables &mdash; gives a **snowflake schema**. It removes redundancy and
adds joins.

For warehouses the star is usually preferred, because dimensions are small
enough that the redundancy costs little, the extra joins cost real query time,
and the denormalised version is far easier to read. The exception is a genuinely
large dimension &mdash; tens of millions of customers &mdash; where the
duplication starts to matter.

## Where it goes wrong

**Mixed grain.** Silent, and it inflates every total.

**Text in the fact table.** It belongs in a dimension; it makes the largest table
wider for no benefit.

**No date dimension.** Fiscal calendars and holidays end up as `CASE`
expressions copied between queries.

**Type 1 everywhere.** History quietly rewrites itself, and last quarter's report
no longer reproduces.
""",
    [
        {"q": "What does a fact table contain?",
         "options": ["Descriptive attributes like product names and categories",
                     "One row per event: numeric measures plus foreign keys to the dimensions",
                     "One row per customer",
                     "Aggregated totals"],
         "answer": 1,
         "why": "Long and narrow. The descriptive text lives in the dimensions, which are short and wide - putting it in the fact table widens the largest table for nothing."},
        {"q": "Why is mixing grain in a fact table so dangerous?",
         "options": ["It breaks foreign keys",
                     "Summing a per-order total across order lines multiplies revenue by the number of lines, and nothing errors",
                     "It prevents indexing",
                     "It makes joins ambiguous"],
         "answer": 1,
         "why": "It is the most common defect in real warehouses precisely because it is silent. State the grain in one sentence before creating the table."},
        {"q": "Why do star schemas usually beat snowflake schemas in a warehouse?",
         "options": ["They use less storage",
                     "Dimensions are small enough that the redundancy costs little, while the extra joins cost real query time",
                     "Snowflake schemas cannot be indexed",
                     "BI tools cannot read snowflakes"],
         "answer": 1,
         "why": "The exception is a genuinely large dimension - tens of millions of customers - where duplication starts to matter more than the joins."},
    ],
    seed="""CREATE TABLE dim_date (date_key INTEGER PRIMARY KEY, day TEXT, month TEXT,
                       quarter TEXT, weekday TEXT, is_holiday INTEGER);
CREATE TABLE dim_product (product_key INTEGER PRIMARY KEY, name TEXT,
                          category TEXT, brand TEXT);
CREATE TABLE dim_store (store_key INTEGER PRIMARY KEY, store TEXT,
                        city TEXT, region TEXT);
CREATE TABLE fact_sales (date_key INTEGER, product_key INTEGER, store_key INTEGER,
                         units INTEGER, revenue REAL);

INSERT INTO dim_date VALUES
 (1,'2026-01-05','January','Q1','Monday',0),(2,'2026-01-06','January','Q1','Tuesday',0),
 (3,'2026-02-16','February','Q1','Monday',1),(4,'2026-04-09','April','Q2','Thursday',0),
 (5,'2026-04-10','April','Q2','Friday',0),(6,'2026-07-20','July','Q3','Monday',0);

INSERT INTO dim_product VALUES
 (1,'Keyboard','Peripherals','Acme'),(2,'Monitor','Displays','Acme'),
 (3,'Cable','Peripherals','Genco'),(4,'Laptop','Computers','Genco');

INSERT INTO dim_store VALUES
 (1,'Leeds Central','Leeds','North'),(2,'Bristol Quay','Bristol','South'),
 (3,'Online','-','Online');

INSERT INTO fact_sales VALUES
 (1,1,1,3,135.0),(1,3,1,10,65.0),(2,2,3,2,360.0),(2,1,2,1,45.0),
 (3,4,3,1,899.0),(3,3,2,4,26.0),(4,2,1,1,180.0),(4,1,3,5,225.0),
 (5,4,2,2,1798.0),(5,3,3,20,130.0),(6,2,2,3,540.0),(6,1,1,2,90.0);
""",
    starter="""-- Every analytical query is this shape: the fact table joined to
-- whichever dimensions the question mentions, grouped by their
-- attributes, aggregating the fact's measures.
SELECT p.category, SUM(f.units) AS units, ROUND(SUM(f.revenue),2) AS revenue
FROM   fact_sales f
JOIN   dim_product p ON p.product_key = f.product_key
GROUP  BY p.category
ORDER  BY revenue DESC;
""",
    variants_label="Same shape, different slices",
    variants=[
        {"label": "Slice by one dimension",
         "sql": "SELECT p.category, SUM(f.units) AS units,\n"
                "       ROUND(SUM(f.revenue),2) AS revenue\n"
                "FROM   fact_sales f\n"
                "JOIN   dim_product p ON p.product_key = f.product_key\n"
                "GROUP  BY p.category\n"
                "ORDER  BY revenue DESC;"},
        {"label": "Add a second dimension",
         "sql": "-- Adding a slice is adding a join and a group-by column.\n"
                "-- Nothing else about the query changes.\n"
                "SELECT d.quarter, s.region, ROUND(SUM(f.revenue),2) AS revenue\n"
                "FROM   fact_sales f\n"
                "JOIN   dim_date  d ON d.date_key  = f.date_key\n"
                "JOIN   dim_store s ON s.store_key = f.store_key\n"
                "GROUP  BY d.quarter, s.region\n"
                "ORDER  BY d.quarter, revenue DESC;"},
        {"label": "What the date dimension is for",
         "sql": "-- No date function knows your holidays or your fiscal calendar.\n"
                "-- A dimension does, and the filter is an ordinary join.\n"
                "SELECT d.day, d.weekday, ROUND(SUM(f.revenue),2) AS revenue\n"
                "FROM   fact_sales f\n"
                "JOIN   dim_date d ON d.date_key = f.date_key\n"
                "WHERE  d.is_holiday = 1\n"
                "GROUP  BY d.day, d.weekday;"},
        {"label": "Three dimensions at once",
         "sql": "-- The star join: filter the small dimensions, use the result to\n"
                "-- restrict the large fact scan.\n"
                "SELECT d.month, p.brand, s.region,\n"
                "       SUM(f.units) AS units, ROUND(SUM(f.revenue),2) AS revenue\n"
                "FROM   fact_sales f\n"
                "JOIN   dim_date    d ON d.date_key    = f.date_key\n"
                "JOIN   dim_product p ON p.product_key = f.product_key\n"
                "JOIN   dim_store   s ON s.store_key   = f.store_key\n"
                "WHERE  p.brand = 'Acme'\n"
                "GROUP  BY d.month, p.brand, s.region\n"
                "ORDER  BY revenue DESC;"},
    ],
)


# ---------------------------------------------------------------------------
# 20. SQL injection and parameterised queries
# ---------------------------------------------------------------------------
topic(
    "sql_injection_and_parameters",
    "SQL Injection and Parameterised Queries",
    "Safety",
    "What goes wrong when data is pasted into a query string, and the one fix "
    "that actually works.",
    _svg(_box(12, 26, 62, 20, fill=S) + _txt(43, 39, "' OR 1=1 --", A, 7)
         + _txt(43, 60, "input", M, 7)
         + _line(78, 36, 96, 36, B, 1.2)
         + _box(100, 26, 48, 20, fill="none", stroke=A) + _txt(124, 39, "query", A, 7)
         + _txt(124, 60, "now different", M, 7)),
    [
        "Injection happens when input is <em>concatenated</em> into SQL, so the "
        "database cannot tell data from instructions.",
        "A parameterised query sends the SQL and the values separately. The "
        "value can never become syntax, whatever it contains.",
        "Escaping is not the fix. It is a blacklist, it varies by engine and "
        "charset, and it fails on numeric contexts entirely.",
        "Identifiers &mdash; table and column names &mdash; cannot be "
        "parameterised. Those need an allowlist.",
    ],
    """
title: SQL Injection and Parameterised Queries
intro: The oldest widespread vulnerability in web software, why it happens, and the single correct fix.

## The mechanism

Build a query by pasting user input into a string:

```
"SELECT * FROM users WHERE name = '" + name + "'"
```

With `name = "Ada"` this produces a sensible query. With
`name = "' OR '1'='1"` it produces:

```
SELECT * FROM users WHERE name = '' OR '1'='1'
```

The quote closed the string early, and everything after it became **syntax**
rather than data. The database is not confused or exploited &mdash; it is
correctly executing the query it was given. The bug happened before it arrived.

Run the variants above to see it: the same lookup, safe and unsafe, with a normal
value and then a crafted one.

## What can be done through it

A closed quote gives an attacker the whole language.

**Authentication bypass.** `' OR '1'='1` as a password makes the `WHERE` clause
true for every row.

**Reading other tables.** A `UNION SELECT` appends results from anywhere the
database user can read.

**Writing.** If the driver allows multiple statements, a semicolon starts a new
one.

**Blind extraction.** Even with no output at all, a condition that changes
whether the page errors, or how long it takes, leaks one bit per request &mdash;
and one bit per request is enough to read a password hash.

## The fix

Send the query and the values separately:

```
cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
```

The `?` is a **placeholder**. The database receives the query text and the value
through different channels, parses the statement first, and then binds the value
into an already-parsed plan.

The value therefore cannot alter the structure of the query, because parsing has
already finished by the time it arrives. `' OR '1'='1` becomes a search for a
user whose name is literally `' OR '1'='1`, which finds nothing.

This is not a filter that might miss something. It is a structural guarantee:
there is no input for which a bound parameter becomes syntax.

## Why escaping is not the fix

Escaping tries to neutralise dangerous characters in the input. It fails for
reasons that are not obvious in advance:

**Numeric contexts have no quotes.** `WHERE id = " + id` needs no quote to
escape, and `1 OR 1=1` needs no special characters at all.

**Character sets.** Multi-byte encodings have historically allowed a byte
sequence that becomes a quote after the escaping function has run.

**It is a blacklist.** Every blacklist is a claim to have thought of everything.

**It is per-engine.** Rules differ between MySQL, PostgreSQL and SQLite, and code
that moves between them silently stops being correct.

Parameterisation avoids all of this by never putting the value in the query text
at all.

## Identifiers cannot be parameterised

This is the real limitation. A placeholder can stand for a *value*, not for a
table or column name:

```
"ORDER BY " + column      -- cannot be parameterised
```

The correct approach is an **allowlist**: map the user's input to a known-good
identifier and reject anything unrecognised.

```
allowed = {"name": "name", "date": "created_at"}
column = allowed.get(user_input)
if column is None: reject()
```

Never sanitise an identifier by escaping. Choose it from a fixed set.

## The other layers

Parameterise everywhere, and then:

**Least privilege.** The application's database user should not own the schema or
be able to `DROP`. It limits the damage of any bug, not just this one.

**Do not show database errors.** Error text is how blind extraction is made
fast.

**ORMs help but do not immunise.** Their query builders parameterise by default,
and every one of them has a raw-SQL escape hatch that does not. The escape hatch
is where the vulnerabilities are.

## Where it goes wrong

**"It is an internal tool."** Internal input is still input, and internal tools
get exposed.

**Parameterising most of a query.** One concatenated fragment is enough.

**Trusting a value because it came from a dropdown.** The dropdown is in the
client. The request is not.

**Escaping instead of binding.** Even when correct today, it is one encoding
change from not being.
""",
    [
        {"q": "Why does a parameterised query prevent injection?",
         "options": ["It escapes dangerous characters",
                     "The statement is parsed before the value arrives, so the value can never become syntax",
                     "It validates input types",
                     "It runs with fewer privileges"],
         "answer": 1,
         "why": "It is a structural guarantee rather than a filter: there is no input for which a bound parameter turns into query structure."},
        {"q": "Why is escaping an inadequate defence?",
         "options": ["It is slow",
                     "Numeric contexts have no quotes to escape, character sets can defeat it, and it is a per-engine blacklist",
                     "It breaks Unicode",
                     "It only works on SELECT"],
         "answer": 1,
         "why": "WHERE id = 1 OR 1=1 contains no special characters at all. Parameterisation avoids the whole class by never putting the value in the query text."},
        {"q": "How should a user-supplied ORDER BY column be handled?",
         "options": ["Parameterise it with a placeholder",
                     "Map it through an allowlist of known-good identifiers and reject anything else",
                     "Escape it",
                     "Wrap it in quotes"],
         "answer": 1,
         "why": "Placeholders stand for values, not identifiers. Identifiers must be chosen from a fixed set rather than sanitised."},
    ],
    seed="""CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, role TEXT);
INSERT INTO users VALUES
  (1,'Ada','ada@example.com','admin'),
  (2,'Bo','bo@example.com','user'),
  (3,'Cy','cy@example.com','user'),
  (4,'Di','di@example.com','user');

CREATE TABLE password_resets (user_id INTEGER, token TEXT);
INSERT INTO password_resets VALUES (1,'a1b2-secret-token'),(2,'c3d4-secret-token');
""",
    starter="""-- The intended query, with an ordinary value concatenated in.
-- Nothing looks wrong yet.
SELECT id, name, role FROM users WHERE name = 'Ada';
""",
    variants_label="The same lookup, four ways",
    variants=[
        {"label": "Normal input, concatenated",
         "sql": "-- name = \"Ada\". Looks fine, and the bug is already present.\n"
                "SELECT id, name, role FROM users WHERE name = 'Ada';"},
        {"label": "Crafted input: bypass",
         "sql": "-- name = \"' OR '1'='1\". The quote closed the string early and\n"
                "-- the rest became syntax. Every row comes back.\n"
                "SELECT id, name, role FROM users WHERE name = '' OR '1'='1';"},
        {"label": "Crafted input: read another table",
         "sql": "-- A UNION appends results from anywhere this database user can\n"
                "-- read. Nothing about the original query intended this.\n"
                "SELECT id, name, role FROM users WHERE name = ''\n"
                "UNION SELECT user_id, token, 'leaked' FROM password_resets;"},
        {"label": "Parameterised: the fix",
         "sql": "-- In application code this is  WHERE name = ?  with the value\n"
                "-- passed separately. The lab has no driver to bind through, so\n"
                "-- this is what binding AMOUNTS to: the crafted string arriving\n"
                "-- as a VALUE rather than as syntax. The statement is parsed\n"
                "-- first, so this searches for a user literally named\n"
                "--     ' OR '1'='1\n"
                "-- and nobody is. Zero rows - the payload is inert.\n"
                "SELECT id, name, role FROM users WHERE name = ''' OR ''1''=''1';"},
        {"label": "Why escaping is not enough",
         "sql": "-- A numeric context has no quotes to escape, and this payload\n"
                "-- contains no special characters for an escaper to catch.\n"
                "SELECT id, name, role FROM users WHERE id = 1 OR 1=1;"},
    ],
)

CHECKS = {"database/%s.html" % t["slug"]: {"check": t["check"]} for t in TOPICS}
